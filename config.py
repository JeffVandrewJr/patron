import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN = os.environ.get('EMAIL') or 'email@domain.com'
    BLOGGING_SITENAME = os.environ.get('SITENAME') or 'Patron'
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
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY') or '085767hsjd83dhddfvjhd74t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
