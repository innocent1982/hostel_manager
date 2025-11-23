from django.urls import Path
from rest_framwork_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView
)
from .views import UserView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token-verify/', TokenVerifyView.as_view()),
    path('auth/token-refresh/', TokenRefreshView.as_view()),
    path('user/create/', UserView.as_view())
]
