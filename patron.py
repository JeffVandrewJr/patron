# Copyright (c) 2018 Jeff Vandrew Jr

from app import app, db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}