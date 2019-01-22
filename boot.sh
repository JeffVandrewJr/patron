#!/bin/sh
flask db upgrade
wait
key=$(hexdump -n 24 -e '4/4 "%08X"' /dev/urandom)
export SECRET_KEY=$key
python3 docker_boot.py &
exec gunicorn patron:app
