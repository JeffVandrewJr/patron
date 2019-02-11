from datetime import datetime


def test_new_user(new_user):
    '''
    GIVEN a User model
    WHEN new User is created
    THEN check the email, hashed pass, authentication
    expiration, password reset
    '''
    assert new_user.username == 'test'
    assert new_user.email == 'test@test.com'
    assert datetime.today() > new_user.expiration
    assert new_user.check_password('test')
    assert new_user.role == 'Patron'
    assert not new_user.mail_opt_out
