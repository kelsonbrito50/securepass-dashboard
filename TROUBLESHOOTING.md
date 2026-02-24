# Troubleshooting

## Backend Issues
### Database connection failed
- Check DATABASE_URL in .env
- Ensure Railway PostgreSQL is running

### Migrations error
- Run `python manage.py migrate`

## Frontend Issues
### API connection error
- Verify REACT_APP_API_URL points to backend
- Check CORS settings in Django

### Build fails
- Clear node_modules: `rm -rf node_modules && npm install`
