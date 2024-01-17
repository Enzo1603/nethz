#!/bin/sh


# Migrationen ausführen
python manage.py migrate

# Starten des Gunicorn-Servers
exec gunicorn --bind 0.0.0.0:80 nethz_django.wsgi:application
