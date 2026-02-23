"""Pytest configuration and shared fixtures."""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123!'
    )


@pytest.fixture
def authenticated_client(client, user):
    """Return an authenticated test client."""
    client.force_login(user)
    return client


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='AdminPassword123!'
    )
