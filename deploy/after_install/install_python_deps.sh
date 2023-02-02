#!/usr/bin/env bash
set -xeE

# should we delete the env and recreate?
# Create a virtualenv
cd /var/www/wcivf/
python3 -m venv venv

source /var/www/wcivf/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

pip install -r /var/www/wcivf/code/requirements.txt
