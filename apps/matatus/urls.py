from django.urls import path
from apps.matatus.views import (
    SaccoAPIView,
    SaccoDetailAPIView,
    RouteAPIView,
    RouteDetailAPIView,
    BusAPIView,
    BusDetailAPIView,
    BusTripAPIView,
    BusTripDetailAPIView,
)


urlpatterns = [
    path("saccos/", SaccoAPIView.as_view(), name="saccos"),
    path("saccos/<int:pk>/", SaccoDetailAPIView.as_view(), name="sacco-details"),
    path("routes/", RouteAPIView.as_view(), name="routes"),
    path("routes/<int:pk>/", RouteDetailAPIView.as_view(), name="route-details"),
    path("buses/", BusAPIView.as_view(), name="buses"),
    path("buses/<int:pk>/", BusDetailAPIView.as_view(), name="bus-details"),
    path("trips/", BusTripAPIView.as_view(), name="trips"),
    path("trips/<int:pk>/", BusTripDetailAPIView.as_view(), name="trip-details"),
]
