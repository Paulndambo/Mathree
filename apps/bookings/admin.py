from django.contrib import admin

from apps.bookings.models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "trip", "number_of_seats", "amount", "status"]
