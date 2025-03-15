from datetime import datetime

from django.shortcuts import render
from django.db import transaction

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from apps.core.constants import UserRole

from apps.users.models import User
from apps.wallets.models import Wallet


from apps.users.serializers import (
    UsersSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

date_today = datetime.now().date()


# Create your views here.
class UsersAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-created_on")
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all().order_by("-created_on")
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()

            wallet = Wallet.objects.create(owner=user)
            wallet_address = (
                f"WLT{user.id}{date_today.day}{date_today.month}{date_today.year}"
            )
            wallet.address = wallet_address
            wallet.save()

            return Response(
                {"message": "User account created successfully!!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
