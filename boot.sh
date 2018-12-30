#!/bin/sh
flask db upgrade
wait
exec gunicorn patron:app
