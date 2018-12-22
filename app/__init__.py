from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_blogging import SQLAStorage, BloggingEngine
from sqlalchemy import create_engine, MetaData
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

# extensions
bootstrap = Bootstrap(app)
engine = create_engine('sqlite:///patron.db')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=engine)

from app import routes
