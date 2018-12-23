from btcpay import BTCPayClient
from btcpay.crypto import generate_privkey
import shelve


def pairing(code, host):
    privkey = generate_privkey()
    btc_client = BTCPayClient(host=host, pem=privkey)
    btc_token = btc_client.pair_client(code)
    btc_client = BTCPayClient(host=host, pem=privkey, tokens=btc_token)
    with shelve.open('data') as data:
        data['btc_client'] = btc_client
