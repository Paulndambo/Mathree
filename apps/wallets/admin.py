from django.contrib import admin

from apps.wallets.models import Wallet, WalletTransaction


# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "owner", "balance"]


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "wallet", "transaction_type", "amount"]
