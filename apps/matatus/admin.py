from django.contrib import admin

from apps.matatus.models import Sacco, Route, Bus, BusTrip
# Register your models here.
@admin.register(Sacco)
class SaccoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'country', 'merchant_code']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'starts_from', 'destination']


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['id', 'sacco', 'plate_number', 'capacity']


@admin.register(BusTrip)
class BusTripAdmin(admin.ModelAdmin):
    list_display = ['id', 'route', 'bus', 'total_tickets', 'tickets_purchased', 'fully_booked', 'amount_raised', 'time', 'fare', 'completed']
    