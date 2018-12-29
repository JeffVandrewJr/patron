# Copyright (c) 2018 Jeff Vandrew Jr

from app import create_app, db, blog_engine
from app.models import User, BTCPayClientStore, SecretKey
from app.pricing import Pricing
from flask_blogging_patron.signals import editor_post_saved
import os

app = create_app()


# set secret key
with app.app_context():
    secret_key = SecretKey.query.first()
    if secret_key is not None:
        app.config['SECRET_KEY'] = secret_key.key
    else:
        app.config['SECRET_KEY'] = os.urandom(24)
        secret_key = SecretKey(key=app.config['SECRET_KEY'])
        db.session.add(secret_key)
        db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,
            'editor_post_saved': editor_post_saved,
            'blog_engine': blog_engine,
            'BTCPayClientStore': BTCPayClientStore,
            'Pricing': Pricing,
           }
