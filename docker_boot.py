import os
import requests
import threading
import time


def load_config():
    def start_loop():
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
    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == '__main__':
    load_config()
