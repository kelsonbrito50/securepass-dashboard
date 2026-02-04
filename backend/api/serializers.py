from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PasswordCheck, UserStats


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        # Create stats for new user
        UserStats.objects.create(user=user)
        return user


class PasswordCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordCheck
        fields = ['id', 'label', 'strength_score', 'is_breached', 'breach_count', 'checked_at']
        read_only_fields = ['id', 'strength_score', 'is_breached', 'breach_count', 'checked_at']


class PasswordCheckRequestSerializer(serializers.Serializer):
    """For incoming password check requests"""
    password = serializers.CharField(write_only=True, min_length=1)
    label = serializers.CharField(max_length=100, required=False, allow_blank=True)


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = ['total_checks', 'breached_count', 'avg_strength', 'last_check']


class PasswordStrengthResponseSerializer(serializers.Serializer):
    """Response for password strength check"""
    score = serializers.IntegerField()
    strength = serializers.CharField()  # weak, fair, good, strong, very_strong
    feedback = serializers.ListField(child=serializers.CharField())
    is_breached = serializers.BooleanField()
    breach_count = serializers.IntegerField()
    criteria = serializers.DictField()
