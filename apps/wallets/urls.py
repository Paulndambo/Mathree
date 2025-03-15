from django.urls import path

from apps.wallets.views import (
    WalletAPIView,
    WalletRechargeAPIView,
    WalletTransferAPIView,
)

urlpatterns = [
    path("", WalletAPIView.as_view(), name="wallets"),
    path("recharge-wallet/", WalletRechargeAPIView.as_view(), name="recharge-wallet"),
    path("wallet-transfer/", WalletTransferAPIView.as_view(), name="wallet-transfer"),
]
