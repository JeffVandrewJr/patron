from app.models import AdminData
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class InitialConfig(object):
    BLOGGING_SITENAME = 'Patron'
    BLOGGING_SITEURL = 'https://github.com'
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


class SecondConfig(object):
    admin_data = AdminData.query.filter_by(initial_setup=True).first()
    BLOGGING_SITENAME = admin_data.site_name
    BLOGGING_SITEURL = admin_data.site_url
    BLOGGING_URL_PREFIX = None  # but see PROTECTED_BLOGGING_URL_PREFIX
    BLOGGING_BRANDURL = None
    BLOGGING_TWITTER_USERNAME = admin_data.twitter
    BLOGGING_DISQUS_SITENAME = admin_data.disqus
    BLOGGING_GOOGLE_ANALYTICS = admin_data.ga
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    PROTECTED_BLOGGING_URL_PREFIX = '/updates'
    SECRET_KEY = admin_data.csrf_key
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
