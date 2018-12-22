from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_blogging import SQLAStorage, BloggingEngine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
sql_storage = SQLAStorage(db=db)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)

from app import routes, models
