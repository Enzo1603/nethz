# Zugrundeliegendes Image
FROM python:3.12.1-alpine3.19

WORKDIR /app


# Setzen von Umgebungsvariablen
# - PYTHONDONTWRITEBYTECODE verhindert, dass Python .pyc Dateien erstellt werden
# - PYTHONUNBUFFERED stellt sicher, dass Python-Logs sofort in den Docker-Log ausgegeben werden.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Kopieren des Projekts
ADD . /app/

# Installieren von Poetry und Python-Dependendecies
RUN pip install --trusted-host pypi.python.org --no-cache-dir poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Otherwise Django will throw an ImproperlyConfigured Exception
ARG PRODUCTION_DOMAINS="dummy.domain.com,dummy.domain2.com"
ARG EMAIL_HOST="dummy-email-host"
ARG EMAIL_PORT="999"
ARG EMAIL_HOST_USER="dummy-email-host-user"
ARG EMAIL_HOST_PASSWORD="dummy-email-host-password"
ARG DEFAULT_FROM_EMAIL="dummy.from@email.com"
# Otherwise 'python manage.py collectstatic' will throw an error (not saved to the final image)
ARG SECRET_KEY="dummy-secret-key"
# Otherwise the secret key would be saved to the image (not desired)
# ENV SECRET_KEY=${SECRET_KEY}

# Sammeln von statischen Dateien
RUN python manage.py collectstatic --noinput

# Compile messages for translation
RUN apk add --update --no-cache gettext
RUN python manage.py compilemessages

# Ausführen von Django-spezifischen Befehlen wie z.B. das Migrieren der Datenbank
# RUN python manage.py migrate

# Entfernen der Build-Abhängigkeiten, um die Größe des Images zu reduzieren
# RUN apk del build-base

# Port 80 veröffentlichen
EXPOSE 80

# Starten des Gunicorn-Servers
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "nethz_django.wsgi:application"]

# Machen Sie entrypoint.sh ausführbar
RUN chmod +x ./entrypoint.sh

# Setzen Sie entrypoint.sh als Eintrittspunkt
ENTRYPOINT ["./entrypoint.sh"]
