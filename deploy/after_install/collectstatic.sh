#!/usr/bin/env bash
set -xeE

source /var/www/wcivf/venv/bin/activate
python /var/www/wcivf/code/manage.py collectstatic --noinput --clear
