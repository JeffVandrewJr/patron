from app import app
from app.models import User
from app.email import send_reminder_emails
from datetime import datetime, timedelta
from threading import Thread


@app.cli.command()
def send_renewals():
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
    Thread(target=send_reminder_emails, args=(app, reminder_list)).start()
