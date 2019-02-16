from app import create_app, db
from app.models import User, PriceLevel, Email
from tests.tconfig import Config
from datetime import datetime, timedelta
import pytest


@pytest.fixture(scope='module')
def new_user():
    user = User(
        username='test',
        email='test@test.com',
        expiration=(datetime.today() - timedelta(hours=24)),
        renew=True,
        role='Patron',
        mail_opt_out=False
    )
    user.set_password('test')
    return user


@pytest.fixture(scope='session')
def test_client():
    app = create_app(config_class=Config)
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def test_mail():
    mail = Email(
            server='junk',
            username='junk',
            password='junk',
            default_sender='junk@junk.com',
            use_tls=True,
            port=587,
            suppress=True
            )
    return mail


@pytest.fixture(scope='function')
def init_database(new_user, test_mail):
    db.drop_all()
    db.create_all()
    db.session.add(new_user)
    db.session.add(test_mail)
    level_1 = PriceLevel(
        name='Patron',
        description="You're a patron!",
        price=10,
    )
    level_2 = PriceLevel(
        name='Cooler Patron',
        description="You're a cooler patron!",
        price=20,
    )
    level_3 = PriceLevel(
        name='Coolest Patron',
        description="You're the best!",
        price=60,
    )
    db.session.add(level_1)
    db.session.add(level_2)
    db.session.add(level_3)
    db.session.commit()
    yield db
    db.drop_all()
