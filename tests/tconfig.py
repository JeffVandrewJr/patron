import os
from os.path import normpath, abspath, join

basedir = abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN = 'test@test.com'
    BLOGGING_SITENAME = os.environ.get('SITENAME') or 'LibrePatron'
    BLOGGING_SITEURL = os.environ.get('SITEURL') or 'https://example.com'
    BLOGGING_URL_PREFIX = '/updates'
    BLOGGING_BRANDURL = os.environ.get('BRANDURL')
    BLOGGING_TWITTER_USERNAME = os.environ.get('TWITTER')
    BLOGGING_DISQUS_SITENAME = os.environ.get('DISQUS')
    BLOGGING_GOOGLE_ANALYTICS = os.environ.get('GOOGLE_ANALYTICS')
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    BLOGGING_ESCAPE_MARKDOWN = False
    MAIL_SERVER = 'ssrs.reachmail.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'example@example.com'
    MAIL_PASSWORD = 'password'
    PREFERRED_URL_SCHEME = 'https'
    SCHEDULER_HOUR = 9
    SCHEDULER_MINUTE= None
    SECRET_KEY = 'a-very-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = 'librepatron.com'
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRF_ENABLED = False
