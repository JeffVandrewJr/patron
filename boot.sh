#!/bin/sh
flask db upgrade
exec gunicorn patron:app
