# Architecture

## Backend (Django REST)
- Django 5.x + Django REST Framework
- JWT authentication
- PostgreSQL (Railway)
- HIBP breach detection (k-anonymity)

## Frontend (React)
- React 18 + TailwindCSS
- Chart.js for data visualization
- React Context for state management
- GitHub Pages hosting

## API Flow
1. User submits password → Backend analyzes strength
2. Backend checks HIBP via k-anonymity (safe)
3. Returns score + breach status + recommendations
