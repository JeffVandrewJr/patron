<h1>Current Version of LibrePatron: 0.6.66</h1>

If your admin panel shows a version less than the version above, follow one of the two sets of instructions below to upgrade. Which set of instructions you choose will be determined by the method you used to originally install LibrePatron.

<h3>Upgrading to Current Version if You Originally Installed LibrePatron with luna-installer.sh</h3>

If you originally installed using the LunaNode one-click installer, upgrading is just as easy. You would simply SSH into your LunaNode [(click here if you forgot how to do that)](https://github.com/JeffVandrewJr/patron/blob/master/ssh.md), and then:
```bash
# change to root; do not forget the trailing hyphen
sudo su -

# the installer should already be in your $HOME directory from the original install; if not, see the README to redownload
# re-run the existing installer; replace example.com and email@mail.com with your domain name and email
. ./luna-installer.sh example.com email@mail.com
```

That's it! On the final line, you would replace `example.com` with the domain where you wish to host LibrePatron, and you would replace `email@email.com` with a valid email address.

<h3>Upgrading to Current Version if you Did Not Use luna-installer.sh</h3>

If you didn't originally install LibrePatron using luna-installer.sh, you'd instead use docker-compose.

```bash
# if you have an old docker-compose.yml file, first delete it
rm docker-compose.yml

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
Your site will then be launched and operational! if you're upgrading from a version prior to 0.6.26, you'll need to reset your price levels and email settings from the web interface admin panel, as price levels and emails settings are now set from the web interface rather than a config file.
