# Development

## BTCPay Server

You can pair with your existing production BTCPay Server, or [set one up locally](https://github.com/btcpayserver/btcpayserver-doc/blob/master/LocalDevelopment.md).

## Run development server

Clone the repository.

Install Python dependencies:

```sh
pip3 install flask flask_admin flask_apscheduler flask_login flask_principal flask_fileupload flask_bootstrap flask_migrate flask_ezmail
pip3 install gunicorn apscheduler sqlalchemy
pip3 install markdown python-slugify jwt psutil
pip3 install btcpay
pip3 install squareconnect
```

Configure database and settings path:

```sh
export ISSO_CONFIG_PATH=$PWD/isso.cfg
export COMMENTS_DB_PATH=$PWD/comments.db
```

Create or upgrade the database:

```sh
flask db upgrade
```

Start the server:

```sh
docker_boot.py & gunicorn patron:app
```
## Run tests

Install Python dependencies:

```sh
pip3 install pytest
```

Configure database path:

```sh
export COMMENTS_DB_PATH_TEST=$PWD/comments-test.db
```

Create or upgrade the test database:


```sh
flask db upgrade
```

Run tests:

```sh
python3 -m pytest
```
