from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models import AbstractBaseModel
from apps.core.constants import UserRole, Gender


# Create your models here.
class User(AbstractBaseModel, AbstractUser):
    role = models.CharField(
        max_length=255, choices=UserRole.choices(), default=UserRole.PASSENGER.value
    )
    gender = models.CharField(max_length=255, choices=Gender.choices(), null=True)
    phone_number = models.CharField(max_length=255, null=True)
    id_number = models.CharField(max_length=255, null=255)
    passport_number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

    def name(self):
        return f"{self.first_name} {self.last_name}"
