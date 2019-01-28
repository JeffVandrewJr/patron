from app import db
from app.api import bp
from app.models import BTCPayClientStore, User, Square, PriceLevel
from datetime import datetime, timedelta
from flask import request, redirect, flash, url_for, current_app
from flask_login import current_user, login_required
from squareconnect.api_client import ApiClient
from squareconnect.apis.customers_api import CustomersApi
from squareconnect.apis.transactions_api import TransactionsApi
from squareconnect.models.create_customer_request import \
        CreateCustomerRequest
from squareconnect.models.create_customer_card_request import \
        CreateCustomerCardRequest
import uuid


@bp.route('/v1/updatesub', methods=['GET', 'POST'])
def update_sub():
    # receives and processes pmt notifications from BTCPay
    if not request.json or 'id' not in request.json:
        return "Not a valid IPN.", 200
    btc_client_store = BTCPayClientStore.query.all()[0]
    btc_client = btc_client_store.client
    invoice = btc_client.get_invoice(request.json['id'])
    if isinstance(invoice, dict):
        if 'status' in invoice:
            current_app.logger.info('IPN: ' + invoice['status'])
            if invoice['status'] == "paid" or \
               invoice['status'] == "complete" or \
               invoice['status'] == "confirmed":
                user = User.query.filter_by(
                    username=invoice['buyer']['name']).first()
                if user is None:
                    return "Payment made for unregistered user.", 200
                if user.role == 'admin':
                    return "Administrator should not make payments.", 200
                elif invoice['status'] == "confirmed":
                    if user.last_payment != invoice['id']:
                        user.last_payment = invoice['id']
                        if user.expiration <= datetime.today():
                            base = datetime.today()
                        else:
                            base = user.expiration
                        user.expiration = base + timedelta(days=30)
                        user.role = invoice['orderId']
                        user.renew = True
                        db.session.commit()
                        return "Payment Accepted", 201
                    else:
                        return "Payment Already Processed", 200
                elif invoice['status'] == "paid":
                    # add a few hours if expired or almost expired
                    measure = user.expiration - timedelta(hours=6)
                    if measure <= datetime.today():
                        user.expiration = datetime.today()\
                                + timedelta(hours=6)
                        user.role = invoice['orderId']
                        user.renew = False
                        db.session.commit()
                elif invoice['status'] == "complete":
                    # handle lightning payments
                    if user.last_payment != invoice['id']:
                        user.last_payment = invoice['id']
                        if user.expiration <= datetime.today():
                            base = datetime.today()
                        else:
                            base = user.expiration
                        user.expiration = base + timedelta(days=30)
                        user.role = invoice['orderId']
                        user.renew = True
                        db.session.commit()
                        return "Payment Accepted", 201
                    else:
                        return "Payment Already Processed", 200
                else:
                    return "IPN Received", 200
            else:
                return "Status not paid or confirmed.", 200
        else:
            return "No payment status received.", 200
    else:
        return "Invalid transaction ID.", 400


@bp.route('/v1/square/<int:price>', methods=['GET', 'POST'])
@login_required
def process_square(price):
    '''
    Receives a nonce from Square, and uses the nonce to
    charge the card. Upon successful charge, it updates the
    user's subscription and stores the Square Customer ID and
    Card ID for future charges.
    '''
    if not request.form or 'nonce' not in request.form:
        return "Bad Request", 422
    square = Square.query.first()
    nonce = request.form['nonce']
    api_client = ApiClient()
    api_client.configuration.access_token = square.access_token
    customers_api = CustomersApi(api_client)
    customer_request = CreateCustomerRequest(
        email_address=current_user.email)
    try:
        customer_res = customers_api.create_customer(customer_request)
    except Exception as e:
        flash('Card could not be processed.')
        current_app.logger.error(e, exc_info=True)
        return redirect(url_for('main.support'))
    customer = customer_res.customer
    if customer is None:
        flash('Card could not be processed.')
        current_app.logger.info(
            f'''
            {current_user.username} card declined:
            {customer_res.errors}
            '''
        )
        return redirect(url_for('main.support'))
    else:
        customer_card_request = CreateCustomerCardRequest(
            card_nonce=nonce,
        )
        try:
            card_res = customers_api.create_customer_card(
                customer.id,
                customer_card_request,
            )
        except Exception as e:
            flash('Card could not be processed.')
            current_app.logger.error(e, exc_info=True)
            return redirect(url_for('main.support'))
        card = card_res.card
        if card is None:
            flash('Card could not be processed.')
            current_app.logger.info(
                f'''
                {current_user.username} card declined:
                {card_res.errors}
                '''
            )
            return redirect(url_for('main.support'))
        else:
            current_user.square_id = customer.id
            current_user.square_card = card.id
    transactions_api = TransactionsApi(api_client)
    idempotency_key = str(uuid.uuid1())
    cents = price * 100
    amount = {'amount': cents, 'currency': 'USD'}
    body = {
        'idempotency_key': idempotency_key,
        'customer_id': current_user.square_id,
        'customer_card_id': current_user.square_card,
        'amount_money': amount,
    }
    try:
        charge_response = transactions_api.charge(
            square.location_id, body
        )
    except Exception as e:
        flash('Card could not be processed.')
        current_app.logger.error(e, exc_info=True)
        return redirect(url_for('main.support'))
    transaction = charge_response.transaction
    if transaction is None:
        flash('Card could not be processed.')
        current_app.logger.info(
            f'''
            {current_user.username} card declined:
            {charge_response.errors}
            '''
        )
        return redirect(url_for('main.support'))
    elif transaction.id is not None:
        flash('Subscription Updated')
        if current_user.expiration <= datetime.today():
            base = datetime.today()
        else:
            base = current_user.expiration
        current_user.expiration = base + timedelta(days=30)
        new_role = PriceLevel.query.filter_by(price=price).first()
        if hasattr(new_role, 'name'):
            current_user.role = new_role.name
        else:
            current_user.role = PriceLevel.query.first().name
            current_app.logger.error(f'{current_user.username} \
                        signed up for nonexistent price level.')
        db.session.commit()
        return redirect(url_for('main.index'))
