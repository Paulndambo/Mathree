from rest_framework import serializers

from apps.users.models import User
from apps.wallets.models import Wallet
from apps.wallets.serializers import WalletSerializer

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "gender",
            "gender",
            "password",
            "role",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = "__all__"

    def get_wallet(self, obj):
        wallet = Wallet.objects.filter(owner=obj).first()
        return WalletSerializer(wallet).data
