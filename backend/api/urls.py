from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    PasswordCheckView,
    QuickCheckView,
    PasswordHistoryView,
    UserStatsView,
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password checking
    path('passwords/check/', PasswordCheckView.as_view(), name='password_check'),
    path('passwords/quick-check/', QuickCheckView.as_view(), name='quick_check'),
    path('passwords/history/', PasswordHistoryView.as_view(), name='password_history'),
    
    # Dashboard
    path('stats/', UserStatsView.as_view(), name='user_stats'),
]
