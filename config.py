import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BLOGGING_SITENAME = 'Patron'
    BLOGGING_SITEURL = 'https://example.com'
    BLOGGING_URL_PREFIX = None  # but see PROTECTED_BLOGGING_URL_PREFIX
    BLOGGING_BRANDURL = None
    BLOGGING_TWITTER_USERNAME = None
    BLOGGING_DISQUS_SITENAME = None
    BLOGGING_GOOGLE_ANALYTICS = None
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    PROTECTED_BLOGGING_URL_PREFIX = '/updates'
    SECRET_KEY = '085767hsjd83dhddfvjhd74t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
