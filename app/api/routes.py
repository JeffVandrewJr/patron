from app import db
from app.api import bp
from app.models import BTCPayClientStore, User, Square, PriceLevel
from datetime import datetime, timedelta
from flask import request, redirect, flash, url_for, current_app
from flask_login import current_user
import requests
from squareconnect.api_client import ApiClient
from squareconnect.apis.customers_api import CustomersApi
from squareconnect.apis.transactions_api import TransactionsApi
from squareconnect.models.create_customer_request import \
        CreateCustomerRequest
from squareconnect.models.create_customer_card_request import \
        CreateCustomerCardRequest
from urllib.parse import parse_qsl
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
            if invoice['status'] == "paid" or \
               invoice['status'] == "confirmed":
                user = User.query.filter_by(
                    username=invoice['buyer']['name']).first()
                if user is None:
                    return "Payment made for unregistered user.", 200
                if user.role == 'admin':
                    return "Administrator should not make payments.", 200
                elif invoice['status'] == "confirmed":
                    if user.expiration <= datetime.today():
                        base = datetime.today()
                    else:
                        base = user.expiration
                    user.expiration = base + timedelta(days=30)
                    user.role = invoice['orderId']
                    db.session.commit()
                    return "Payment Accepted", 201
                elif invoice['status'] == "paid":
                    # add a few hours if expired or almost expired
                    measure = user.expiration - timedelta(hours=6)
                    if measure <= datetime.today():
                        user.expiration = datetime.today()\
                                + timedelta(hours=6)
                        user.role = invoice['orderId']
                        db.session.commit()
                    return "Payment Accepted", 201
                else:
                    return "IPN Received", 200
            else:
                return "Status not paid or confirmed.", 200
        else:
            return "No payment status received.", 200
    else:
        return "Invalid transaction ID.", 400


@bp.route('/v1/square/<int:price>', methods=['GET', 'POST'])
def process_square(price):
    if not request.form or 'nonce' not in request.form:
        return "Bad Request", 422
    square = Square.query.first()
    nonce = request.form['nonce']
    api_client = ApiClient()
    api_client.configuration.access_token = square.access_token
    if current_user.square_id is None:
        customers_api = CustomersApi(api_client)
        customer_request = CreateCustomerRequest(
            email_address=current_user.email)
        try:
            customer_res = customers_api.create_customer(customer_request)
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
                card_res = customers_api.create_customer_card(
                    customer.id,
                    customer_card_request,
                )
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
                    current_user.square_id = customer
                    current_user.square_card = card
        except Exception as e:
            flash('Card could not be processed.')
            current_app.logger.error(e, exc_info=True)
            return redirect(url_for('main.support'))
    else:
        customer = current_user.square_id
        card = current_user.square_card
    try:
        transactions_api = TransactionsApi(api_client)
        idempotency_key = str(uuid.uuid1())
        cents = price * 100
        amount = {'amount': cents, 'currency': 'USD'}
        body = {
            'idempotency_key': idempotency_key,
            'customer_id': customer.id,
            'customer_card_id': card.id,
            'amount_money': amount,
        }
        charge_response = transactions_api.charge(
            square.location_id, body
        )
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
            try:
                current_user.role = PriceLevel.query.filter_by(
                    price=price).first().name
            except Exception as e:
                if current_user.role is None:
                    current_user.role = PriceLevel.query.first().name
                current_app.logger.error(e, exc_info=True)
            db.session.commit()
            return redirect(url_for('main.index'))
    except Exception as e:
        flash('Card could not be processed.')
        current_app.logger.error(e, exc_info=True)
        return redirect(url_for('main.support'))


@bp.route('/v1/updatesubpaypal', methods=['GET', 'POST'])
def update_sub_paypal():
    # TODO this was probably mooted by Square integration
    params = parse_qsl(request.form)
    params.append(('cmd', '_notify-validate'))
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Python-IPN-Verification-Script'
    }
    r = requests.post(
        VERIFY_URL,
        params=params,
        headers=headers,
        verify=True
    )
    r.raise_for_status()
    if r.text == 'VERIFIED':
        user.expiration = datetime.today() + timedelta(days=30)
        db.session.commit()
    elif r.text == 'INVALID':
        return None
