# Use Python 3.13 slim image for smaller size and better security
FROM python:3.13-slim

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/tmp/uv-cache

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
RUN export SECRET_KEY="$SECRET_KEY" && \
    export PRODUCTION_DOMAINS="$PRODUCTION_DOMAINS" && \
    export EMAIL_HOST="$EMAIL_HOST" && \
    export EMAIL_PORT="$EMAIL_PORT" && \
    export EMAIL_HOST_USER="$EMAIL_HOST_USER" && \
    export EMAIL_HOST_PASSWORD="$EMAIL_HOST_PASSWORD" && \
    export DEFAULT_FROM_EMAIL="$DEFAULT_FROM_EMAIL" && \
    uv run python manage.py collectstatic --noinput && \
    uv run python manage.py compilemessages

# Create cache directory and change ownership
RUN mkdir -p /tmp/uv-cache && \
    chown -R appuser:appuser /app /tmp/uv-cache

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
