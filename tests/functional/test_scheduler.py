from flask_ezmail.connection import email_dispatched


def test_scheduler(test_client, new_user):
    messages = []

    @email_dispatched.connect
    def suppressed_mail(message):
        messages.append(message)

    message = messages[0]
    assert message.recipients == [new_user]
