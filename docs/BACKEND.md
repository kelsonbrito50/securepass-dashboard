# Backend Development Guide

## Stack

- **Framework:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL 15
- **Auth:** JWT (SimpleJWT)
- **External API:** HIBP (Have I Been Pwned)

## App Structure

```
backend/
├── core/           # Project settings, URL router
│   ├── settings.py
│   └── urls.py
├── authentication/ # JWT auth, user registration/login
├── passwords/      # Password strength + HIBP check
├── users/          # User profile management
└── conftest.py     # Pytest shared fixtures
```

## HIBP Integration

Password breach checking uses k-anonymity to protect user privacy:

1. Hash password with SHA-1
2. Send first 5 chars to HIBP API
3. Compare full hash locally
4. Never sends the full password or hash to HIBP

```python
import hashlib
import requests

def check_hibp(password: str) -> int:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
    # count occurrences
    ...
```

## Running Dev Server

```bash
cd backend
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```
