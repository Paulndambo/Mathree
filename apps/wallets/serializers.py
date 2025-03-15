from rest_framework import serializers

from apps.wallets.models import Wallet, WalletTransaction


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField()
    transactions = WalletTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = "__all__"


class RechargeWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class WalletTransferSerializer(serializers.Serializer):
    destination_address = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
