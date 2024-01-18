# Build Docker Container

## Build Docker Image

To be able to only run once the `python manage.py collectstatic` during the image build you must provide a secret key. This secret key can be a 'dummy' secret key.

```bash
sudo docker build --build-arg SECRET_KEY=dummy_secret_key -t image_name /path/to/nethz_django
```

## Run Docker Container

Currently only the testing environment (or the development) environment are supported (otherwise you would need to update the allowed hosts in django's settings.py file before building your image).

Here you need to provide the 'real' secret key. Otherwise your container will crash immediately due to the missing secret key (see the logs of your docker container).

To make the database persistent you need to specify a volume.

```bash
sudo docker run -dit -p 6000:80 -e ENVIRONMENT=testing -e SECRET_KEY=real_secret_key -v /host/path/to/container_volume/db:/app/db --name container_name image_name

```
