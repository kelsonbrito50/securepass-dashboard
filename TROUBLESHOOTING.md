# Troubleshooting Guide

A reference for common issues encountered when developing or deploying SecurePass Dashboard.

---

## Backend Issues

### `django.db.utils.OperationalError: could not connect to server`

**Cause:** PostgreSQL is not running or `DATABASE_URL` is misconfigured.

**Fix:**
```bash
# Local: ensure Postgres is running
pg_ctl start
# Or with Docker:
docker compose up -d db

# Check your .env
echo $DATABASE_URL
```

---

### `ModuleNotFoundError: No module named 'rest_framework'`

**Cause:** Virtual environment not activated or dependencies not installed.

**Fix:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### `CORS` errors in the browser

**Cause:** Frontend origin not in `CORS_ALLOWED_ORIGINS`.

**Fix:** In `backend/securepass/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://kelsonbrito50.github.io",
]
```

---

### `401 Unauthorized` on API requests

**Cause:** Token missing or expired.

**Fix:**
1. Log out and log back in to get a fresh token
2. Ensure `Authorization: Token <token>` header is sent with every request
3. Verify `REST_FRAMEWORK` settings include `TokenAuthentication`

---

## Frontend Issues

### `VITE_API_BASE_URL is undefined`

**Cause:** `.env` file not created or wrong variable name.

**Fix:**
```bash
cp frontend/.env.example frontend/.env
# Set VITE_API_BASE_URL=http://localhost:8000/api
```

Variables must be prefixed with `VITE_` to be exposed to the client.

---

### Blank page on GitHub Pages

**Cause:** `base` not set in `vite.config.js`.

**Fix:**
```js
// vite.config.js
export default {
  base: '/securepass-dashboard/',
}
```

---

### `npm run build` fails — `Cannot find module`

**Fix:**
```bash
rm -rf frontend/node_modules
npm install --prefix frontend
npm run build --prefix frontend
```

---

## Railway Deployment Issues

### Build fails: `No module named 'gunicorn'`

**Fix:** Ensure `gunicorn` is in `backend/requirements.txt`:
```
gunicorn>=21.2.0
```

### Migrations not running

**Fix:** Add a release command in `railway.toml`:
```toml
[deploy]
releaseCommand = "python manage.py migrate"
```

---

## Still stuck?

Open an [issue](https://github.com/kelsonbrito50/securepass-dashboard/issues) with:
- Steps to reproduce
- Full error output
- Your OS, Python version, Node version
