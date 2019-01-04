<h1>LibrePatron: A Self-Hosted Patreon Alternative Backed by BTCPay</h1>

Copyright (C) 2018 Jeff Vandrew Jr

Latest Stable Release: 0.1.28

Patreon is a popular service that allows content creators to receive contributions from supporters on a recurring basis. Unfortunately, Patreon is also a dedicated enemy of the concept of free speech as an important civic virtue. Patreon is known to arbitarily ban its creators for "thought crime."

Unfortunately most Patreon alternatives to date do not implement all of Patreon's main features, namely:

* Main page to entice new subscribers
* Google Analytics
* Protected page to post updates (viewable by subscribers only)
* Automatic bulk emailing of updates to subscribers
* Managing billing and subscription expiration
* Automatic monthly billing via email

While still in alpha status, LibrePatron implements all of these features. 

Portions of this package rely on a fork of the Flask-Blogging package by Gouthaman Balaraman.

If you're a creator reading this unconcerned with free speech issues, Patreon still takes a percentage of your earnings, which can be avoided by using LibrePatron.

Sample site: https://librepatron.com

Slack Group: https://slack.librepatron.com

<h2>Improvements Roadmap</h2>

1. Fiat integration. We're not in a 100% Bitcoin world yet (unfortunately). 
2. Easier subscriber export.
3. Allowing subsribers to comment on updates is turned off by default, but is permitted by entering Disqus information in the configuration file. If turning this feature on is popular, factoring out Disqus could be a long term improvement.
4. More granular control over subscription levels.
5. Move pricing configuration into web interface admin panel.

Easy install is below, or if you prefer you can do it the [hard way](https://github.com/JeffVandrewJr/patron/blob/master/manual-install.md).

<h2>Easy Install Method</h2>

A docker-compose is provided that automatically installs LibrePatron along with nginx and obtains SSL certificates, all in a few easy steps (to be executed from `$HOME` directory):

```bash
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/librepatron.env

# open librepatron.env and fill in the necessary info as mentioned in the file comments, and then save
nano librepatron.env

mkdir pricing
cd pricing
wget -O pricing.yaml https://raw.githubusercontent.com/JeffVandrewJr/patron/master/pricing.yaml.sample

# open pricing.yaml, enter your subscription plans, and then save it
nano pricing.yaml

cd ..
sudo docker network create nginx-net
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/docker-compose.yml
sudo docker-compose up -d
```
Your site will then be launched and operational!

Users get a one day subscription as soon as they pay the BTCPay invoice. That is bumped to 30 days as soon as BTCPay recognizes the payment as "confirmed". BTCPay settings determine how many confirmations are required to make a payment "confirmed."

The first visitor to the site will be prompted to register as administrator. The administrator is the user that posts updates, gets paid, etc. The administrator is the content creator.

After registering as administrator, be sure to first make a "homepage" post. A "homepage" post does not appear on your updates, but sets the text for the main page that all visitors (subscribed or not) can view. Then you can add some updates.

Before letting people know about your site, be sure to click "Admin Panel" to pair your site to your BTCPay server!

<h3>Notes</h3>

If you don't use the official Docker image and instead choose to install from source, LibrePatron will fail in sending email reminders if your server doesn't have a validly set timezone. This is because LibrePatron depends on the APScheduler library, which needs a set timezone at all times. The Docker image takes care of this for you by setting a timezone in the container.

You'll note that during setup, you must provide a "secret code" of random digits. This is necessary for a variety of reasons. If you don't know how to get one, here is one method:

```python
python3
>>>import os
>>>os.urandom(24).hex()
>>>exit()
```

A random string will be printed to screen that you can then copy and paste.

You'll also need SMTP server info. Gmail is not a good server to use for this purpose. If you need one, here's an example of a service that would work: https://www.easy-smtp.com/
