<h1>Current Version of LibprePatron: 0.6.64</h1>

<h2>Upgrading to Current Version if You Originally Used luna-installer.sh</h2>

If you originally installed using the LunaNode one-click installer, upgrading is just as easy. You would simply SSH into your LunaNode [(click here if you forgot how to do that)](https://github.com/JeffVandrewJr/patron/blob/master/ssh.md), and then:
```bash
# change to root; do not forget the trailing hyphen
sudo su -

# the installer should already be in your $HOME directory from the original install
# re-run the existing installer; replace example.com and email@mail.com with your domain name and email
. ./luna-installer.sh example.com email@mail.com
```

That's it! On the final line, you would replace `example.com` with the domain where you wish to host LibrePatron, and you would replace `email@email.com` with a valid email address.
