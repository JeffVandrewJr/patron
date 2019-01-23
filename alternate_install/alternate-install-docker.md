<h2>Alternate Install via Docker-Compose</h2>

If you're not using the installer script mentioned in the README, a docker-compose is provided that automatically installs LibrePatron along with nginx and obtains SSL certificates. You do not need to do anything in this section if you used the LunaNode installer. 

Before installing, don't forget to point your domain's DNS to your server's address. (You perform this step with your domain registrar: GoDaddy, NameCheap, etc.) You must point both the main domain and the `comments` subdomain. So if you're hosting LibrePatron at `example.com`, both `example.com` and `comments.example.com` must point to your server address. Here are the steps (to be executed from `$HOME` directory):

```bash
wget https://github.com/JeffVandrewJr/patron/blob/master/alternate_install/librepatron.env

# open librepatron.env and fill in the necessary info as mentioned in the file comments, and then save
nano librepatron.env

wget https://github.com/JeffVandrewJr/patron/blob/master/alternate_install/isso.env

# open isso.env and fill in the necessary info as mentioned in the file comments, and then save
nano isso.env

sudo docker network create nginx-net
wget https://raw.githubusercontent.com/JeffVandrewJr/patron/master/docker-compose.yml
sudo docker-compose up -d
```
Your site will then be launched and operational! You can upgrade from a prior version by executing the same steps above. Just make sure you delete your old `docker-compose.yml` first. if you're upgrading from a version prior to 0.6.26, you'll need to reset your price levels and email settings from the web interface admin panel, as price levels and emails settings are now set from the web interface rather than a config file. You'll also need the new isso.env file if you're upgrading from a version prior to 0.6.26.
