# Contributing to SecurePass Dashboard

Thank you for your interest in contributing! Here's how to get involved.

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/securepass-dashboard.git
   cd securepass-dashboard
   ```
3. Set the upstream remote:
   ```bash
   git remote add upstream https://github.com/kelsonbrito50/securepass-dashboard.git
   ```

---

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # edit as needed
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Branching Strategy

| Branch type | Pattern | Example |
|---|---|---|
| Feature | `feat/<description>` | `feat/password-export` |
| Bug fix | `fix/<description>` | `fix/token-refresh` |
| Docs | `docs/<description>` | `docs/api-reference` |
| CI/Chore | `ci/<description>` or `chore/<description>` | `ci/lint-workflow` |

Always branch from `main` and keep branches short-lived.

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `chore`, `ci`, `test`, `refactor`, `style`

---

## Pull Request Process

1. Ensure tests pass: `pytest` (backend) and `npm test` (frontend)
2. Run linters: `flake8 backend/` and `npm run lint`
3. Open a PR against `main` with a clear description
4. Request a review — at least one approval is required before merging

---

## Code Style

- **Python:** PEP 8 (enforced by `flake8` and `black`)
- **JavaScript/JSX:** ESLint + Prettier
- **Commits:** Conventional Commits

---

## Reporting Issues

Please use the [GitHub Issues](https://github.com/kelsonbrito50/securepass-dashboard/issues) page.
Include steps to reproduce, expected vs. actual behavior, and your environment.

---

## Code of Conduct

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
