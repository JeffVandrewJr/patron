from app import create_app, db
from app.models import User
from tests.tconfig import Config
from datetime import datetime, timedelta
import pytest


@pytest.fixture(scope='module')
def new_user():
    user = User(
        username='test',
        email='test@test.com',
        expiration=(datetime.today() - timedelta(hours=24)),
        mail_opt_out=False
    )
    user.set_password('test')
    return user


@pytest.fixture(scope='module')
def test_client():
    app = create_app(config_class=Config)
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def init_database(new_user):
    db.create_all()
    db.session.add(new_user)
    db.session.commit()
    yield db
    db.drop_all()
