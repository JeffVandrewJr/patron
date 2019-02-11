from flask_ezmail.connection import email_dispatched
from time import sleep


def test_scheduler(test_client, new_user, init_database):
    messages = []

    @email_dispatched.connect
    def suppressed_mail(message):
        messages.append(message)

    sleep(5)
    print('Sleeping 55 more seconds.')
    sleep(55)
    message = messages[0]
    assert message.recipients == [new_user]
