import os
from os.path import abspath, join

basedir = abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN = None
    BLOGGING_SITENAME = os.environ.get('SITENAME') or 'LibrePatron'
    BLOGGING_SITEURL = os.environ.get('SITEURL') or 'https://example.com'
    BLOGGING_URL_PREFIX = '/updates'
    BLOGGING_BRANDURL = os.environ.get('BRANDURL')
    BLOGGING_TWITTER_USERNAME = os.environ.get('TWITTER')
    BLOGGING_DISQUS_SITENAME = os.environ.get('DISQUS')
    BLOGGING_GOOGLE_ANALYTICS = None
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    BLOGGING_ESCAPE_MARKDOWN = False
    MAIL_SERVER = None
    MAIL_PORT = None
    MAIL_USE_TLS = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    PREFERRED_URL_SCHEME = 'https'
    if os.environ.get('SCHEDULER_HOUR') is not None:
        SCHEDULER_HOUR = int(os.environ.get('SCHEDULER_HOUR'))
    else:
        SCHEDULER_HOUR = 9
    if os.environ.get('SCHEDULER_MINUTE') is not None:
        SCHEDULER_MINUTE = int(os.environ.get('SCHEDULER_MINUTE'))
    else:
        SCHEDULER_MINUTE = None
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'placeholder'
    SERVER_NAME = os.environ.get('VIRTUAL_HOST')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
