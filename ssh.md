Here are instructions on how to access your LunaNode via SSH. I stole them from bitcoinshirt!

<h2>Connect via SSH to your Virtual Machine</h2>

Log into LunaNode to grab your IP address and password. To do this, go to https://lunanode.com, log in, and then go to this screen:

![LunaNode](https://cdn-images-1.medium.com/max/800/1*YLwkQ_aoZuVme5EAIynlnA.png)

You're now ready to log into your VPS via SSH. 

If you are on Linux/MacOS/WSL, simply open a terminal and enter the following command:
```bash
# fill in the x's with your LunaNode's IP address
ssh ubuntu@xxx.xx.x.x
```
You'll then be prompted for your password. This is NOT the password you used to log into the LunaNode website. It is the password shown on the screen above (yours will obviously be different from the password on the above screenshot).

If you are on windows, download and install Putty [Direct Link](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.70-installer.msi) and copy/paste your IP in Host Name (or IP Address) textbox:

![Putty](https://cdn-images-1.medium.com/max/800/1*ldCagOzckSKupFlR9tUR8A.png)
