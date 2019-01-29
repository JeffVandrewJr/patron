from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os
from os.path import abspath, join
import shelve

basedir = abspath(os.path.dirname(__file__))


class Config(object):
    BLOGGING_SITENAME = os.environ.get('SITENAME') or 'LibrePatron'
    BLOGGING_SITEURL = os.environ.get('SITEURL') or 'https://example.com'
    SERVER_NAME = os.environ.get('VIRTUAL_HOST')
    BLOGGING_URL_PREFIX = '/updates'
    BLOGGING_BRANDURL = os.environ.get('BRANDURL')
    BLOGGING_TWITTER_USERNAME = os.environ.get('TWITTER')
    BLOGGING_GOOGLE_ANALYTICS = None
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    BLOGGING_ESCAPE_MARKDOWN = False
    COMMENTS = False
    COMMENTS_SUBURI = os.environ.get('COMMENTS_SUBURI') is not None
    if COMMENTS_SUBURI:
        COMMENTS_URL = BLOGGING_SITEURL + '/isso'
    else:
        COMMENTS_URL = 'https://comments.' + SERVER_NAME
    PREFERRED_URL_SCHEME = 'https'
    if os.environ.get('SCHEDULER_HOUR') is not None:
        SCHEDULER_HOUR = int(os.environ.get('SCHEDULER_HOUR'))
    else:
        SCHEDULER_HOUR = 9
    if os.environ.get('SCHEDULER_MINUTE') is not None:
        SCHEDULER_MINUTE = int(os.environ.get('SCHEDULER_MINUTE'))
    else:
        SCHEDULER_MINUTE = None
    SECRET_KEY_LOCATION = os.environ.get('SECRET_KEY_LOCATION') or \
        join(basedir, 'key')
    with shelve.open(SECRET_KEY_LOCATION) as key:
        if key.get('key') is None:
            SECRET_KEY = os.urandom(24).hex()
            key['key'] = SECRET_KEY
        else:
            SECRET_KEY = key['key']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + join(basedir, 'app.db')
    SCHEDULER_JOBSTORES = {
            'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
        }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
