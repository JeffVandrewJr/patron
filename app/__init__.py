from config import Config
from copy import deepcopy
from flask import Flask
from flask_blogging_patron import BloggingEngine, SQLAStorage
from flask_blogging_patron.signals import editor_post_saved
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_principal import Permission, RoleNeed
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)

# extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
sql_storage = SQLAStorage(db=db)
db.create_all()
blog_engine = BloggingEngine(app, sql_storage)
login = LoginManager(app)
mail = Mail(app)

# permissions - flask_principal objects created by BloggingEngine
principals = blog_engine.principal
admin_permission = Permission(RoleNeed('admin'))

# deepcopy auto-generated flask_blogging bp, then delete it
temp_bp = deepcopy(app.blueprints['blogging'])
del app.blueprints['blogging']

# blueprints
from app.api import bp as api_bp
from app.auth import bp as auth_bp
from app.admin import bp as admin_bp
from app.blogging import bp as blogging_bp
from app.main import bp as main_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(blogging_bp, url_prefix=app.config.get('BLOGGING_URL_PREFIX')) 
app.register_blueprint(main_bp)

# subscribe to new post signal from blog_engine
from app.email import email_post
@editor_post_saved.connect
def email(sender, post_id):
    email_post(post_id)

from app import models
