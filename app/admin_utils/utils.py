from app.models import ThirdPartyServices
from configparser import ConfigParser
from flask import current_app
import os


def isso_config():
    file = '/var/lib/config/isso.cfg'
    if os.path.isfile(file):
        os.remove(file)
    isso_pass = ThirdPartyServices.query.filter_by(
        name='isso').first().code
    isso_config = ConfigParser()
    isso_config['general'] = {}
    isso_config['general']['dbpath'] = '/var/lib/db/comments.db'
    isso_config['general']['host'] = current_app.config['BLOGGING_SITEURL']
    isso_config['admin']['enabled'] = 'true'
    isso_config['admin']['password'] = isso_pass
    with open(file, 'w') as configfile:
        isso_config.write(configfile)
