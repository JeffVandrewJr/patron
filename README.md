<h1>LibrePatron: A Self-Hosted Patreon Alternative Backed by BTCPay</h1>

Copyright (C) 2018-2019 Jeff Vandrew Jr

Latest Stable Release: 0.7.35

Patreon is a popular service that allows content creators to receive contributions from supporters on a recurring basis. Unfortunately, Patreon is also a dedicated enemy of the concept of free speech as an important civic virtue. Patreon is known to arbitrarily ban its creators for "thought crime."

Unfortunately most Patreon alternatives to date do not implement all of Patreon's main features, namely:

* Support for both Bitcoin (BTCPay Server) and optionally credit cards (Square)
* Main page to entice new subscribers
* Google Analytics
* Protected page to post updates (viewable by subscribers only)
* Automatic bulk emailing of updates to subscribers
* Managing billing and subscription expiration
* Automatic monthly billing via email
* User commenting on updates
* 21 themes and color schemes to choose from

Portions of this package rely on a fork of the Flask-Blogging package by Gouthaman Balaraman.

If you're a creator reading this unconcerned with free speech issues, Patreon still takes a percentage of your earnings, which can be avoided by using LibrePatron.

Sample site: https://librepatron.com

Slack Group: http://slack.librepatron.com

<h2>Improvements Roadmap</h2>

1. More granular control over subscription levels.
2. Right now, user comments only show when you click on an inidividual creator update in the "Updates" list. This should be improves so there is an indicator that a post has user comments even before it is clicked.

<h2>Easy Install</h2>

You first need a BTCPay installation. If you have not yet installed BTCPay, [here](https://docs.btcpayserver.org/deployment/lunanodewebdeployment) are instructions to get BTCPay set up.

You can also find an illustrated version of these instructions [here](https://blog.btcpayserver.org/librepatron-patreon-alternative/).

If you set up BTCPay using the one-click LunaNode install (or any dockerized install of BTCPay), to set up LibrePatron you would simply SSH into your LunaNode [(click here if you forgot how to do that)](https://github.com/JeffVandrewJr/patron/blob/master/ssh.md), and then:
```bash
# change to root; do not forget the trailing hyphen
sudo su -

cd btcpayserver-docker

export BTCPAYGEN_ADDITIONAL_FRAGMENTS="$BTCPAYGEN_ADDITIONAL_FRAGMENTS;opt-add-librepatron"

# replace example.com with the domain where you want to host LibrePatron
export LIBREPATRON_HOST="example.com"

. btcpay-setup.sh -i
```

That's it! You would replace `example.com` with the domain where you wish to host LibrePatron. Also make sure that domain points to the same IP address as the domain you use for BTCPay. (This would be set with your domain host: GoDaddy, NameCheap, etc).

You only ever need to do that setup once, as from then on LibrePatron will update alongside BTCPay.

If you didn't use the LunaNode one-click install, the same instructions above apply so long as you're using the dockerized version of BTCPay.

If you wish to install separately from BTCPay for whatever reason, see the alternate instructions in the 'alternate_install' directory.

In the future, you can upgrade by simply upgrading BTCPay; LibrePatron will upgrade right alongside it. Just log into BTCPay through the web, then go to Server Settings --> Maintenance --> Update.

IMPORTANT: Before advertising your site, see the section on post-install setup below.

<h2>Post-Install Setup</h2>

The first visitor to the site will be prompted to register as administrator. The administrator is the user that posts updates, gets paid, etc. The administrator is the content creator.

Heading to the admin panel should be your first step after registering as the admin, as the site will not function properly until email and BTCPay Server settings are filled in. Square settings for accepting fiat are optional, as are the settings for Google Analytics and user comments. BTCPay pairing and email setup are mandatory, and your site will malfunction without them.

You'll need SMTP server info for the email section. Gmail, Yahoo, etc are not good servers to use for this purpose, as they block bulk emails. If you don't have SMTP settings to use, here's an example of an easy to use service that would work: https://www.easy-smtp.com/ (free for 10,000 emails per month).

Your users will get a 5 hour subscription as soon as they pay their BTCPay invoice. That is bumped to 30 days as soon as BTCPay recognizes the payment as "confirmed". BTCPay settings determine how many confirmations are required to make a payment "confirmed."

If you decide to allow fiat payments, after setting up square, it is suggested that you run a [test charge by follwing these instructions](https://github.com/JeffVandrewJr/patron/blob/master/test-charge.md).

<h2>Development</h2>

See [DEVELOPMENT.md](DEVELOPMENT.md) for instructions on how to run a local development copy and how to contribute code.
