import os
import requests
import time

'''
Some configuration options are loaded from the database,
however the database cannot be loaded until after Flask app creation.
Therefore, some config has to be done by registering the config
functions with @app.before_first_request decorator in the app
factory. The script in this file will continually make GET requests
to LibrePatron until it gets a valid 200 response when a Docker
container boots. This will force those config functions to load upon boot.
'''


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
