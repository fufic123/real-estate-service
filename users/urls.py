from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [    
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('register/', RegistrationAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('verify-email/<str:token>/', VerifyEmailAPI.as_view()),
    path("social/", SocialSettingsAPI.as_view()),
    path("", GetUserAPI.as_view())
]