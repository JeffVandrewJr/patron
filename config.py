import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BLOGGING_SITENAME = os.environ.get('SITENAME') or 'Patron'
    BLOGGING_SITEURL = os.environ.get('SITEURL') or 'https://example.com'
    BLOGGING_URL_PREFIX = None  # but see PROTECTED_BLOGGING_URL_PREFIX
    BLOGGING_BRANDURL = os.environ.get('BRANDURL')
    BLOGGING_TWITTER_USERNAME = os.environ.get('TWITTER')
    BLOGGING_DISQUS_SITENAME = os.environ.get('DISQUS')
    BLOGGING_GOOGLE_ANALYTICS = os.environ.get('GOOGLE_ANALYTICS')
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    PROTECTED_BLOGGING_URL_PREFIX = '/updates'
    SECRET_KEY = os.environ.get('SECRET_KEY') or '085767hsjd83dhddfvjhd74t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
