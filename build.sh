#!/usr/bin/env bash
# exit on error
set -o errexit

# Install requirements
pip install -r requirements.txt

# Create static directories
mkdir -p static/material/admin/css
mkdir -p static/material/admin/js

# Copy material admin static files
cp -r $(pip show django-material-admin | grep Location | cut -d " " -f 2)/material/static/material/* static/material/

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate