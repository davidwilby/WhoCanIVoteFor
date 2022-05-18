#!/usr/bin/env bash
set -xeE

source /var/www/wcivf/env/bin/activate
# "default" database has to be migrated first to avoid errors migrating logger
python /var/www/wcivf/code/manage.py migrate --noinput
python /var/www/wcivf/code/manage.py migrate --database=logger --noinput
