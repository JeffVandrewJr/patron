from app import db, login, protected_blog_engine
from flask_login import UserMixin, current_user
from flask_principal import identity_loaded, RoleNeed
from werkzeug.security import generate_password_hash, check_password_hash


class AdminData(db.model):
    id = db.Column(db.Integer, primary_key=True)
    initial_setup = (db.Boolean)
    site_name = db.Column(db.String(128))
    site_url = db.Column(db.String(128))
    twitter = db.Column(db.String(64))
    disqus = db.Column(db.String(64))
    ga = db.Column(db.String(128))
    csrf_key = db.Column(db.String(128))


class SupportLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Price Level {self.name}>'


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    expiration = db.Column(db.DateTime, index=True)
    role = db.Column(db.String(64))

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return f'{self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
@protected_blog_engine.user_loader
def load_user(id):
    return User.query.get(int(id))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    if current_user.role == 'admin':
        identity.provides.add(RoleNeed('admin'))
        identity.provides.add(RoleNeed('blogger'))
    identity.user = current_user
