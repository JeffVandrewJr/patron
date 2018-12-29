from app import scheduler
from app.email import send_reminder_emails
from app.models import User
from datetime import datetime, timedelta


@scheduler.task('cron', id='renewals', hour=9)
def renewals():
    yesterday = datetime.today() - timedelta(hours=24)
    tomorrow = datetime.today() + timedelta(hours=24)
    last_reminder = User.query.filter_by(
        expiration < tomorrow,
        expiration > yesterday
    ).all()
    six = datetime.today() + timedelta(hours=144)
    four = datetime.today() + timedelta(hours=96)
    first_reminder = User.query.filter_by(
        expiration < six,
        expiration > four
    ).all()
    reminder_list = first_reminder + last_reminder
    send_reminder_emails(scheduler.app, reminder_list)
