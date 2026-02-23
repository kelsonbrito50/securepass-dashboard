# Developer Onboarding Guide

Welcome to SecurePass Dashboard! Get up and running in under 10 minutes.

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Git

## Quick Start

### 1. Clone

```bash
git clone https://github.com/kelsonbrito50/securepass-dashboard.git
cd securepass-dashboard
```

### 2. Environment Setup

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Start with Docker

```bash
docker-compose up --build
```

This starts:
- Django backend on http://localhost:8000
- React frontend on http://localhost:5173
- PostgreSQL database

### 4. Apply Migrations

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Development (Without Docker)

### Backend

```bash
cd backend
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Key Concepts

- **k-anonymity**: We send only the first 5 SHA-1 chars to HIBP API
- **JWT auth**: Access tokens expire in 5 min, refresh in 1 day
- **CORS**: Configured in `backend/core/settings.py`

## Admin Panel

http://localhost:8000/admin/ — Use superuser credentials.
