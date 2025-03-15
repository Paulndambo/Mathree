from django.db import models

from apps.core.models import AbstractBaseModel


# Create your models here.
class Sacco(AbstractBaseModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    merchant_code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Route(AbstractBaseModel):
    name = models.CharField(max_length=255)
    starts_from = models.CharField(max_length=255, null=True)
    destination = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Bus(AbstractBaseModel):
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=255)
    capacity = models.IntegerField(default=1)

    def __str__(self):
        return self.plate_number


class BusTrip(AbstractBaseModel):
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    total_tickets = models.IntegerField(default=0)
    tickets_purchased = models.IntegerField(default=0)
    fully_booked = models.BooleanField(default=False)
    amount_raised = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    time = models.DateTimeField(null=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.route.name} ({self.bus.plate_number})"

    def route_name(self):
        return self.route.name

    def vehicle(self):
        return self.bus.plate_number

    def available_tickets(self):
        return self.total_tickets - self.tickets_purchased
