from django.shortcuts import render
from django.db import transaction

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.core.constants import TransactionType

from apps.wallets.models import Wallet, WalletTransaction
from apps.wallets.serializers import (
    WalletSerializer,
    WalletTransactionSerializer,
    WalletTransferSerializer,
    RechargeWalletSerializer,
)

# Create your views here.
class WalletAPIView(generics.ListAPIView):
    queryset = Wallet.objects.all().order_by("-created_on")
    serializer_class = WalletSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Wallet.objects.all().order_by("-created_on")

        return Wallet.objects.filter(owner=user)


class WalletTransferAPIView(generics.CreateAPIView):
    serializer_class = WalletTransferSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid(raise_exception=True):
            destination_address = serializer.validated_data.get("destination_address")
            amount = serializer.validated_data.get("amount")

            source_wallet = Wallet.objects.get(owner=user)
            destination_wallet = Wallet.objects.get(address=destination_address)

            if not source_wallet or not destination_wallet:
                return Response(
                    {
                        "failed": "The wallet you are trying to transfer to does not exist"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if source_wallet.balance >= 0 and source_wallet.balance >= amount:
                source_wallet.balance -= amount
                destination_wallet.balance += amount
                destination_wallet.save()
                source_wallet.save()
                WalletTransaction.objects.create(
                    wallet=source_wallet,
                    transaction_type=TransactionType.TRANSFER.value,
                    amount=-amount,
                )
                WalletTransaction.objects.create(
                    wallet=destination_wallet,
                    transaction_type=TransactionType.TRANSFER.value,
                    amount=amount,
                )
                return Response(
                    {"message": "Transaction was successful!!"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "failed": f"You have insufficient funds to be able to transfer {amount}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletRechargeAPIView(generics.CreateAPIView):
    serializer_class = RechargeWalletSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid(raise_exception=True):
            amount = serializer.validated_data.get("amount")

            if amount <= 0:
                return Response({"failed": "Amount must be greater than zero"})

            wallet = Wallet.objects.get(owner=user)
            wallet.balance += amount
            wallet.save()

            WalletTransaction.objects.create(
                wallet=wallet,
                transaction_type=TransactionType.RECHARGE.value,
                amount=amount,
            )
            return Response(
                {"message": "Recharge was successfull"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
