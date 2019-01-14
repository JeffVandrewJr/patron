<h1>LibrePatron: A Self-Hosted Patreon Alternative Backed by BTCPay</h1>

Copyright (C) 2018-2019 Jeff Vandrew Jr

Latest Stable Release: 0.6.37

Patreon is a popular service that allows content creators to receive contributions from supporters on a recurring basis. Unfortunately, Patreon is also a dedicated enemy of the concept of free speech as an important civic virtue. Patreon is known to arbitarily ban its creators for "thought crime."

Unfortunately most Patreon alternatives to date do not implement all of Patreon's main features, namely:

* Main page to entice new subscribers
* Google Analytics
* Protected page to post updates (viewable by subscribers only)
* Automatic bulk emailing of updates to subscribers
* Managing billing and subscription expiration
* Automatic monthly billing via email
* Support for both Bitcoin (BTCPay Server) and optionally fiat (Square)
* User commenting on updates

Portions of this package rely on a fork of the Flask-Blogging package by Gouthaman Balaraman.

If you're a creator reading this unconcerned with free speech issues, Patreon still takes a percentage of your earnings, which can be avoided by using LibrePatron.

Sample site: https://librepatron.com

Slack Group: https://slack.librepatron.com

<h2>Improvements Roadmap</h2>

1. More granular control over subscription levels.

<h2>Install Method</h2>

A docker-compose is provided that automatically installs LibrePatron along with nginx and obtains SSL certificates, all in a few easy steps (to be executed from `$HOME` directory):

```bash
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/librepatron.env

# open librepatron.env and fill in the necessary info as mentioned in the file comments, and then save
nano librepatron.env

wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/isso.env

# open isso.env and fill in the necessary info as mentioned in the file comments, and then save
nano isso.env

sudo docker network create nginx-net
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/docker-compose.yml
sudo docker-compose up -d
```
Your site will then be launched and operational! 

The first visitor to the site will be prompted to register as administrator. The administrator is the user that posts updates, gets paid, etc. The administrator is the content creator. Setting up everything in the admin panel should be your first step, as the site will not function properly until email and other settings are filled in.

You can upgrade from a prior version by executing the same steps above. Just make sure you delete your old `docker-compose.yml` first. if you're upgrading from a version prior to 0.6.26, you'll need to reset your price levels and email settings from the web interface admin panel, as price levels and emails settings are now set from the web interface rather than a config file. You'll also need the new isso.env file if you're upgrading from a version prior to 0.6.26.

Users get a 5 hour subscription as soon as they pay the BTCPay invoice. That is bumped to 30 days as soon as BTCPay recognizes the payment as "confirmed". BTCPay settings determine how many confirmations are required to make a payment "confirmed."

If you decide to allow fiat payments, after setting up square, it is suggested that you run a [test charge by follwing these instructions](https://github.com/JeffVandrewJr/patron/blob/master/test-charge.md).

<h3>Notes</h3>

You'll note that in the `librepatron.env` file, you must provide a "secret key" of random digits. This is necessary for a variety of reasons. If you don't know how to get one, here is one method:

```python
python3
>>>import os
>>>os.urandom(24).hex()
>>>exit()
```

A random string will be printed to screen that you can then copy and paste.

You'll also need SMTP server info. Gmail is not a good server to use for this purpose. If you need one, here's an example of a service that would work: https://www.easy-smtp.com/
