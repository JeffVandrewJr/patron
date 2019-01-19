<h1>LibrePatron: A Self-Hosted Patreon Alternative Backed by BTCPay</h1>

Copyright (C) 2018-2019 Jeff Vandrew Jr

Latest Stable Release: 0.6.62

Patreon is a popular service that allows content creators to receive contributions from supporters on a recurring basis. Unfortunately, Patreon is also a dedicated enemy of the concept of free speech as an important civic virtue. Patreon is known to arbitarily ban its creators for "thought crime."

Unfortunately most Patreon alternatives to date do not implement all of Patreon's main features, namely:

* Support for both Bitcoin (BTCPay Server) and optionally fiat (Square)
* Main page to entice new subscribers
* Google Analytics
* Protected page to post updates (viewable by subscribers only)
* Automatic bulk emailing of updates to subscribers
* Managing billing and subscription expiration
* Automatic monthly billing via email
* User commenting on updates

Portions of this package rely on a fork of the Flask-Blogging package by Gouthaman Balaraman.

If you're a creator reading this unconcerned with free speech issues, Patreon still takes a percentage of your earnings, which can be avoided by using LibrePatron.

Sample site: https://librepatron.com

Slack Group: https://slack.librepatron.com

<h2>Improvements Roadmap</h2>

1. More granular control over subscription levels.

<h2>Easy LunaNode Installer</h2>

If you installed BTCPay via LunaNode one-click installer, you can also install LibrePatron with a single extra command! This method will also work on any non-LunaNode BTCPay-Docker install so long as the source files are at `/root/btcpayserver-docker/`.

Before installing, don't forget to point your domain to your LunaNode's IP address. (You perform this step with your domain registrar: GoDaddy, NameCheap, etc.) You must point both the main domain and the `comments` subdomain. So if you're hosting LibrePatron at `example.com`, both `example.com` and `comments.example.com` must point to your LunaNode's IP address.

You would simply SSH into your LunaNode [(click here if you forgot how to do that)](https://github.com/JeffVandrewJr/patron/blob/master/ssh.md), and then:
```bash
# change to root; do not forget the trailing hyphen
sudo su -

# download the installer
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/luna-installer.sh
chmod +x luna-installer.sh

# run the installer, replace example.com and email@mail.com with your domain name and email
./luna-installer.sh example.com email@mail.com
```

That's it! On the final line, you would replace `example.com` with the domain where you wish to host LibrePatron, and you would replace `email@email.com` with a valid email address.

In the future, you can upgrade by simply re-running the installer. The installer automatically installs the latest stable version.

IMPORTANT: Before advertising your site, see the section on post-install setup below.

<h2>Alternate Install via Docker-Compose</h2>

If you're not using the installer script above, a docker-compose is provided that automatically installs LibrePatron along with nginx and obtains SSL certificates. You would only need this if you're not using the LunaNode instructions above. Instructions for said alternate install can be obtained by clicking [here](https://github.com/JeffVandrewJr/patron/blob/master/alternate-install-docker.md).

<h2>Post-Install Setup</h2>

The first visitor to the site will be prompted to register as administrator. The administrator is the user that posts updates, gets paid, etc. The administrator is the content creator. Heading to the admin panel should be your first step after registering as the admin, as the site will not function properly until email and BTCPay Server settings are filled in. Square settings for accepting fiat are optional, as are the settings for Google Analytics and user comments. BTCPay pairing and email setup are mandatory, and your site will malfunction without them.

You'll need SMTP server info for the email section. Gmail, Yahoo, etc are not good servers to use for this purpose, as they block bulk emails. If you don't have SMTP settings to use, here's an example of an easy to use service that would work: https://www.easy-smtp.com/

Your users will get a 5 hour subscription as soon as they pay their BTCPay invoice. That is bumped to 30 days as soon as BTCPay recognizes the payment as "confirmed". BTCPay settings determine how many confirmations are required to make a payment "confirmed."

If you decide to allow fiat payments, after setting up square, it is suggested that you run a [test charge by follwing these instructions](https://github.com/JeffVandrewJr/patron/blob/master/test-charge.md).
