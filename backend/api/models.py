from django.contrib.auth.models import User
from django.db import models


class PasswordCheck(models.Model):
    """
    Stores password check history (only hash prefix, never full password)
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_checks"
    )
    hash_prefix = models.CharField(
        max_length=5, help_text="First 5 chars of SHA1 hash (k-anonymity)"
    )
    label = models.CharField(
        max_length=100, blank=True, help_text="Optional label (e.g., 'Gmail password')"
    )
    strength_score = models.IntegerField(default=0, help_text="0-100 strength score")
    is_breached = models.BooleanField(default=False)
    breach_count = models.IntegerField(default=0, help_text="Times found in breaches")
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-checked_at"]

    def __str__(self):
        return f"{self.label or 'Unlabeled'} - {self.user.username}"


class UserStats(models.Model):
    """
    Aggregated statistics for dashboard
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    total_checks = models.IntegerField(default=0)
    breached_count = models.IntegerField(default=0)
    avg_strength = models.FloatField(default=0.0)
    last_check = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Stats for {self.user.username}"
