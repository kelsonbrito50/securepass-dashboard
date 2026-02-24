# Architecture Overview

SecurePass Dashboard is built on a decoupled full-stack architecture.

## Backend — Django REST Framework

- **Framework:** Django 4.x + Django REST Framework
- **Database:** PostgreSQL (Railway-managed in production)
- **Auth:** Token-based authentication (DRF `authtoken`)
- **Password audit:** Have I Been Pwned (HIBP) API integration via `pwnedpasswords`
- **Structure:**
  ```
  backend/
  ├── securepass/       # Django project settings
  ├── accounts/         # User registration & auth endpoints
  ├── passwords/        # Password health check endpoints
  └── requirements.txt
  ```

## Frontend — React + Vite

- **Framework:** React 18 with Vite
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **HTTP client:** Axios
- **Structure:**
  ```
  frontend/
  ├── src/
  │   ├── components/   # Reusable UI components
  │   ├── pages/        # Route-level views
  │   ├── hooks/        # Custom React hooks
  │   └── api/          # Axios API helpers
  └── vite.config.js
  ```

## Data Flow

```
Browser → React SPA → Axios → DRF REST API → PostgreSQL
                                    ↓
                              HIBP API (external)
```

## Authentication Flow

1. User registers/logs in via `/api/auth/`
2. DRF returns a token stored in `localStorage`
3. All subsequent requests include `Authorization: Token <token>`

## Deployment

| Layer    | Platform       |
|----------|---------------|
| Backend  | Railway        |
| Frontend | GitHub Pages   |
| Database | Railway Postgres|

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.
