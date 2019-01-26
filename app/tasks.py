from app import scheduler, db, SCHEDULER_HOUR, SCHEDULER_MINUTE
from app.email import send_reminder_emails, send_failed_emails
from app.models import User, Square, PriceLevel
from datetime import datetime, timedelta
import shelve
from squareconnect.api_client import ApiClient
from squareconnect.apis.transactions_api import TransactionsApi
import uuid

'''
Registers all BTCPay and Square renewal tasks to run daily.
Uses Flask-APScheduler.
'''


@scheduler.task(
    'cron',
    id='do_renewals',
    hour=SCHEDULER_HOUR,
    minute=SCHEDULER_MINUTE,
)
def renewals():
    with shelve.open(scheduler.app.config['SECRET_KEY_LOCATION']) as storage:
        begin = storage['last_renewal']
    renewals_btcpay(begin)
    renewals_square(begin)
    with shelve.open(scheduler.app.config['SECRET_KEY_LOCATION']) as storage:
        storage['last_renewal'] = datetime.today()


def renewals_btcpay(begin):
    tomorrow = datetime.today() + timedelta(hours=24)
    scheduler.app.logger.info('Starting BTCPay renewals')
    with scheduler.app.app_context():
        last_reminder = User.query.filter(
            User.expiration < tomorrow,
            User.expiration > begin,
            User.renew != False,
            User.square_id == None,
            User.role != None,
        ).all()
    six = datetime.today() + timedelta(hours=144)
    four = datetime.today() + timedelta(hours=96)
    with scheduler.app.app_context():
        first_reminder = User.query.filter(
            User.expiration < six,
            User.expiration > four,
            User.renew != False,
            User.square_id == None,
            User.role != None,
        ).all()
    reminder_set = set(last_reminder).union(set(first_reminder))
    send_reminder_emails(scheduler.app, reminder_set)
    scheduler.app.logger.info('Finished BTCPay renewals')


def renewals_square(begin):
    scheduler.app.logger.info('Starting Square renewals')
    tomorrow = datetime.today() + timedelta(hours=24)
    failed_list = []
    declined_list = []
    with scheduler.app.app_context():
        charge_list = User.query.filter(
            User.expiration < tomorrow,
            User.expiration > begin,
            User.square_id != None,
            User.role != None,
        ).all()
        if charge_list:
            square = Square.query.first()
            api_client = ApiClient()
            api_client.configuration.access_token = square.access_token
            transactions_api = TransactionsApi(api_client)
            for user in charge_list:
                idempotency_key = str(uuid.uuid1())
                price_level = PriceLevel.query.filter_by(
                    name=user.role).first()
                if price_level is None:
                    failed_list.append(user)
                    continue
                cents = price_level.price * 100
                amount = {'amount': cents, 'currency': 'USD'}
                body = {
                    'idempotency_key': idempotency_key,
                    'customer_id': user.square_id,
                    'customer_card_id': user.square_card,
                    'amount_money': amount,
                }
                try:
                    charge_response = transactions_api.charge(
                        square.location_id, body
                    )
                except Exception as e:
                    scheduler.app.logger.info(
                        f'{user.username} card declined {e}'
                    )
                    declined_list.append(user)
                    continue
                transaction = charge_response.transaction
                if transaction is None:
                    scheduler.app.logger.info(
                        f'{user.username} card declined'
                    )
                    declined_list.append(user)
                    continue
                elif transaction.id is None:
                    scheduler.app.logger.info(
                        f'{user.username} card declined'
                    )
                    declined_list.append(user)
                    continue
                else:
                    if user.expiration <= datetime.today():
                        base = datetime.today()
                    else:
                        base = user.expiration
                    user.expiration = base + timedelta(days=30)
                    db.session.commit()
    send_failed_emails(
        scheduler.app,
        failed_list=failed_list,
        declined_list=declined_list,
    )
    scheduler.app.logger.info('Square renewals complete')
