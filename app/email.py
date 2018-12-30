from app import mail
from app.models import User
from datetime import datetime
from flask import render_template, current_app, url_for
from flask_mail import Message
import logging
from markdown import Markdown
from threading import Thread
from urllib.parse import urlencode


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_async_bulkmail(app, msg, users):
    with app.app_context():
        try:
            with mail.connect() as conn:
                for user in users:
                    if user.expiration <= datetime.today():
                        break
                    msg.recipients = [user.email]
                    conn.send(msg)
        except Exception:
            logging.exception('Exception in send_async_bulkmail')
            raise


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)).start()


def send_reminder_emails(app, reminder_list):
    with app.app_context():
        try:
            site = app.config['BLOGGING_SITENAME']
            with mail.connect() as conn:
                for user in reminder_list:
                    dict = {}
                    dict['username'] = user.username
                    params = urlencode(dict)
                    url = str(url_for('main.create_invoice'))\
                        + '?' + str(params)
                    expires = user.expiration.date()
                    msg = Message(
                        f'{site} Renewal',
                        sender=app.config.get('ADMIN'),
                        recipients=[user.email],
                        body=render_template(
                            'email/reminder.txt',
                            site=site,
                            user=user,
                            url=url,
                            expires=expires,
                        ),
                        html=None
                    )
                    conn.send(msg)
        except Exception:
            logging.exception('Exception in send_reminder_emails')
            raise


def send_bulkmail(subject, sender, users, text_body, html_body):
    msg = Message(subject, sender=sender)
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_bulkmail,
        args=(current_app._get_current_object(), msg, users)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        'Password Reset',
        sender=current_app.config['ADMIN'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt',
                                  user=user, token=token),
        html_body=None
    )


def email_post(post):
    try:
        markdown = Markdown()
        post['rendered_text'] = markdown.convert(post['text'])
        html_body = render_template(
            'email/email_post.html',
            post=post,
        )
        text_body = render_template(
            'email/email_post.txt',
            post=post,
        )
        site = current_app.config.get('BLOGGING_SITENAME')
        users = User.query.filter_by(mail_opt_out=False).all()
        send_bulkmail(
            f'New Update from {site}',
            sender=current_app.config.get('ADMIN'),
            users=users,
            html_body=html_body,
            text_body=text_body
        )
    except Exception:
        logging.exception('Exception in email_post')
        raise
