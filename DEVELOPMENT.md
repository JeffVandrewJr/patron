# Development

## BTCPay Server

You can pair with your existing production BTCPay Server, or [set one up locally](https://github.com/btcpayserver/btcpayserver-doc/blob/master/LocalDevelopment.md).

## Run development server

Clone the repository.

Install Python dependencies:

```sh
pip install flask flask_admin flask_apscheduler flask_login flask_principal flask_fileupload flask_bootstrap flask_migrate flask_ezmail
pip install gunicorn apscheduler sqlalchemy
pip install markdown python-slugify jwt psutil
pip install btcpay
pip install squareconnect
```

Create or upgrade the database:

```sh
flask db upgrade
```

Start the server:

```sh
export ISSO_CONFIG_PATH=$PWD
export COMMENTS_DB_PATH=$PWD
docker_boot.py & gunicorn patron:app
```
