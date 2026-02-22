web: cd backend && python manage.py migrate --noinput && gunicorn securepass.wsgi:application --bind 0.0.0.0:$PORT
