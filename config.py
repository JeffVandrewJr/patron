import os
from os.path import normpath, abspath, join

basedir = abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN = os.environ.get('EMAIL')
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
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    if os.environ.get('MAIL_PORT') is not None:
        MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SCHEDULER_HOUR = os.environ.get('SCHEDULER_HOUR') or 9
    SCHEDULER_MINUTE= os.environ.get('SCHEDULER_MINUTE')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'placeholder'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME='127.0.0.1'
