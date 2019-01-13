from app.models import Email, User, ThirdPartyServices
from configparser import ConfigParser
from flask import current_app
import os


def isso_config():
    file = '/var/lib/config/isso.cfg'
    if os.path.isfile(file):
        os.remove(file)
    email = Email.query.first()
    isso_pass = ThirdPartyServices.query.filter_by(
        name='isso').first().code
    isso_config = ConfigParser()
    isso_config['general'] = {}
    isso_config['general']['dbpath'] = '/var/lib/db/comments.db'
    isso_config['general']['host'] = current_app.config['SERVER_NAME']
    isso_config['general']['notify'] = 'smtp'
    isso_config['general']['log-file'] = 'var/lib/db/moderation-queue.txt'
    isso_config['admin'] = {}
    isso_config['admin']['enabled'] = 'true'
    isso_config['admin']['password'] = isso_pass
    isso_config['moderation'] = {}
    isso_config['moderation']['enabled'] = 'true'
    isso_config['smtp'] = {}
    isso_config['smtp']['username'] = email.username
    isso_config['smtp']['password'] = email.password
    isso_config['smtp']['host'] = email.server
    isso_config['smtp']['port'] = email.port
    isso_config['smtp']['security'] = 'starttls'
    isso_config['smtp']['to'] = User.query.filter_by(
        role='admin').first().email
    isso_config['smtp']['from'] = email.outgoing_email
    isso_config['guard'] = {}
    isso_config['guard']['enabled'] = 'true'
    with open(file, 'w') as configfile:
        isso_config.write(configfile)
