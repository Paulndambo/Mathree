from django.urls import path
from apps.bookings.views import BookingAPIView, BookBusTicketAPIView

urlpatterns = [
    path("", BookingAPIView.as_view(), name="bookings"),
    path("book-ticket/", BookBusTicketAPIView.as_view(), name="book-ticket"),
]
