#!/bin/sh
flask db upgrade
python3 docker_boot.py
wait
exec gunicorn patron:app
