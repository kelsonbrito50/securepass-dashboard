"""
Unit tests for Django models.
"""

import pytest
from api.models import PasswordCheck, UserStats


@pytest.mark.django_db
class TestPasswordCheckModel:
    def test_create_password_check(self, user):
        check = PasswordCheck.objects.create(
            user=user,
            hash_prefix="ABCDE",
            label="Gmail",
            strength_score=85,
            is_breached=False,
            breach_count=0,
        )
        assert check.pk is not None
        assert check.hash_prefix == "ABCDE"
        assert str(check) == "Gmail - testuser"

    def test_unlabeled_check_str(self, user):
        check = PasswordCheck.objects.create(
            user=user,
            hash_prefix="12345",
            strength_score=40,
        )
        assert "Unlabeled" in str(check)

    def test_ordering_is_newest_first(self, user):
        _ = PasswordCheck.objects.create(
            user=user, hash_prefix="00001", strength_score=10
        )
        c2 = PasswordCheck.objects.create(
            user=user, hash_prefix="00002", strength_score=20
        )
        checks = list(PasswordCheck.objects.filter(user=user))
        assert checks[0].pk == c2.pk  # newest first

    def test_cascade_delete(self, user):
        PasswordCheck.objects.create(user=user, hash_prefix="AAAAA", strength_score=50)
        user_id = user.pk
        user.delete()
        assert PasswordCheck.objects.filter(user_id=user_id).count() == 0


@pytest.mark.django_db
class TestUserStatsModel:
    def test_create_user_stats(self, user):
        stats = UserStats.objects.create(
            user=user,
            total_checks=10,
            breached_count=2,
            avg_strength=65.5,
        )
        assert stats.pk is not None
        assert "testuser" in str(stats)

    def test_one_to_one_constraint(self, user):
        UserStats.objects.create(user=user)
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            UserStats.objects.create(user=user)

    def test_get_or_create_stats(self, user):
        stats, created = UserStats.objects.get_or_create(user=user)
        assert created is True
        stats2, created2 = UserStats.objects.get_or_create(user=user)
        assert created2 is False
        assert stats.pk == stats2.pk
