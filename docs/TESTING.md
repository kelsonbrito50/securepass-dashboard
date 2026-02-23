# Testing Guide

## Overview

This project uses pytest for backend testing.

## Setup

```bash
pip install -r backend/requirements-dev.txt
```

## Running Tests

```bash
# Run all tests
cd backend && pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_passwords.py

# Run specific test
pytest tests/test_passwords.py::TestPasswordStrength::test_strong_password
```

## Test Structure

```
backend/
├── conftest.py          # Shared fixtures
└── tests/
    ├── test_passwords.py    # Password validation tests
    ├── test_auth.py         # Authentication tests
    └── test_hibp.py         # HIBP API integration tests
```

## Writing Tests

```python
import pytest

@pytest.mark.django_db
def test_user_creation(user):
    assert user.email == 'test@example.com'
    assert user.is_active
```

## Coverage Target

Aim for >80% coverage on core business logic.
