from config import Config
from copy import deepcopy
from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_apscheduler import APScheduler
from flask_blogging_patron import BloggingEngine, SQLAStorage
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_principal import Permission, RoleNeed
from flask_sqlalchemy import SQLAlchemy


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

    # pre-first request loads
    @app.before_first_request
    def load_ga():
        from app.models import ThirdPartyServices
        ga = ThirdPartyServices.query.filter_by(name='ga').first()
        if ga is not None:
            app.config['BLOGGING_GOOGLE_ANALYTICS'] = ga.code


    @app.before_first_request
    def load_mail():
        from app.models import Email
        email = Email.query.first()
        if email is not None:
            app.config['ADMIN'] = email.outgoing_email
            app.config['MAIL_SERVER'] = email.server
            app.config['MAIL_PORT'] = email.port
            app.config['MAIL_USERNAME'] = email.username
            app.config['MAIL_PASSWORD'] = email.password
            mail.init_app(app)


    # tasks
    from app import tasks

    return app


from app import admin_views
from app import models, subscriptions
