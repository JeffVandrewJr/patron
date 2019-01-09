from app import scheduler
from app.email import send_reminder_emails
from app.models import User
from datetime import datetime, timedelta


@scheduler.task(
    'cron',
    id='do_renewals',
    hour=scheduler.app.config.get('SCHEDULER_HOUR'),
    minute=scheduler.app.config.get('SCHEDULER_MINUTE'),
)
def renewals():
    yesterday = datetime.today() - timedelta(hours=24)
    tomorrow = datetime.today() + timedelta(hours=24)
    with scheduler.app.app_context():
        last_reminder = User.query.filter(
            User.expiration < tomorrow,
            User.expiration > yesterday,
            User.square_id == None,
        ).all()
    six = datetime.today() + timedelta(hours=144)
    four = datetime.today() + timedelta(hours=96)
    with scheduler.app.app_context():
        first_reminder = User.query.filter(
            User.expiration < six,
            User.expiration > four,
            User.square_id == None,
        ).all()
    reminder_list = first_reminder + last_reminder
    send_reminder_emails(scheduler.app, reminder_list)
