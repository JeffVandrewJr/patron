from app import app, mail
from flask import render_template
from flask_mail import Message
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        'Password Reset',
        sender=app.config['ADMIN'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt',
                                  user=user, token=token)
    )
