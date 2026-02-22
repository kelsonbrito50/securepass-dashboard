# Backend Dockerfile — Railway-ready
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

EXPOSE 8000

# Use PORT env var (Railway injects this)
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn securepass.wsgi:application --bind 0.0.0.0:${PORT:-8000}
