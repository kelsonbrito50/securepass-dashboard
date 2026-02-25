<div align="center">

# 🔐 SecurePass Dashboard

### Full-Stack Password Security Platform

[![Django](https://img.shields.io/badge/Django-REST_Framework-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Railway](https://img.shields.io/badge/Railway-Deployed-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**Protecting users from compromised passwords using real breach data.**

[🚀 Live Demo](#-live-demo) · [📖 API Docs](#-api-documentation) · [🛠 Getting Started](#-getting-started) · [🔒 Security](#-security)

</div>

---

## 🚀 Live Demo

| Layer | URL |
|-------|-----|
| 🖥️ **Frontend** | [https://kelsonbrito50.github.io/securepass-dashboard](https://kelsonbrito50.github.io/securepass-dashboard) |
| ⚙️ **Backend API** | Hosted on Railway — see [API Documentation](#-api-documentation) for endpoints |

> **Note:** The backend is deployed on Railway with a PostgreSQL database. Cold starts may take a few seconds on the first request.

---

## 📌 About

**SecurePass Dashboard** is a full-stack security platform that empowers users to audit the strength and exposure of their passwords — in real time, with zero compromise to their privacy.

It integrates with the **Have I Been Pwned (HIBP)** API using the **k-anonymity model**, meaning your actual password is never transmitted over the network. The frontend delivers an interactive, data-rich dashboard built with React 18, TailwindCSS, and Chart.js, while the Django REST Framework backend handles authentication, analysis logic, and breach lookups.

This project was built to demonstrate real-world security engineering — not just CRUD.

---

## ✨ Features

### 🔍 Password Strength Analyzer
- Real-time entropy calculation and strength scoring
- Identifies weaknesses: length, character diversity, common patterns
- Visual feedback with dynamic strength indicators

### 🛡️ HIBP Breach Detection
- Checks passwords against a database of **billions of compromised credentials**
- Uses **k-anonymity** — only the first 5 characters of the SHA-1 hash are sent to the HIBP API
- Your full password never leaves your browser in plaintext

### 📊 Interactive Dashboard
- Historical analysis charts powered by **Chart.js**
- Visual breakdown of password health metrics over time
- Clean, responsive UI with TailwindCSS

### 🔐 JWT Authentication
- Stateless authentication with access and refresh token flow
- Secure route protection on both frontend and backend
- Token expiration and renewal handled transparently

---

## 🧰 Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **Python 3.x** | Core language |
| **Django** | Web framework |
| **Django REST Framework** | API layer |
| **Simple JWT** | Token-based authentication |
| **PostgreSQL** | Relational database |
| **Railway** | Cloud deployment & managed DB |
| **HIBP API** | Breach data source |

### Frontend
| Technology | Purpose |
|---|---|
| **React 18** | UI library |
| **Vite** | Build tool & dev server |
| **TailwindCSS** | Utility-first styling |
| **Chart.js** | Data visualization |
| **Axios** | HTTP client |
| **React Router v6** | Client-side routing |
| **GitHub Pages** | Static hosting |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              React 18 SPA (GitHub Pages)                │   │
│   │                                                         │   │
│   │  ┌──────────────┐   ┌───────────────┐  ┌────────────┐  │   │
│   │  │  Auth Views  │   │  Dashboard    │  │  Analyzer  │  │   │
│   │  │  (JWT Flow)  │   │  (Chart.js)   │  │  (HIBP UI) │  │   │
│   │  └──────┬───────┘   └───────┬───────┘  └─────┬──────┘  │   │
│   └─────────┼───────────────────┼────────────────┼──────────┘   │
│             │         HTTPS / JWT Bearer Token   │              │
└─────────────┼───────────────────┼────────────────┼──────────────┘
              │                   │                │
              ▼                   ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│              Django REST Framework API (Railway)                │
│                                                                 │
│   ┌──────────────┐   ┌────────────────┐   ┌─────────────────┐  │
│   │  /api/auth/  │   │  /api/analyze/ │   │  /api/history/  │  │
│   │  JWT tokens  │   │  strength +    │   │  user records   │  │
│   │              │   │  breach check  │   │                 │  │
│   └──────────────┘   └───────┬────────┘   └────────┬────────┘  │
└──────────────────────────────┼─────────────────────┼───────────┘
                               │                     │
              ┌────────────────┘                     │
              │                                      ▼
              ▼                          ┌────────────────────────┐
┌────────────────────────┐               │       PostgreSQL        │
│      HIBP API          │               │   (Railway Managed DB)  │
│  api.pwnedpasswords.com│               │  users / analyses /     │
│  k-anonymity range     │               │  history records        │
│  SHA-1[0:5] prefix     │               └────────────────────────┘
└────────────────────────┘
```

**Data flow for breach detection:**
1. User submits password in browser
2. React computes `SHA-1(password)` client-side
3. Only the **first 5 hex chars** of the 40-character hex hash are transmitted (the "prefix")
4. Backend forwards the prefix to HIBP API and receives a list of matching hash suffixes
5. React checks if the full hash suffix is in that list — **locally, in the browser**
6. Zero exposure of the actual password to any server

---

## 📖 API Documentation

### Base URL
```
https://<your-railway-app>.railway.app/api/
```

### Authentication

#### `POST /api/auth/register/`
Register a new user account.

```json
// Request
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "YourPassword123!"
}

// Response 201
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com"
}
```

#### `POST /api/auth/token/`
Obtain JWT access and refresh tokens.

```json
// Request
{
  "username": "johndoe",
  "password": "YourPassword123!"
}

// Response 200
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

#### `POST /api/auth/token/refresh/`
Refresh an expired access token.

```json
// Request
{ "refresh": "<jwt_refresh_token>" }

// Response 200
{ "access": "<new_jwt_access_token>" }
```

---

### Password Analysis

> All analysis endpoints require `Authorization: Bearer <access_token>` header.

#### `POST /api/analyze/`
Analyze password strength and check breach status.

```json
// Request
{
  "hash_prefix": "5BAA6",
  "password_meta": {
    "length": 12,
    "has_uppercase": true,
    "has_lowercase": true,
    "has_numbers": true,
    "has_symbols": false
  }
}

// Response 200
{
  "strength_score": 72,
  "strength_label": "Strong",
  "breach_count": 0,
  "is_compromised": false,
  "feedback": ["Add symbols to further strengthen your password"]
}
```

#### `GET /api/history/`
Retrieve the authenticated user's analysis history.

```json
// Response 200
[
  {
    "id": 42,
    "analyzed_at": "2024-11-15T14:32:00Z",
    "strength_score": 45,
    "strength_label": "Weak",
    "is_compromised": true,
    "breach_count": 3281
  }
]
```

---

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Resource created |
| `400` | Bad request / validation error |
| `401` | Unauthorized — invalid or missing JWT |
| `403` | Forbidden |
| `404` | Not found |
| `500` | Internal server error |

---

## 🔒 Security

### K-Anonymity Model (HIBP)

The k-anonymity implementation ensures **your full password hash is never sent to any external service**:

1. The password is hashed with **SHA-1** entirely in the client
2. Only the **first 5 characters** of the 40-character hex hash are transmitted (the "prefix")
3. The HIBP API returns all known compromised hashes that share that same 5-char prefix (~500 results on average)
4. The client performs a **local lookup** to determine if the full hash is in the list

This means even if the HIBP API or the backend were compromised, it would be mathematically infeasible to reverse-engineer the original password from a 5-character hash prefix.

### JWT Authentication

- **Access tokens** are short-lived (default: 5 minutes)
- **Refresh tokens** enable seamless session renewal without re-authentication
- Tokens are stored in memory (not `localStorage`) to mitigate XSS risk
- All API routes are protected — unauthenticated requests return `401 Unauthorized`

### General Security Practices

- Passwords are **never stored** — only hashed prefixes are sent
- HTTPS enforced on all deployed services
- Django's CSRF protection enabled on state-mutating views
- Django `SECRET_KEY` and database credentials managed via environment variables
- `DEBUG=False` in production
- CORS restricted to the frontend domain

---

## 🛠 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (local) or Railway account (cloud)
- Git

---

### Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/kelsonbrito50/securepass-dashboard.git
cd securepass-dashboard/backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
```

Edit `.env` with your values:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/securepass
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

```bash
# 5. Run database migrations
python manage.py migrate

# 6. Create a superuser (optional)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Backend running at: `http://localhost:8000`

---

### Frontend Setup

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Configure environment variables
cp .env.example .env.local
```

Edit `.env.local`:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

```bash
# 3. Start the development server
npm run dev
```

Frontend running at: `http://localhost:5173`

---

## 💡 What I Learned

Building SecurePass Dashboard pushed me into real-world security engineering territory:

- **K-anonymity in practice** — Implementing the HIBP k-anonymity model forced me to deeply understand hash functions, prefix matching, and why client-side cryptography matters. It's not just "call the API" — the privacy guarantee requires deliberate architectural choices about where computation happens.

- **Decoupled full-stack deployment** — Running the frontend on GitHub Pages and the backend on Railway taught me the realities of CORS configuration, API URL management across environments, and the tradeoffs of separating static hosting from API hosting.

- **JWT token lifecycle** — Building the complete flow (login → access token → expiry → refresh → re-auth) from scratch gave me a much deeper understanding than any tutorial. Handling edge cases like concurrent requests during token refresh was the real challenge.

- **Chart.js for security data** — Visualizing password analysis history required thinking about what metrics actually matter to users. A strength score means nothing without context — showing trends over time made the data actionable.

- **Django REST Framework serializer design** — Writing serializers that validate security-sensitive input (hash prefixes, password metadata) without ever accepting the raw password taught me to think defensively about every field in an API contract.

---

## License

[MIT](./LICENSE) © [Kelson Brito](https://github.com/kelsonbrito50)

---

<div align="center">

Built by **[Kelson Brito](https://github.com/kelsonbrito50)**

⭐ Star this repo if you find it useful.

</div>
