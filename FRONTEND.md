# Frontend Guide

This document covers the React frontend for SecurePass Dashboard.

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| React | 18.x | UI framework |
| Vite | 5.x | Build tool & dev server |
| Tailwind CSS | 3.x | Utility-first styling |
| Lucide React | latest | Icon library |
| Axios | 1.x | HTTP client |
| React Router | 6.x | Client-side routing |

---

## Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├── api/              # Axios instances & API call helpers
│   │   └── client.js
│   ├── components/       # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── PasswordCard.jsx
│   │   └── StrengthMeter.jsx
│   ├── hooks/            # Custom React hooks
│   │   └── useAuth.js
│   ├── pages/            # Route-level page components
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   └── Register.jsx
│   ├── App.jsx           # Root component & router
│   └── main.jsx          # Vite entry point
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

---

## Local Development

```bash
cd frontend
npm install
npm run dev
```

The dev server starts at **http://localhost:5173** and proxies API calls to `http://localhost:8000`.

### Environment Variables

Create a `.env` file in `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

> **Note:** All Vite env vars must be prefixed with `VITE_` to be exposed to the browser.

---

## Available Scripts

| Script | Description |
|---|---|
| `npm run dev` | Start Vite dev server with HMR |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint across all source files |

---

## Routing

| Path | Component | Auth required |
|---|---|---|
| `/` | Dashboard | ✅ |
| `/login` | Login | ❌ |
| `/register` | Register | ❌ |
| `/password/:id` | PasswordDetail | ✅ |

Protected routes redirect to `/login` if no valid token is present.

---

## API Integration

All API calls go through `src/api/client.js`, which attaches the auth token automatically:

```js
import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Token ${token}`;
  return config;
});

export default client;
```

---

## Build & Deploy

Production builds are deployed to GitHub Pages via the CI workflow. See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

```bash
npm run build
# Output: frontend/dist/
```
