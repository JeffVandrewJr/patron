<h2>Manual Install Method (from Source)</h2>

If you prefer installing from source rather than using the simplified install in the [README](https://github.com/JeffVandrewJr/patron/blob/master/README.md#easy-install-method):
```bash
git clone https://github.com/JeffVandrewJr/patron.git

cd patron

# this checkout step is IMPORTANT, otherwise you may run an unstable version
git checkout v0.5.2

# one of LibrePatron's dependencies will crash without a valid timezone setting (see notes in README)
# different distros set timezone differently; below is an Ubuntu example
export TZ=America/New_York

# install dependencies
sudo apt-get install build-essential libffi-dev python3-dev libssl-dev

# venv and pip dependencies
python3 -m venv venv
source venv/bin/activate
pip install gunicorn
pip install -r requirements.txt

# open librepatron.env, which shows all environmental variables which you need to set
# then make sure you set each of those variables
# you'll probably want to commit the exported variables to a shell config file so they stay set
nano librepatron.env
export SITEURL=https://example.com
export VIRTUAL_HOST=example.com
# <keep setting the rest of the variables mentioned in librepatron.env>

# set up the database
flask db upgrade

# run gunicorn
# fill in the log files of your choice below
export GUNICORN_CMD_ARGS="--bind=0.0.0.0:8006 --workers=3 --access-logfile=- --error-logfile=-"
gunicorn patron:app
```
You'll of course then need to set a proxy server to direct traffic to port 8006.
