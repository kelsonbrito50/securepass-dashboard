from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.utils import timezone

from .models import PasswordCheck, UserStats
from .serializers import (
    UserSerializer, 
    PasswordCheckSerializer,
    PasswordCheckRequestSerializer,
    UserStatsSerializer,
    PasswordStrengthResponseSerializer,
)
from .services import (
    calculate_password_strength,
    check_hibp_breach,
    get_hash_prefix,
)


class RegisterView(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class PasswordCheckView(APIView):
    """
    Check password strength and breach status
    POST: Analyze a password and save to history
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordCheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        password = serializer.validated_data['password']
        label = serializer.validated_data.get('label', '')
        
        # Calculate strength
        strength_result = calculate_password_strength(password)
        
        # Check breach status
        is_breached, breach_count = check_hibp_breach(password)
        
        # Save to history (only hash prefix for privacy)
        password_check = PasswordCheck.objects.create(
            user=request.user,
            hash_prefix=get_hash_prefix(password),
            label=label,
            strength_score=strength_result['score'],
            is_breached=is_breached,
            breach_count=breach_count,
        )
        
        # Update user stats
        self._update_user_stats(request.user)
        
        # Build response
        response_data = {
            'id': password_check.id,
            'score': strength_result['score'],
            'strength': strength_result['strength'],
            'feedback': strength_result['feedback'],
            'criteria': strength_result['criteria'],
            'is_breached': is_breached,
            'breach_count': breach_count,
            'label': label,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    def _update_user_stats(self, user):
        """Update aggregated user statistics"""
        stats, created = UserStats.objects.get_or_create(user=user)
        
        checks = PasswordCheck.objects.filter(user=user)
        stats.total_checks = checks.count()
        stats.breached_count = checks.filter(is_breached=True).count()
        stats.avg_strength = checks.aggregate(
            avg=models.Avg('strength_score')
        )['avg'] or 0
        stats.last_check = timezone.now()
        stats.save()


class QuickCheckView(APIView):
    """
    Quick password check without saving (no auth required)
    Good for anonymous/demo users
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        password = request.data.get('password', '')
        if not password:
            return Response(
                {'error': 'Password is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate strength
        strength_result = calculate_password_strength(password)
        
        # Check breach status
        is_breached, breach_count = check_hibp_breach(password)
        
        response_data = {
            'score': strength_result['score'],
            'strength': strength_result['strength'],
            'feedback': strength_result['feedback'],
            'criteria': strength_result['criteria'],
            'is_breached': is_breached,
            'breach_count': breach_count,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class PasswordHistoryView(generics.ListAPIView):
    """Get user's password check history"""
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordCheckSerializer
    
    def get_queryset(self):
        return PasswordCheck.objects.filter(user=self.request.user)[:50]


class UserStatsView(APIView):
    """Get user's security statistics for dashboard"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stats, created = UserStats.objects.get_or_create(user=request.user)
        
        # Get additional stats
        checks = PasswordCheck.objects.filter(user=request.user)
        
        # Strength distribution
        strength_dist = {
            'weak': checks.filter(strength_score__lt=30).count(),
            'fair': checks.filter(strength_score__gte=30, strength_score__lt=50).count(),
            'good': checks.filter(strength_score__gte=50, strength_score__lt=70).count(),
            'strong': checks.filter(strength_score__gte=70, strength_score__lt=90).count(),
            'very_strong': checks.filter(strength_score__gte=90).count(),
        }
        
        # Recent checks
        recent = PasswordCheckSerializer(checks[:5], many=True).data
        
        return Response({
            'total_checks': stats.total_checks,
            'breached_count': stats.breached_count,
            'avg_strength': round(stats.avg_strength, 1),
            'last_check': stats.last_check,
            'strength_distribution': strength_dist,
            'recent_checks': recent,
            'security_score': self._calculate_security_score(stats, strength_dist),
        })
    
    def _calculate_security_score(self, stats, strength_dist):
        """Calculate overall security score (0-100)"""
        if stats.total_checks == 0:
            return 0
        
        # Penalize breached passwords heavily
        breach_penalty = (stats.breached_count / stats.total_checks) * 40
        
        # Reward strong passwords
        strong_ratio = (strength_dist['strong'] + strength_dist['very_strong']) / stats.total_checks
        strong_bonus = strong_ratio * 30
        
        # Base on average strength
        avg_bonus = (stats.avg_strength / 100) * 30
        
        score = max(0, min(100, 100 - breach_penalty + strong_bonus + avg_bonus - 30))
        return round(score, 1)


# Add missing import
from django.db import models
