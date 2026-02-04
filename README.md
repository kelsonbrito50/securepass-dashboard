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
│   │   ├── settings.py   # Configuration
│   │   └── urls.py       # URL routing
│   ├── db.sqlite3        # SQLite database (auto-created)
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # React + Vite
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Route pages
│   │   ├── context/      # React Context (Auth)
│   │   └── api/          # Axios configuration
│   ├── .env.example      # Environment variables template
│   └── package.json      # Node dependencies
│
├── docs/                 # Documentation
│   ├── TECH_STACK.md     # Technology deep dive
│   ├── ARCHITECTURE.md   # System architecture
│   └── API.md            # API reference
│
└── start.sh              # Dev start script (both servers)
```

---

## 🚀 Complete Setup Guide

### Prerequisites

Before starting, make sure you have:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

Check versions:
```bash
python --version    # Should be 3.10+
node --version      # Should be 18+
npm --version       # Comes with Node.js
```

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/kelsonbrito50/securepass-dashboard.git
cd securepass-dashboard
```

---

## 🗄️ Backend Setup (Django)

### Step 2: Create Python Virtual Environment

**Linux/Mac:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2+
- Django REST Framework
- SimpleJWT (for authentication)
- django-cors-headers
- requests (for HIBP API)

### Step 4: Database Setup

SecurePass uses **SQLite** by default (no installation needed).

**Create database tables:**
```bash
python manage.py migrate
```

This creates `db.sqlite3` with tables:
- `User` - User accounts
- `PasswordCheck` - Password check history
- `UserStats` - User statistics

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying api.0001_initial... OK
  ...
```

### Step 5: Create Admin User (Optional)

To access Django admin panel:
```bash
python manage.py createsuperuser
```

Follow prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: (your choice, min 8 chars)

### Step 6: Start Backend Server

```bash
python manage.py runserver
```

**Backend is now running on:** http://localhost:8000

**Test it:**
```bash
curl http://localhost:8000/api/passwords/quick-check/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"password":"test123"}'
```

**Expected:** JSON response with password strength analysis.

---

## ⚛️ Frontend Setup (React)

Open a **new terminal** (keep backend running).

### Step 7: Install Node Dependencies

```bash
cd frontend
npm install
```

This installs:
- React 18
- Vite (build tool)
- TailwindCSS
- Axios (API client)
- Chart.js
- React Router
- Lucide React (icons)

### Step 8: Configure API URL (Optional)

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```
VITE_API_URL=http://localhost:8000/api
```

**Note:** Default is already `http://localhost:8000/api`, so this step is optional for local development.

### Step 9: Start Frontend Server

```bash
npm run dev
```

**Frontend is now running on:** http://localhost:5173

**Open in browser:** http://localhost:5173

---

## 🎯 Quick Start (Both Servers)

Use the included start script:

```bash
chmod +x start.sh
./start.sh
```

This starts both servers automatically!

**To stop:** Press `Ctrl+C`

---

## ✅ Verify Everything Works

### Test 1: Quick Check (No Login)

1. Open http://localhost:5173
2. Enter any password in the checker
3. Click "Check Security"
4. ✅ You should see strength score and breach status

### Test 2: Create Account

1. Click "Create Free Account"
2. Enter username, email, password
3. Click "Create Account"
4. ✅ You should be redirected to dashboard

### Test 3: Dashboard

1. After logging in, you should see:
   - Total checks counter
   - Strength distribution chart
   - Recent checks list
2. Try checking more passwords
3. ✅ Watch stats update in real-time

---

## 🗄️ Database Information

### SQLite (Development)

- **Location:** `backend/db.sqlite3`
- **Automatic:** Created on first `migrate`
- **Reset database:**
  ```bash
  rm backend/db.sqlite3
  python manage.py migrate
  ```

### PostgreSQL (Production)

For production, switch to PostgreSQL:

**1. Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

**2. Create Database:**
```bash
sudo -u postgres psql
CREATE DATABASE securepass;
CREATE USER securepassuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE securepass TO securepassuser;
\q
```

**3. Update Django Settings:**

Edit `backend/securepass/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'securepass',
        'USER': 'securepassuser',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**4. Install PostgreSQL adapter:**
```bash
pip install psycopg2-binary
```

**5. Run migrations:**
```bash
python manage.py migrate
```

---

## 🔧 Troubleshooting

### Backend Issues

**"Port 8000 already in use":**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

**"No module named X":**
```bash
# Make sure venv is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Database errors:**
```bash
# Delete and recreate database
rm db.sqlite3
python manage.py migrate
```

### Frontend Issues

**"Port 5173 already in use":**
```bash
# Kill process on port 5173
lsof -i :5173
kill -9 <PID>
```

**"Cannot find module X":**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

---

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

**Full API documentation:** [docs/API.md](docs/API.md)

---

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

---

## 🔒 Security Features

- **No plain text storage** - Passwords are never stored
- **K-anonymity** - HIBP queries only send hash prefix
- **JWT with refresh** - Secure, stateless authentication
- **CORS configured** - Restricted to allowed origins
- **Input validation** - All inputs sanitized via serializers

---

## 📚 Documentation

- [**Tech Stack Deep Dive**](docs/TECH_STACK.md) - Detailed explanation of all technologies
- [**Architecture Overview**](docs/ARCHITECTURE.md) - System design and data flow
- [**API Reference**](docs/API.md) - Complete REST API documentation

---

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

---

## 🚧 Future Improvements

- [ ] Password generator
- [ ] Two-factor authentication
- [ ] Browser extension
- [ ] Export reports (PDF)
- [ ] Dark/light theme toggle
- [ ] Internationalization (i18n)

---

## 👨‍💻 Author

**Kelson Brito**
- LinkedIn: [kelson-brito](https://www.linkedin.com/in/kelson-brito-ba922b363)
- GitHub: [@kelsonbrito50](https://github.com/kelsonbrito50)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built as a portfolio project to demonstrate full-stack development skills.*
