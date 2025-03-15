from django.db import models

from apps.core.models import AbstractBaseModel
from apps.core.constants import BookingStatus


# Create your models here.
class Booking(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    trip = models.ForeignKey("matatus.BusTrip", on_delete=models.SET_NULL, null=True)
    number_of_seats = models.IntegerField(default=1)
    seat_numbers = models.JSONField(default=list)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    status = models.CharField(
        max_length=255,
        choices=BookingStatus.choices(),
        default=BookingStatus.PENDING.value,
    )

    def __str__(self):
        return self.user.username
