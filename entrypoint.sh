#!/bin/sh

# Exit on any error
set -e

# Run database migrations
uv run python manage.py migrate

# Start Gunicorn server
exec uv run gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 nethz_django.wsgi:application
