from rest_framework import serializers

from apps.matatus.models import Sacco, Bus, Route, BusTrip


class SaccoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sacco
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class BusTripSerializer(serializers.ModelSerializer):
    route_name = serializers.ReadOnlyField()
    vehicle = serializers.ReadOnlyField()
    available_tickets = serializers.ReadOnlyField()
    start_point = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    trip_time = serializers.SerializerMethodField()
    trip_date = serializers.SerializerMethodField()


    class Meta:
        model = BusTrip
        fields = "__all__"

    def get_start_point(self, obj):
        return obj.route.starts_from

    def get_destination(self, obj):
        return obj.route.destination
    
    def get_trip_time(self, obj):
        return obj.time.time()
    
    def get_trip_date(self, obj):
        return obj.time.date()

