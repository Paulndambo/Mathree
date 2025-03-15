from decimal import Decimal
from django.shortcuts import render
from django.db import transaction

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.bookings.models import Booking
from apps.matatus.models import BusTrip
from apps.bookings.serializers import BookingSerializer, BookTicketSerializer
from apps.wallets.models import Wallet
from apps.core.constants import BookingStatus


# Create your views here.
class BookingAPIView(generics.ListAPIView):
    queryset = Booking.objects.all().order_by("-created_on")
    serializer_class = BookingSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all().order_by("-created_on")
        return Booking.objects.filter(user=self.request.user).order_by("-created_on")


class BookBusTicketAPIView(generics.CreateAPIView):
    serializer_class = BookTicketSerializer

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            trip_id = serializer.validated_data.get("trip")
            number_of_seats = serializer.validated_data.get("number_of_seats")
            total_amount = serializer.validated_data.get("total_amount")

            trip = BusTrip.objects.get(id=trip_id)

            available_tickets = trip.total_tickets - trip.tickets_purchased

            if available_tickets < int(number_of_seats) or available_tickets <= 0:
                return Response(
                    {
                        "failed": "This bus does not have the number of seats you need, try another one"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            wallet = Wallet.objects.get(owner=user)

            if wallet.balance < total_amount:
                return Response(
                    {"failed": "Wallet balance is too low"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            booking = Booking.objects.create(user=user, trip=trip, amount=total_amount)

            booking.trip.tickets_purchased += number_of_seats
            booking.trip.amount_raised += booking.amount
            booking.trip.save()

            if booking.trip.tickets_purchased == booking.trip.total_tickets:
                booking.trip.fully_booked = True
                booking.trip.save()

            wallet.pay(total_amount)
            booking.status = BookingStatus.PAID.value
            booking.save()

            return Response(
                {"message": "Seats successfully reserved!!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)