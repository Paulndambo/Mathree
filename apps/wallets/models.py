from datetime import datetime
from django.db import models

from apps.core.models import AbstractBaseModel
from apps.core.constants import TransactionType

date_today = datetime.now().date()


# Create your models here.
class Wallet(AbstractBaseModel):
    owner = models.OneToOneField("users.User", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    address = models.CharField(max_length=255, null=True)

    @property
    def owner_name(self):
        return self.owner.name
    
    def __str__(self):
        return f"{self.owner.username}: {self.address}"

    def pay(self, amount):
        self.balance -= amount
        self.save()

        WalletTransaction.objects.create(
            wallet=self, 
            transaction_type=TransactionType.PAYMENT.value, 
            amount=amount
        )


# Wallet Transaction Model
class WalletTransaction(AbstractBaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=255, choices=TransactionType.choices())
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
