<h2>Manual Install Method (from Source)</h2>

If you prefer installing from source rather than using the simplified install in the [README](https://github.com/JeffVandrewJr/patron/blob/master/README.md#easy-install-method):
```bash
git clone https://github.com/JeffVandrewJr/patron.git

cd patron

# this checkout step is IMPORTANT, otherwise you may run an unstable version
git checkout v0.6.10

# one of LibrePatron's dependencies will crash without a valid timezone setting
# different distros set timezone differently; if your distro ships with tzselect use the command below
tzselect

# install dependencies
sudo apt-get install build-essential libffi-dev python3-dev libssl-dev

# venv and pip dependencies
python3 -m venv venv
source venv/bin/activate
pip install gunicorn
pip install -r requirements.txt

# a variety of environmental variables need to be set
# you'll probably want to commit the exported variables to a shell config file so they stay set
export FLASK_APP=patron.py
export SITEURL=https://example.com
export VIRTUAL_HOST=example.com
export DATABASE_URL=sqlite:////var/lib/db/app.db
export SITEURL=https://example.com
export GUNICORN_CMD_ARGS="--bind=0.0.0.0:8006 --workers=3 --access-logfile=<insert-file> --error-logfile=<insert-file>"

# set up the database
flask db upgrade

# run gunicorn
gunicorn patron:app
```
You'll of course then need to set a proxy server to direct traffic to port 8006.
