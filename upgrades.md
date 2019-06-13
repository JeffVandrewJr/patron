<h1>Current Version of LibrePatron: 0.7.37</h1>

If your admin panel shows a version less than the version above, follow one of the two sets of instructions below to upgrade. Which set of instructions you choose will be determined by the method you used to originally install LibrePatron.

<h3>Upgrading to Current Version if You Installed through BTCPay</h3>

If you originally installed using the official BTCPay installer, you would simply update your BTCPay server and your LibrePatron should update right alongside it. 

To do that, you simply log into BTCPay, then hit Server Settings, Maintenance, then Update.

Note that there can be a short delay before the latest upgrade is available through the BTCPay update system.

<h3>Upgrading to Current Version if you Did Not Install Through BTCPay</h3>

If you didn't originally install through BTCPay and your LibrePatron instance lives on a server separate from your BTCPay instance, you'd instead use docker-compose.

```bash
# if you have an old docker-compose.yml file, first delete it
rm docker-compose.yml

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
Your site will then be launched and operational! if you're upgrading from a version prior to 0.6.26, you'll need to reset your price levels and email settings from the web interface admin panel, as price levels and emails settings are now set from the web interface rather than a config file.
