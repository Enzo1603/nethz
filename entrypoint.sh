#!/bin/sh

# Exit on any error
set -e

# Run database migrations
python manage.py migrate

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --access-logfile - nethz_django.wsgi:application
