from flask_ezmail.connection import email_dispatched
from time import sleep


def test_scheduler(test_client, new_user, init_database):
    messages = []

    @email_dispatched.connect
    def suppressed_mail(message):
        messages.append(message)

    test_client.get('/')
    sleep(65)
    message = messages[0]
    assert message.recipients == [new_user.email]
