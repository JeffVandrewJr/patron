import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BLOGGING_SITENAME = 'Patron'
    BLOGGING_SITEURL = 'https://github.com'
    BLOGGING_BRANDURL = None
    BLOGGING_TWITTER_USERNAME = '@twitter'
    BLOGGING_DISQUS_SITENAME = None
    BLOGGING_GOOGLE_ANALYTICS = None
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '085767hsjd83dhddfvjhd74t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
