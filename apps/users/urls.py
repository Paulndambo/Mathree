from django.urls import path

from apps.users.views import UsersAPIView, UserRegistrationAPIView, UserProfileAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("", UsersAPIView.as_view(), name="users"),
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token"),
    path("verify-token/", TokenVerifyView.as_view(), name="verify-token"),
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
]
