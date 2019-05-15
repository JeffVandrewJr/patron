<h2>Alternate Install via Docker-Compose</h2>

If you're not using the installer script mentioned in the README [(click here to see the README)](https://github.com/JeffVandrewJr/patron/blob/master/README.md), a docker-compose is provided that automatically installs LibrePatron along with nginx and obtains SSL certificates. You do not need to do anything in this section if you used the LunaNode installer. 

Before installing, don't forget to point your domain's DNS to your server's address. (You perform this step with your domain registrar: GoDaddy, NameCheap, etc.) You must point both the main domain and the `comments` subdomain. So if you're hosting LibrePatron at `example.com`, both `example.com` and `comments.example.com` must point to your server address. Here are the steps (to be executed from `$HOME` directory):

```bash
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/alternate_install/librepatron.env

# open librepatron.env and fill in the necessary info as mentioned in the file comments, and then save
nano librepatron.env

wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/alternate_install/isso.env

# open isso.env and fill in the necessary info as mentioned in the file comments, and then save
nano isso.env

sudo docker network create nginx-net
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/docker-compose.yml
sudo docker-compose up -d
```
Your site will then be launched and operational! You can upgrade from a prior version by executing the same steps above. Just make sure you delete your old `docker-compose.yml` first. if you're upgrading from a version prior to 0.6.26, you'll need to reset your price levels and email settings from the web interface admin panel, as price levels and emails settings are now set from the web interface rather than a config file. You'll also need the new isso.env file if you're upgrading from a version prior to 0.6.26.

<h2>Post-Install Setup</h2>

The first visitor to the site will be prompted to register as administrator. The administrator is the user that posts updates, gets paid, etc. The administrator is the content creator. 

Heading to the admin panel should be your first step after registering as the admin, as the site will not function properly until email and BTCPay Server settings are filled in. Square settings for accepting fiat are optional, as are the settings for Google Analytics and user comments. BTCPay pairing and email setup are mandatory, and your site will malfunction without them.

You'll need SMTP server info for the email section. Gmail, Yahoo, etc are not good servers to use for this purpose, as they block bulk emails. If you don't have SMTP settings to use, here's an example of an easy to use service that would work: https://www.easy-smtp.com/ (free for 10,000 emails per month).

Your users will get a 5 hour subscription as soon as they pay their BTCPay invoice. That is bumped to 30 days as soon as BTCPay recognizes the payment as "confirmed". BTCPay settings determine how many confirmations are required to make a payment "confirmed."

If you decide to allow fiat payments, after setting up square, it is suggested that you run a [test charge by follwing these instructions](https://github.com/JeffVandrewJr/patron/blob/master/test-charge.md).
