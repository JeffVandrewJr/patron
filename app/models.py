from app import app, db, login, blog_engine
from flask_login import UserMixin, current_user
from flask_principal import identity_loaded, RoleNeed
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash


class BTCPayClientStore(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.PickleType)

    def __repr__(self):
        return f'Pickled BTCPay Client, Id {self.id}'


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    expiration = db.Column(db.DateTime, index=True)
    mail_opt_out = db.Column(db.Boolean, index=True)
    role = db.Column(db.String(64))

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return f'''
                {self.username}, 
                {self.email}, 
                {self.expiration}, 
                {self.role}
                '''

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
@blog_engine.user_loader
def load_user(id):
    return User.query.get(int(id))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    if current_user.role == 'admin':
        identity.provides.add(RoleNeed('admin'))
        identity.provides.add(RoleNeed('blogger'))
    identity.user = current_user
