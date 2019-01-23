from app.models import ThirdPartyServices
from configparser import ConfigParser
from flask import current_app


def isso_config():
    # isso requires a config file
    # this function writes a config file in isso format
    # file is saved in a Docker volume shared between lp and isso
    file = '/var/lib/config/isso.cfg'
    isso_pass = ThirdPartyServices.query.filter_by(
        name='isso').first().code
    isso_config = ConfigParser()
    isso_config['general'] = {}
    isso_config['general']['dbpath'] = '/var/lib/db/comments.db'
    isso_config['general']['host'] = current_app.config['BLOGGING_SITEURL']
    isso_config['admin'] = {}
    isso_config['admin']['enabled'] = 'true'
    isso_config['admin']['password'] = isso_pass
    isso_config['guard'] = {}
    isso_config['guard']['ratelimit'] = '50'
    isso_config['guard']['direct-reply'] = '100'
    with open(file, 'w') as configfile:
        isso_config.write(configfile)
