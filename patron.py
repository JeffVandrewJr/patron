# Copyright (c) 2018 Jeff Vandrew Jr

from app import app, db, blog_engine
from app.models import User
from flask_blogging_patron.signals import editor_post_saved


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 
            'editor_post_saved': editor_post_saved,
            'blog_engine': blog_engine}
