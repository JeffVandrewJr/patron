#!/bin/sh
flask db upgrade
wait
python3 docker_boot.py &
exec gunicorn patron:app
