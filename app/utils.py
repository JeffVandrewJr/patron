from app import db
from app.models import BTCPayClientStore
from btcpay import BTCPayClient
from btcpay.crypto import generate_privkey
from flask import request, current_app
import os
import re
import signal
from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    # prevents malicious redirects
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def pairing(code, host):
    # pairs BTCPay
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


def hup_gunicorn():
    # romuald/gunicorn-hup
    mre = re.compile(r'^gunicorn:\s+master\s+\[(.*)\]')
    pids = [ int(pid) for pid in os.listdir('/proc') if pid.isdigit() ]
    for pid in pids:
        path = os.path.join('/proc', str(pid), 'cmdline')
        try:
            data = open(path).read()
        except Exception:
            continue
        found = mre.search(data)
        if not found:
            continue
        current_app.logger.info("HUP: %d" % pid)
        os.kill(pid, signal.SIGHUP)
