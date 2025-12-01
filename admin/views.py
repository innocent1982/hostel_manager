from rest_framework.views import APIView
from booking.models import Booking
from api.serializers import BookingSerializer
from rest_framework.response import Response


def get_bookings(self, request, *args, **kwargs):
    pending_bookings = Bookings.objects.filter(status="pending")
    serializer = BookingSerializer(data=pending_bookings, many=True)
    if pending_bookings:
        if serializer.is_valid():
            data = serializer.data
            return Response({"bookings":data}, status=200)
        else:
            return 


