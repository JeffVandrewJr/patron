# Copyright (c) 2018 Jeff Vandrew Jr

from app import create_app, db, blog_engine
from app.email import send_reminder_emails
from app.models import User, BTCPayClientStore, SecretKey
from app.pricing import Pricing
from datetime import datetime, date, timedelta
from flask_blogging_patron.signals import editor_post_saved
import os
import shelve

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,
            'editor_post_saved': editor_post_saved,
            'blog_engine': blog_engine,
            'BTCPayClientStore': BTCPayClientStore,
            'Pricing': Pricing,
            'send_reminder_emails': send_reminder_emails,
            'tomorrow': datetime.today() + timedelta(hours=24),
            'yesterday': datetime.today() - timedelta(hours=24),
           }
