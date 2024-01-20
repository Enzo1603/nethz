# Environment Variables

This section outlines the environment variables used in this project. You can create a `.env` file in the root directory of the project to define all the environment variables. These variables can then be loaded into your application using the `python-decouple` library.

- `SECRET_KEY`: **(required)** A unique, secret key used for security purposes. It is essential for running the application and should be kept confidential.

- `PRODUCTION_DOMAINS`: (optional in development/testing, **required** in production) Specifies the domain name(s) for the production environment. This should be set to the domain or domains where the application is hosted in production. **Multiple domains** can be specified by separating them with commas. For example: "example.com,example.net,example.org".

- `ENVIRONMENT`: (optional) Specifies the mode in which the application runs. It can be set to `development`, `testing`, or `production`. The default value is `production`.
  - In `development` mode:
    - `DEBUG` is activated, allowing error details to be displayed.
    - `ALLOWED_HOSTS` includes `127.0.0.1` and `localhost`.
    - `STATIC_URL` is set to `"static/"`.
  - In `testing` mode:
    - `DEBUG` is set to `false` to facilitate the testing of error pages and other non-development scenarios. Therefore you can simulate your production mode inside your development environment.
    - `ALLOWED_HOSTS` includes `localhost` and `127.0.0.1`.
    - `STATIC_URL` is set to `"assets/"`. You therefore need to run `python manage.py collectstatic` (already done for you in the docker image).
  - In `production` mode:
    - `DEBUG` is set to `false` for security and performance.
    - `ALLOWED_HOSTS` is set to your `PRODUCTION_DOMAINS`.
    - `STATIC_URL` is `"assets/"`. You therefore need to run `python manage.py collectstatic` (already done for you in the docker image).

# Build Docker Container

## Build Docker Image

```bash
sudo docker build -t image_name /path/to/nethz_django
```

## Run Docker Container

To run your docker container in the `production` environment, you need to specify the `PRODUCTION_DOMAINS` environment variable under which your container is being accessed (or you need to update the ALLOWED_HOSTS in django's settings.py file before building your image).

To run your docker container in the `testing` or `development` environment, you do not need to set a production domain.

Here you need to provide your `SECRET_KEY`. Otherwise your container will crash immediately due to the missing secret key (see the logs of your docker container).

To make the database persistent you need to specify a volume.

```bash
sudo docker run -dit -p 6000:80 -e ENVIRONMENT=environment -e SECRET_KEY=secret_key -v /host/path/to/container_volume/db:/app/db --name container_name image_name
```
