#!/usr/bin/env bash
# Exit on error
set -o errexit

python -m pip install --upgrade pip
# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# create static directory if it doesn't exist
mkdir -p static

# Apply any outstanding database migrations
python manage.py migrate