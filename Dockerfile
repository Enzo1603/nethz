# Multi-stage build for smaller final image
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv for faster dependency resolution
RUN pip install --no-cache-dir uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies to a virtual environment
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    gettext \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code (templates, locale, static, etc.)
COPY templates/ /app/templates/
COPY locale/ /app/locale/
COPY static/ /app/static/
COPY accounts/ main/ worldle/ lib/ nethz_django/ manage.py entrypoint.sh ./

# Build arguments for collectstatic (not saved to final image)
ARG SECRET_KEY="dummy-secret-key"
ARG PRODUCTION_DOMAINS="dummy.domain.com"
ARG EMAIL_HOST="dummy-email-host"
ARG EMAIL_PORT="999"
ARG EMAIL_HOST_USER="dummy-email-host-user"
ARG EMAIL_HOST_PASSWORD="dummy-email-host-password"
ARG DEFAULT_FROM_EMAIL="dummy.from@email.com"

# Collect static files and compile messages
RUN python manage.py collectstatic --noinput && \
    python manage.py compilemessages

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
