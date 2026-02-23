# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- PostgreSQL database
- Python 3.11+
- Node.js 18+

## Environment Setup

```bash
cp .env.example .env
# Edit .env with your values
```

## Local Development

```bash
docker-compose up --build
```

App will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Production Deployment (Railway)

1. Connect GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Railway auto-deploys on push to `main`

See `railway.json` for Railway configuration.

## Manual Production Deploy

```bash
# Backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application

# Frontend
npm ci
npm run build
npm start
```

## Database Migrations

```bash
python manage.py migrate
```

Always run after deploying schema changes.
