# Deployment

## Backend (Railway)
1. Connect GitHub repo to Railway
2. Set environment variables
3. Auto-deploys on push to main

## Frontend (GitHub Pages)
1. Build: `cd frontend && npm run build`
2. Deploy via GitHub Actions to gh-pages branch

## Environment Variables
- `DATABASE_URL` — PostgreSQL connection
- `SECRET_KEY` — Django secret
- `ALLOWED_HOSTS` — Backend domain
