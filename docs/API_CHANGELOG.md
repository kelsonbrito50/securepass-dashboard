# API Changelog

Tracks breaking and non-breaking changes to the SecurePass Dashboard API.

## [v1.0.0] - 2024-01-01

### Added
- `POST /api/auth/register/` — User registration
- `POST /api/auth/login/` — JWT login
- `POST /api/auth/logout/` — Logout and token invalidation
- `POST /api/auth/refresh/` — Refresh access token
- `POST /api/passwords/check/` — Check password strength + HIBP
- `GET /api/passwords/history/` — Password check history
- `GET /api/users/me/` — Get current user profile
- `PATCH /api/users/me/` — Update user profile

## Versioning

This API follows [Semantic Versioning](https://semver.org/). Breaking changes increment the major version.

## Deprecation Policy

Deprecated endpoints will be marked in the API docs and removed after 3 months notice.
