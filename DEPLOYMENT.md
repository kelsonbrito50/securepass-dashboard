# Deployment Guide

This guide covers deploying SecurePass Dashboard to **Railway** (backend) and **GitHub Pages** (frontend).

---

## Prerequisites

- Railway account: https://railway.app
- GitHub repository with Actions enabled
- Node.js 18+ and Python 3.11+ locally

---

## Backend — Railway

### 1. Create a New Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **New Project → Deploy from GitHub Repo**
3. Select `kelsonbrito50/securepass-dashboard`
4. Set the **Root Directory** to `backend`

### 2. Add PostgreSQL

1. Inside the project, click **New → Database → PostgreSQL**
2. Railway auto-injects `DATABASE_URL` into your service

### 3. Environment Variables

Set these in Railway → Variables:

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.up.railway.app` |
| `DATABASE_URL` | Auto-set by Railway Postgres |

### 4. Deploy

Railway builds on every push to `main`. Check the build logs in the Railway dashboard.

### 5. Run Migrations

Open a Railway shell or use the CLI:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## Frontend — GitHub Pages

### 1. Configure `vite.config.js`

```js
export default {
  base: '/securepass-dashboard/',
}
```

### 2. Set API Base URL

Create `frontend/.env.production`:
```
VITE_API_BASE_URL=https://your-app.up.railway.app/api
```

### 3. Enable GitHub Pages

1. Go to **Settings → Pages**
2. Set source to **GitHub Actions**

### 4. Deploy

Push to `main`. The `deploy-frontend.yml` workflow will build and publish automatically.

---

## Health Check

- Backend: `https://your-app.up.railway.app/api/health/`
- Frontend: `https://kelsonbrito50.github.io/securepass-dashboard/`

---

## Rollback

- **Railway:** Click **Deployments → Rollback** in the dashboard
- **GitHub Pages:** Revert the commit and push to re-trigger the workflow
