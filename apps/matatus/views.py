from django.shortcuts import render
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from apps.matatus.models import Sacco, Route, Bus, BusTrip
from apps.matatus.serializers import (
    SaccoSerializer,
    RouteSerializer,
    BusSerializer,
    BusTripSerializer,
)


# Create your views here.
class SaccoAPIView(generics.ListCreateAPIView):
    queryset = Sacco.objects.all().order_by("-created_on")
    serializer_class = SaccoSerializer

    permission_classes = [IsAdminUser]


class SaccoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sacco.objects.all().order_by("-created_on")
    serializer_class = SaccoSerializer

    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class RouteAPIView(generics.ListCreateAPIView):
    queryset = Route.objects.all().order_by("-created_on")
    serializer_class = RouteSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        return [AllowAny()]


class RouteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all().order_by("-created_on")
    serializer_class = RouteSerializer

    lookup_field = "pk"


class BusAPIView(generics.ListCreateAPIView):
    queryset = Bus.objects.all().order_by("-created_on")
    serializer_class = BusSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get(self, request, *args, **kwargs):
        cache_key = "buses_list"  # Unique cache key
        cached_data = cache.get(cache_key)

        if cached_data:
            # Return cached response if it exists
            return Response(cached_data, status=status.HTTP_200_OK)

        # If no cache, fetch data from the database
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # Cache the response for 5 minutes (300 seconds)
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data, status=status.HTTP_200_OK)


class BusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all().order_by("-created_on")
    serializer_class = BusSerializer

    lookup_field = "pk"


class BusTripAPIView(generics.ListCreateAPIView):
    queryset = BusTrip.objects.all().order_by("-created_on")
    serializer_class = BusTripSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            trip = serializer.save()
            trip.total_tickets = trip.bus.capacity
            trip.save()
            return Response(
                {"message": "Trip successfully created!!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusTripDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusTrip.objects.all().order_by("-created_on")
    serializer_class = BusTripSerializer

    lookup_field = "pk"
