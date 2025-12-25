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
ENV PYTHONPATH="/app"

# Copy application code
COPY templates/ /app/templates/
COPY locale/ /app/locale/
COPY static/ /app/static/
COPY accounts/ /app/accounts/
COPY main/ /app/main/
COPY worldle/ /app/worldle/
COPY lib/ /app/lib/
COPY nethz_django/ /app/nethz_django/
COPY manage.py entrypoint.sh ./

# Collect static files and compile messages
# Dummy values only for build
RUN export SECRET_KEY="build-only-dummy-key" \
    PRODUCTION_DOMAINS="localhost" \
    EMAIL_HOST="localhost" \
    EMAIL_PORT="25" \
    EMAIL_HOST_USER="dummy" \
    EMAIL_HOST_PASSWORD="dummy" \
    DEFAULT_FROM_EMAIL="dummy@localhost" && \
    python manage.py collectstatic --noinput && \
    python manage.py compilemessages --ignore=.venv

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/', timeout=5)" || exit 1

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
