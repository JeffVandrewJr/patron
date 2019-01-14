# Copyright (c) 2018 Jeff Vandrew Jr

from app import create_app, db, blog_engine
from app.email import send_reminder_emails
from app.models import User, BTCPayClientStore, PriceLevel, \
        ThirdPartyServices, Email
from datetime import datetime, timedelta
from flask_blogging_patron.signals import editor_post_saved
import requests
import threading
import time

app = create_app()


def load_config():
    def start_loop():
        url = 'https://' + str(app.config['SERVER_NAME'])
        while True:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    app.logger.info('Config successfully loaded.')
                    break
                else:
                    app.config.info('Waiting to load config.')
            except Exception:
                app.logger.info('Waiting for site to load.')
            time.sleep(2)
    thread = threading.Thread(target=start_loop)
    thread.start


load_config()


if __name__ == '__main__':
    load_config()
    app.run(load_dotenv=True, ssl_context='adhoc')


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 'User': User,
        'editor_post_saved': editor_post_saved,
        'blog_engine': blog_engine,
        'Email': Email,
        'ThirdPartyServices': ThirdPartyServices,
        'BTCPayClientStore': BTCPayClientStore,
        'PriceLevel': PriceLevel,
        'send_reminder_emails': send_reminder_emails,
        'tomorrow': datetime.today() + timedelta(hours=24),
        'yesterday': datetime.today() - timedelta(hours=24),
    }
