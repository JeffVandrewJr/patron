from config import Config
from configparser import ConfigParser
from copy import deepcopy
from datetime import datetime, timedelta
from flask import Flask, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_apscheduler import APScheduler
from flask_blogging_patron import BloggingEngine, SQLAStorage
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_principal import Permission, RoleNeed
from flask_sqlalchemy import SQLAlchemy
import os
import shelve

'''
Unfortunately Flask App factories can't conform to PEP
Codex beauty standards!
'''


VERSION = '0.7.28'

# register extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
global sql_storage
blog_engine = BloggingEngine()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
scheduler = APScheduler()


# register Flask-Admin
class AdminHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', version=VERSION)

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


# this will be needed in the create_app fn later
global temp_bp

# permissions - flask_principal objects created by BloggingEngine
principals = blog_engine.principal
admin_permission = Permission(RoleNeed('admin'))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals['THEME_FILE'] = 'themes/' + \
        app.config['THEME'] + '.min.css'
    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        global sql_storage
        sql_storage = SQLAStorage(db=db)
    migrate.init_app(app, db)
    login.init_app(app)
    admin.init_app(app)
    blog_engine.init_app(app, sql_storage)
    global SCHEDULER_HOUR
    global SCHEDULER_MINUTE
    SCHEDULER_HOUR = app.config.get('SCHEDULER_HOUR')
    SCHEDULER_MINUTE = app.config.get('SCHEDULER_MINUTE')
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
    with shelve.open(app.config['SECRET_KEY_LOCATION']) as storage:
        if storage.get('last_renewal') is None:
            delta = datetime.today().hour - SCHEDULER_HOUR + 24
            storage['last_renewal'] = datetime.today() - timedelta(hours=delta)
            app.logger.info('Dummy last renewal date created.')

    # pre-first request loads
    @app.before_first_request
    def load_ga():
        from app.models import ThirdPartyServices
        ga = ThirdPartyServices.query.filter_by(name='ga').first()
        if ga is not None:
            app.config['BLOGGING_GOOGLE_ANALYTICS'] = ga.code
            app.logger.info('GA configuration success.')

    @app.before_first_request
    def load_theme():
        from app.models import ThirdPartyServices
        theme = ThirdPartyServices.query.filter_by(name='theme').first()
        if theme is not None:
            app.config['THEME'] = theme.code
            app.jinja_env.globals['THEME_FILE'] = 'themes/' + \
                theme.code + '.min.css'
            app.logger.info('Theme configuration success.')

    @app.before_first_request
    def load_tasks():
        from app import tasks
        app.logger.info(f'Next renewal time: \
                {scheduler._scheduler.get_jobs()[0].next_run_time}')

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


    return app


from app import admin_views
from app import models, subscriptions
