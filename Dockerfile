# Use Python 3.13 slim image for smaller size and better security
FROM python:3.13-slim

# User will be set at runtime via docker-compose

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gettext \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Build arguments for collectstatic (not saved to final image)
ARG SECRET_KEY="dummy-secret-key"
ARG PRODUCTION_DOMAINS="dummy.domain.com"
ARG EMAIL_HOST="dummy-email-host"
ARG EMAIL_PORT="999"
ARG EMAIL_HOST_USER="dummy-email-host-user"
ARG EMAIL_HOST_PASSWORD="dummy-email-host-password"
ARG DEFAULT_FROM_EMAIL="dummy.from@email.com"

# Collect static files and compile messages
RUN uv run python manage.py collectstatic --noinput && \
    uv run python manage.py compilemessages

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# User will be set at runtime via docker-compose

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
