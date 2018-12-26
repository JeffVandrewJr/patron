from app import db
from app.api import bp
from app.models import BTCPayClientStore, User
from datetime import timedelta
from flask import request, abort


@bp.route('/v1/updatesub', methods=['GET', 'POST'])
def update_sub():
    # receives and processes pmt notifications from BTCPay
    if not request.json or 'id' not in request.json:
        abort(400)
    btc_client_store = BTCPayClientStore.query.all().first()
    btc_client = btc_client_store.client
    invoice = btc_client.get_invoice(request.json['id'])
    if isinstance(invoice, dict):
        if 'status' in invoice:
            if invoice['status'] == "paid" or "confirmed":
                user = User.query.filter_by(username=invoice['buyer']['name']).first()
                if user is None:
                    return "Payment made for unregistered user.", 200
                if user.role == 'admin':
                    return "Administrator should not make payments.", 200
                else:
                    user.expiration = user.expiration + timedelta(days=30)
                    user.role = invoice['orderId']
                    db.session.commit()
                    return "Payment Accepted", 201
            else:
                return "Status not paid or confirmed.", 200
        else:
            return "No payment status received.", 400
    else:
        return "Invalid transaction ID.", 400
