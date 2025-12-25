#!/bin/sh

# Exit on any error
set -e

# Run database migrations (only if needed)
python manage.py migrate --noinput

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --access-logfile - --error-logfile - nethz_django.wsgi:application
