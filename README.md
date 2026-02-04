# 🔐 SecurePass Dashboard

A full-stack password security dashboard with breach detection - portfolio project demonstrating modern web development practices.

[![Django](https://img.shields.io/badge/Django-4.2+-green?logo=django)](https://djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-blue?logo=react)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What It Does

- ✅ Analyzes password strength with detailed scoring (0-100)
- ✅ Detects data breaches using Have I Been Pwned API (k-anonymity)
- ✅ Interactive dashboard with Chart.js visualizations
- ✅ User authentication with JWT tokens
- ✅ Check history and security statistics

## 🖥️ Screenshots

*Coming soon*

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + Vite + TailwindCSS + Chart.js |
| **Backend** | Django 4.2 + Django REST Framework |
| **Auth** | JWT (SimpleJWT) |
| **External API** | Have I Been Pwned |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Icons** | Lucide React |

## 📁 Project Structure

```
securepass-dashboard/
├── backend/              # Django REST API
│   ├── api/              # Main app (models, views, services)
│   │   ├── models.py     # Database models
│   │   ├── views.py      # API endpoints
│   │   ├── services.py   # Business logic
│   │   └── serializers.py
│   ├── securepass/       # Django project settings
│   └── requirements.txt
│
├── frontend/             # React + Vite
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Route pages
│   │   ├── context/      # React Context (Auth)
│   │   └── api/          # Axios configuration
│   └── package.json
│
├── docs/                 # Documentation
│   ├── TECH_STACK.md     # Technology deep dive
│   ├── ARCHITECTURE.md   # System architecture
│   └── API.md            # API reference
│
└── start.sh              # Dev start script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Or use the start script:
```bash
chmod +x start.sh
./start.sh
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api

## 🔑 Key Features

### 1. Password Strength Analyzer
Evaluates passwords against 10 criteria:
- Length (8+, 12+, 16+ characters)
- Character variety (upper, lower, numbers, special)
- Pattern detection (common passwords, sequences, repetition)

### 2. Breach Detection
Uses Have I Been Pwned API with k-anonymity:
- Only sends first 5 characters of SHA-1 hash
- Your actual password never leaves your device
- Checks against billions of leaked passwords

### 3. Security Dashboard
- Doughnut chart: Password strength distribution
- Bar chart: Recent checks comparison
- Statistics: Total checks, breached count, average strength
- Overall security score calculation

### 4. JWT Authentication
- Secure token-based authentication
- Access token (60 min) + Refresh token (7 days)
- Automatic token refresh on expiration

## 📚 Documentation

- [**Tech Stack Deep Dive**](docs/TECH_STACK.md) - Detailed explanation of all technologies
- [**Architecture Overview**](docs/ARCHITECTURE.md) - System design and data flow
- [**API Reference**](docs/API.md) - Complete REST API documentation

## 📊 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Get JWT tokens | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| POST | `/api/passwords/check/` | Full password check | Yes |
| POST | `/api/passwords/quick-check/` | Quick check (no save) | No |
| GET | `/api/passwords/history/` | Check history | Yes |
| GET | `/api/stats/` | Dashboard statistics | Yes |

## 🔒 Security Features

- **No plain text storage** - Passwords are never stored
- **K-anonymity** - HIBP queries only send hash prefix
- **JWT with refresh** - Secure, stateless authentication
- **CORS configured** - Restricted to allowed origins
- **Input validation** - All inputs sanitized via serializers

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

**Backend:**
- Django & Django REST Framework
- RESTful API design
- JWT authentication
- Third-party API integration
- Database modeling

**Frontend:**
- React 18 with hooks
- Context API for state management
- React Router for navigation
- Axios with interceptors
- TailwindCSS for styling
- Chart.js for data visualization

**Security:**
- Password security best practices
- K-anonymity privacy model
- Token-based authentication

## 🚧 Future Improvements

- [ ] Password generator
- [ ] Two-factor authentication
- [ ] Browser extension
- [ ] Export reports (PDF)
- [ ] Dark/light theme toggle
- [ ] Internationalization (i18n)

## 👨‍💻 Author

**Kelson Brito**
- LinkedIn: [kelson-brito](https://www.linkedin.com/in/kelson-brito-ba922b363)
- GitHub: [@kelsonbrito50](https://github.com/kelsonbrito50)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built as a portfolio project to demonstrate full-stack development skills.*
