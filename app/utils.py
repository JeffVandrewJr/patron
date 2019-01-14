from app import db
from app.models import BTCPayClientStore
from btcpay import BTCPayClient
from btcpay.crypto import generate_privkey
from flask import request
from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def pairing(code, host):
    privkey = generate_privkey()
    btc_client = BTCPayClient(host=host, pem=privkey)
    btc_token = btc_client.pair_client(code)
    btc_client = BTCPayClient(host=host, pem=privkey, tokens=btc_token)
    client_store = BTCPayClientStore.query.first()
    if client_store is None:
        client_store = BTCPayClientStore(client=btc_client)
        db.session.add(client_store)
    else:
        client_store.client = btc_client
    db.session.commit()
