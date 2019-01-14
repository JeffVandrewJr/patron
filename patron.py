# Copyright (c) 2018 Jeff Vandrew Jr

from app import create_app, db, blog_engine
from app.email import send_reminder_emails
from app.models import User, BTCPayClientStore, PriceLevel, \
        ThirdPartyServices, Email
from app.utils import load_config
from datetime import datetime, timedelta
from flask_blogging_patron.signals import editor_post_saved

app = create_app()
load_config(
    url='http://' + app.config['SERVER_NAME'],
    app=app,
)


if __name__ == '__main__':
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
