from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_blogging_protected import ProtectedBloggingEngine, ProtectedSQLAStorage
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.principal import Principal, Permission, RoleNeed
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
protected_sql_storage = ProtectedSQLAStorage(db=db)
db.create_all()
protected_blog_engine = ProtectedBloggingEngine(app, protected_sql_storage)
login = LoginManager(app)

# permissions
principals = Principal(app)
admin_permission = Permission(RoleNeed('admin'))

# blueprints
from app.auth import bp as auth_bp
from app.admin import bp as admin_bp
from app.main import bp as main_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(main_bp)

from app import models
