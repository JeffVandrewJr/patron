from app import db
from app.models import BTCPayClientStore
from btcpay import BTCPayClient
from btcpay.crypto import generate_privkey


def pairing(code, host):
    privkey = generate_privkey()
    btc_client = BTCPayClient(host=host, pem=privkey)
    btc_token = btc_client.pair_client(code)
    btc_client = BTCPayClient(host=host, pem=privkey, tokens=btc_token)
    client_store = BTCPayClientStore.query.all().first()
    if client_store is None:
        client_store = BTCPayClientStore(client=btc_client)
    else:
        client_store.client = btc_client
    db.session.add(client_store)
    db.session.commit()
