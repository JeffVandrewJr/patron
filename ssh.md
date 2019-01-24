Here are instructions on how to access your LunaNode via SSH. I stole them from bitcoinshirt!

<h2>Connect via SSH to your Virtual Machine</h2>

Log into LunaNode to grab your IP address and password. To do this, go to https://lunanode.com, log in, and then go to this screen:

![LunaNode](https://cdn-images-1.medium.com/max/800/1*YLwkQ_aoZuVme5EAIynlnA.png)

You're now ready to log into your VPS via SSH. 



<h4>SSH Instructions for Mac, Linux, and other Unix-Like Systems</h4>

If you are on Max, Linux, or another Unix-Like system, the first step is to open a terminal. Thenn simply enter the following command:
```bash
# fill in the x's with your LunaNode's EXTERNAL IP address as shown on the screen above
ssh ubuntu@xxx.xx.x.x
```
You'll then be prompted for your password. This is NOT the password you used to log into the LunaNode website. It is the password shown on the screen above (yours will obviously be different from the password on the above screenshot).



<h4>SSH Instructions for Windows</h4>

If you are on Windows, instead of the commands above, download and install Putty [(click here to download)](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.70-installer.msi) and copy/paste your LunaNode External IP Address in the "Host Name (Or IP Address)" box:

![Putty](https://cdn-images-1.medium.com/max/800/1*ldCagOzckSKupFlR9tUR8A.png)

Reminder: Your LunaNode external IP address will be a series of numbers with dots in between, as shown in the General Tab in the very top photo. When you connect you will be prompted to input a password, which you can find it in the General tab of your Virtual Machine (as shown in the very top photo). This is not the password that you used to log into lunanode.com.
