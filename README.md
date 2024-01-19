# Environment Variables

This section outlines the environment variables used in this project. You can create a `.env` file in the root directory of the project to define all the environment variables. These variables can then be loaded into your application using the `python-decouple` library.

- `SECRET_KEY`: **(required)** A unique, secret key used for security purposes. It is essential for running the application and should be kept confidential.

- `PRODUCTION_DOMAIN`: (optional in development/testing, required in production) Specifies the domain name for the production environment. This should be set to the domain where the application is hosted in production.

- `ENVIRONMENT`: (optional) Specifies the mode in which the application runs. It can be set to `development`, `testing`, or `production`. The default value is `production`.
  - In `development` mode:
    - `DEBUG` is activated, allowing error details to be displayed.
    - `ALLOWED_HOSTS` includes `127.0.0.1` and `localhost`.
    - `STATIC_URL` is set to `"static/"`.
  - In `testing` mode:
    - `DEBUG` is set to `false` to facilitate the testing of error pages and other non-development scenarios. Therefore you can simulate your production mode inside your development environment.
    - `ALLOWED_HOSTS` includes `localhost` and `127.0.0.1`.
    - `STATIC_URL` is set to `"assets/"`.
  - In `production` mode:
    - `DEBUG` is set to `false` for security and performance.
    - `ALLOWED_HOSTS` should be set to your specific domain.
    - `STATIC_URL` is `"assets/"`.

# Build Docker Container

## Build Docker Image

To be able to only run once the `python manage.py collectstatic` during the image build you must provide a secret key. This secret key can be a 'dummy' secret key. This 'dummy' secret key is not saved to the docker image!

```bash
sudo docker build --build-arg SECRET_KEY=dummy_secret_key -t image_name /path/to/nethz_django
```

## Run Docker Container

Currently only the `testing` environment (or the `development` environment) are supported. Otherwise you would need to provide the `PRODUCTION_DOMAIN` environment variable or you would need to update the allowed hosts in django's settings.py file before building your image.

Here you need to provide the 'real' secret key. Otherwise your container will crash immediately due to the missing secret key (see the logs of your docker container).

To make the database persistent you need to specify a volume.

```bash
sudo docker run -dit -p 6000:80 -e ENVIRONMENT=testing -e SECRET_KEY=real_secret_key -v /host/path/to/container_volume/db:/app/db --name container_name image_name

```
