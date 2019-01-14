import os
import requests
import time


def load_config():
    while True:
        try:
            r = requests.get(
                'https://' + os.environ.get('VIRTUAL_HOST')
            )
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(2)


if __name__ == '__main__':
    load_config()
