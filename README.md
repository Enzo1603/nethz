# Environment Variables

This section outlines the environment variables used in this project. You can create a `.env` file in the root directory of the project to define all the environment variables. These variables can then be loaded into your application using the `python-decouple` library.

- `SECRET_KEY`: **(required)** A unique, secret key used for security purposes. It is essential for running the application and should be kept confidential.

- `PRODUCTION_DOMAINS`: (optional in development/testing, **required** in production) Specifies the domain name(s) for the production environment. This should be set to the domain or domains where the application is hosted in production. **Multiple domains** can be specified by separating them with commas. For example: "example.com,example.net,example.org".

- `ENVIRONMENT`: (optional) Specifies the mode in which the application runs. It can be set to `development`, `testing`, or `production`. The default value is `production`.
  - In `development` mode:
    - `DEBUG` is activated, allowing error details to be displayed.
    - `ALLOWED_HOSTS` is set to the wildcard operator `*` (any domain is allowed).
    - `STATIC_URL` is set to `"static/"`.
  - In `testing` mode:
    - `DEBUG` is set to `false` to facilitate the testing of error pages and other non-development scenarios. Therefore you can simulate your production mode inside your development environment.
    - `ALLOWED_HOSTS` is set to the wildcard operator `*` (any domain is allowed).
    - `STATIC_URL` is set to `"assets/"`. You therefore need to run `python manage.py collectstatic` (already done for you in the docker image).
  - In `production` mode:
    - `DEBUG` is set to `false` for security and performance.
    - `ALLOWED_HOSTS` is set to your `PRODUCTION_DOMAINS`.
    - `STATIC_URL` is `"assets/"`. You therefore need to run `python manage.py collectstatic` (already done for you in the docker image).

- `EMAIL_HOST`: (**required**) The host of your email server. For example, for Gmail it would be `smtp.gmail.com`.

- `EMAIL_PORT`: (**required**) The port to use for the SMTP server defined in `EMAIL_HOST`.

- `EMAIL_HOST_USER`: (**required**) The username to use for the SMTP server.

- `EMAIL_HOST_PASSWORD`: (**required**) The password to use for the SMTP server.

- `EMAIL_USE_TLS`: (optional) Whether to use a secure TLS connection when connecting to the SMTP server. If not provided, it defaults to `True`.

- `DEFAULT_FROM_EMAIL`: (**required**) The default email address to use for various automated correspondence from the site managers.

# Build Docker Container

## Build Docker Image

```bash
sudo docker build -t image_name /path/to/nethz_django_root_project_folder
```

## Run Docker Container

To run your docker container in the `production` environment, you need to specify the `PRODUCTION_DOMAINS` environment variable under which your container is being accessed (or you need to update the ALLOWED_HOSTS in django's settings.py file before building your image).

To run your docker container in the `testing` or `development` environment, you do not need to set a production domain.

Here you need to provide your `SECRET_KEY`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,`EMAIL_HOST_PASSWORD`, and`DEFAULT_FROM_EMAIL`. Otherwise your container will crash immediately due to the missing environment variables (see the logs of your docker container).

To make the database persistent you need to specify a volume.

```bash
sudo docker run -dit -p 5000:80 \ 
-e ENVIRONMENT=environment \
-e SECRET_KEY=secret_key \
-e EMAIL_HOST=email_host \
-e EMAIL_PORT=email_port \
-e EMAIL_HOST_USER=email_host_user \
-e EMAIL_HOST_PASSWORD=email_host_password \
-e DEFAULT_FROM_EMAIL=default_from_email \
-v /host/path/to/container_volume/db:/app/db \
--name container_name image_name
```
