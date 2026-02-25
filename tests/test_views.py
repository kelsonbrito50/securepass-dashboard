"""
Integration tests for API endpoints.
Tests registration, JWT auth, password checking, history, and stats.
"""
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_tokens(client, username="testuser", password="TestPassword123!"):
    """Return access token for the given credentials."""
    resp = client.post(
        "/api/auth/login/",
        {"username": username, "password": password},
        format="json",
    )
    return resp.data.get("access")


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestHealthEndpoint:
    def test_health_returns_ok(self):
        client = APIClient()
        resp = client.get("/api/health/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRegisterView:
    def test_register_new_user(self):
        client = APIClient()
        resp = client.post(
            "/api/auth/register/",
            {"username": "newuser", "password": "Strong@Pass1", "email": "new@example.com"},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_register_duplicate_username(self):
        User.objects.create_user("existing", password="pass")
        client = APIClient()
        resp = client.post(
            "/api/auth/register/",
            {"username": "existing", "password": "Str0ng@Pass"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ---------------------------------------------------------------------------
# JWT login
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestLoginView:
    def test_valid_login_returns_tokens(self, user):
        client = APIClient()
        resp = client.post(
            "/api/auth/login/",
            {"username": "testuser", "password": "TestPassword123!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data
        assert "refresh" in resp.data

    def test_invalid_credentials_rejected(self):
        client = APIClient()
        resp = client.post(
            "/api/auth/login/",
            {"username": "nobody", "password": "wrong"},
            format="json",
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ---------------------------------------------------------------------------
# Quick Check (anonymous)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestQuickCheckView:
    @patch("api.views.check_hibp_breach", return_value=(False, 0))
    def test_quick_check_returns_strength(self, mock_hibp):
        client = APIClient()
        resp = client.post(
            "/api/passwords/quick-check/",
            {"password": "Tr0ub4dor&3xPlorer!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "score" in resp.data
        assert "strength" in resp.data
        assert "feedback" in resp.data
        assert "is_breached" in resp.data

    def test_quick_check_empty_password(self):
        client = APIClient()
        resp = client.post("/api/passwords/quick-check/", {"password": ""}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_quick_check_missing_password(self):
        client = APIClient()
        resp = client.post("/api/passwords/quick-check/", {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @patch("api.views.check_hibp_breach", return_value=(True, 999))
    def test_quick_check_detects_breach(self, mock_hibp):
        client = APIClient()
        resp = client.post(
            "/api/passwords/quick-check/",
            {"password": "password"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["is_breached"] is True
        assert resp.data["breach_count"] == 999


# ---------------------------------------------------------------------------
# Authenticated Password Check
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPasswordCheckView:
    @patch("api.views.check_hibp_breach", return_value=(False, 0))
    def test_authenticated_check_saved_to_history(self, mock_hibp, user):
        client = APIClient()
        token = get_tokens(client)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        resp = client.post(
            "/api/passwords/check/",
            {"password": "Tr0ub4dor&3xPlorer!", "label": "Test label"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["label"] == "Test label"
        assert "score" in resp.data
        assert "id" in resp.data

    def test_unauthenticated_check_rejected(self):
        client = APIClient()
        resp = client.post(
            "/api/passwords/check/",
            {"password": "SomePassword1!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("api.views.check_hibp_breach", return_value=(False, 0))
    def test_check_missing_password_field(self, mock_hibp, user):
        client = APIClient()
        token = get_tokens(client)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        resp = client.post("/api/passwords/check/", {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ---------------------------------------------------------------------------
# Password History
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPasswordHistoryView:
    def test_unauthenticated_history_rejected(self):
        client = APIClient()
        resp = client.get("/api/passwords/history/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("api.views.check_hibp_breach", return_value=(False, 0))
    def test_history_returns_own_records(self, mock_hibp, user):
        client = APIClient()
        token = get_tokens(client)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Create a record first
        client.post(
            "/api/passwords/check/",
            {"password": "Tr0ub4dor&3xPlorer!"},
            format="json",
        )

        resp = client.get("/api/passwords/history/")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data) >= 1


# ---------------------------------------------------------------------------
# User Stats
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestUserStatsView:
    def test_unauthenticated_stats_rejected(self):
        client = APIClient()
        resp = client.get("/api/stats/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_stats_returns_dashboard_data(self, user):
        client = APIClient()
        token = get_tokens(client)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        resp = client.get("/api/stats/")
        assert resp.status_code == status.HTTP_200_OK
        for key in ("total_checks", "breached_count", "avg_strength", "strength_distribution"):
            assert key in resp.data, f"Missing key: {key}"
