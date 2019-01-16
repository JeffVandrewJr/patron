from config import Config
from configparser import ConfigParser
from copy import deepcopy
from flask import Flask, redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_apscheduler import APScheduler
from flask_blogging_patron import BloggingEngine, SQLAStorage
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_principal import Permission, RoleNeed
from flask_sqlalchemy import SQLAlchemy
import os


# extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
global sql_storage
blog_engine = BloggingEngine()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
mail = Mail()
scheduler = APScheduler()

#admin setup
class AdminHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and \
                current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


admin = Admin(
    name='LibrePatron Admin',
    template_mode='bootstrap3',
    index_view=AdminHomeView(),
)


# global
global temp_bp

# permissions - flask_principal objects created by BloggingEngine
principals = blog_engine.principal
admin_permission = Permission(RoleNeed('admin'))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        global sql_storage
        sql_storage = SQLAStorage(db=db)
    migrate.init_app(app, db)
    login.init_app(app)
    admin.init_app(app)
    blog_engine.init_app(app, sql_storage)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # deepcopy auto-generated flask_blogging bp, then delete it
    global temp_bp
    temp_bp = deepcopy(app.blueprints['blogging'])
    del app.blueprints['blogging']

    # blueprints
    from app.admin_utils import bp as admin_utils_bp
    from app.api import bp as api_bp
    from app.auth import bp as auth_bp
    from app.blogging import bp as blogging_bp
    from app.main import bp as main_bp
    app.register_blueprint(admin_utils_bp, url_prefix='/admin_utils')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(
        blogging_bp,
        url_prefix=app.config.get('BLOGGING_URL_PREFIX')
    )
    app.register_blueprint(main_bp)

    import logging
    from logging import StreamHandler
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)

    # pre-first request loads
    @app.before_first_request
    def load_ga():
        from app.models import ThirdPartyServices
        ga = ThirdPartyServices.query.filter_by(name='ga').first()
        if ga is not None:
            app.config['BLOGGING_GOOGLE_ANALYTICS'] = ga.code
        app.logger.info('GA configuration success.')


    @app.before_first_request
    def load_isso():
        from app.models import ThirdPartyServices
        isso = ThirdPartyServices.query.filter_by(name='isso').first()
        if isso is not None:
            app.config['COMMENTS'] = True
        else:
            file = '/var/lib/config/isso.cfg'
            if not os.path.isfile(file):
                isso_config = ConfigParser()
                isso_config['default'] = {}
                isso_config['default']['dbpath'] = \
                        'var/lib/db/comments.db'
                isso_config['default']['host'] = \
                        'http://localhost:5000/'
                with open(file, 'w') as configfile:
                    isso_config.write(configfile)
        app.logger.info('Isso configuration success.')


    @app.before_first_request
    def load_mail():
        from app.models import Email
        email = Email.query.first()
        if email is not None:
            app.config['ADMIN'] = email.outgoing_email
            app.config['MAIL_DEFAULT_SENDER'] = email.outgoing_email
            app.config['MAIL_SERVER'] = email.server
            app.config['MAIL_PORT'] = email.port
            app.config['MAIL_USERNAME'] = email.username
            app.config['MAIL_PASSWORD'] = email.password
            mail.server = email.server
            mail.username = email.username
            mail.password = email.password
            if email.port is not None:
                mail.port = int(email.port)
            if app.debut is not None:
                mail.debug = int(app.debug)
            mail.use_tls = True
            mail.use_ssl = False
            mail.default_sender = email.outgoing_email
            mail.max_emails = None
            mail.suppress = False
            mail.fail_silently = True
            mail.app = app
            app.extensions = getattr(app, 'extensions', {})
            app.extensions['mail'] = mail
        else:
            email = Email()
            db.session.add(email)
            db.session.commit()
        app.logger.info('Mail configuration success.')


    # tasks
    from app import tasks
    
    return app


from app import admin_views
from app import models, subscriptions
