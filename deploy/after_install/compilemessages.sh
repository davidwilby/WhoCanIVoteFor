#!/usr/bin/env bash
set -xeE

source /var/www/wcivf/venv/bin/activate
cd /var/www/wcivf/code/
python manage.py compilemessages
