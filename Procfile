web: bash -c 'cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn securepass.wsgi:application --bind 0.0.0.0:$PORT'
