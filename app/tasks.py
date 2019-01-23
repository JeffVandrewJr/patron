from app import scheduler, db, SCHEDULER_HOUR, SCHEDULER_MINUTE
from app.email import send_reminder_emails, send_failed_emails
from app.models import User, Square, PriceLevel
from datetime import datetime, timedelta
from flask import current_app
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
    scheduler.app.logger.info('Starting BTCPay renewals')
    yesterday = datetime.today() - timedelta(hours=24)
    tomorrow = datetime.today() + timedelta(hours=24)
    with scheduler.app.app_context():
        last_reminder = User.query.filter(
            User.expiration < tomorrow,
            User.expiration > yesterday,
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
    reminder_list = first_reminder + last_reminder
    send_reminder_emails(scheduler.app, reminder_list)
    scheduler.app.logger.info('Finished BTCPay renewals')


@scheduler.task(
    'cron',
    id='do_renewals_square',
    hour=SCHEDULER_HOUR,
    minute=SCHEDULER_MINUTE,
)
def renewals_square():
    scheduler.app.logger.info('Starting Square renewals')
    yesterday = datetime.today() - timedelta(hours=24)
    tomorrow = datetime.today() + timedelta(hours=24)
    failed_list = []
    declined_list = []
    with scheduler.app.app_context():
        list = User.query.filter(
            User.expiration < tomorrow,
            User.expiration > yesterday,
            User.square_id != None,
            User.role != None,
        ).all()
        if list != []:
            square = Square.query.first()
            api_client = ApiClient()
            api_client.configuration.access_token = square.access_token
            transactions_api = TransactionsApi(api_client)
            for user in list:
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
