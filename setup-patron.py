#! /usr/bin/env python3

import app
from app import db
from app.models import AdminData, SupportLevel
from config import SecondConfig
import os

admin_data = AdminData.query.filter_by(initial_setup=True).first()
if admin_data is None:
    admin_data = AdminData()
    admin_data.csrf_key = os.urandom(32)
    setup = 3
    print('You have not yet done admin setup, so this script will do both \
          admin setup and support level setup.')
else:
    setup = None
    while setup != 1 or 2 or 3:
        print('''What do you want to set up? \n
              1. Site Admin Setup\n
              2. Set up pricing\n
              3. Both\n''')
        input('Enter 1, 2, or 3: ')
if setup == 1 or 3:
    admin_data.site_name = input('Enter a title for your site: ')
    admin_data.site_url = input('Enter your site URL (include https://): ')
    admin_data.twitter = input('Enter your Twitter handle: ')
    disqus = input('Do you want Disqus comments on your site? (y/n) ')
    if disqus.lower() == 'y':
        admin_data.disqus = input('Enter your Disqus site name: ')
    else:
        admin_data.disqus = None
    ga = input('Do you want Google Analytics on your site? (y/n) ')
    if ga.lower() == 'y':
        admin_data.ga = input('Enter your Google Analytics Code: ')
    else:
        admin_data.ga = None
    admin_data.initial_setup = True
    db.session.add(admin_data)
    db.session.commit()
if setup == 2 or 3:
    input = ''
    while input.lower() != 'f':
        price_levels = SupportLevel.query.all()
        print('Current Price Packages:\n')
        for price_level in price_levels:
            print(f'''ID: {price_level.id}, \n
                  Name: {price_level.name}, \n
                  Price: {price_level.price}''')
        input = input('[A]dd, [D]elete, or [F]inished? ')
        if input.lower() == 'a':
            price_level = SupportLevel()
            price_level.name = input('Enter a name for the price level: ')
            price_level.description = input('Enter a description (over 600 \
                                            characters will be truncated: ')
            price_level.price = input('Enter a price in USD: ')
            db.session.add(price_level)
            db.session.commit()
            print('Price package accepted.')
        elif input.lower() == 'd':
            to_delete = input('Enter ID of price package to delete: ')
            price_level = SupportLevel.query.filter_by(id=to_delete)
            db.session.delete(price_level)
            db.session.commit()
            print('Price package deleted.')
app.config.from_object(SecondConfig)
