# 🔐 SecurePass Dashboard

A full-stack password security dashboard with breach detection - portfolio project.

## 🎯 What It Does

- ✅ Users can check password strength
- ✅ Detects if passwords appeared in data breaches (Have I Been Pwned API)
- ✅ Shows password strength with interactive visuals
- ✅ Dashboard with security statistics

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite + Chart.js + TailwindCSS |
| Backend | Django + Django REST Framework |
| Auth | JWT (SimpleJWT) |
| External API | Have I Been Pwned |
| Database | SQLite (dev) / PostgreSQL (prod) |

## 📁 Structure

```
securepass-dashboard/
├── backend/          # Django REST API
│   ├── securepass/   # Django project
│   ├── api/          # REST API app
│   └── manage.py
├── frontend/         # React app
│   ├── src/
│   └── package.json
└── docs/             # Documentation
```

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Features

1. **Password Strength Analyzer** - Analyzes strength with visual criteria breakdown
2. **Breach Detection** - Checks against Have I Been Pwned database
3. **Security Dashboard** - Charts and statistics
4. **User Auth** - Login/register with JWT tokens

## 🎨 Screenshots

*Coming soon*

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register new user |
| POST | /api/auth/login/ | Login (returns JWT) |
| POST | /api/passwords/check/ | Check password (auth required) |
| POST | /api/passwords/quick-check/ | Quick check (no auth) |
| GET | /api/stats/ | User statistics |

## 🔒 Security

- Passwords are NEVER stored in plain text
- Uses k-anonymity with HIBP API (only first 5 chars of hash sent)
- JWT with refresh tokens
- HTTPS required in production

## 👨‍💻 Author

**Kelson Brito**
- LinkedIn: [kelson-brito](https://www.linkedin.com/in/kelson-brito-ba922b363)
- GitHub: [@kelsonbrito50](https://github.com/kelsonbrito50)

## 📄 License

MIT
