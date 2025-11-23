from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, BookingSerializer, PaymentSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.models import Room
import requests
from rest_framework.decorators import api_view
from booking.models import Booking, Payment
import os
from rest_framework.status import status


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request_method == "POST":
            return [AllowAny()]

        return [permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        user_data = request.data 
        serializer = UserSerializer(user_data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data 
            return Response({"data":data}, status=201)
        return Response({"eror":serializer.errors}, status=400)


@api_view(['GET'])
def trigger_payment(request):
    url = "https://paychangu.com/payments/initiate"
    user = request.user 
    booking = Booking.objects.get(user=user)
    if booking:
        payment_data = {
            "amount":booking.cost,
            "email":booking.user.email,
            "currency":"MKW",
            "tx_ref":booking.tx_ref,
            "callback_url":"http://127.0.0.1:8000/api/booking/verify-payment"
        }
    headers = {
        "content-type":"application/json",
        "Authorization": f"Bearer {os.environ["PAYCHANGU_API_KEY"]}"
    }
    response = requests.post(url, headers=headers, json=payment_data)
    if response.status_code == HTTP_200_OK:
        data = {
            "booking":booking.id,
            "amount":booking.cost,
            "status":"pending",
        }
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        payment_url = response.json()["payment_url"]
        return Response({"url":payment_url}, status=200)
    else:
        return Response({"error":"failed to initiate payment"}, status=400)


from datetime import datetime
class PaymentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = booking.user
        booking = Booking.objects.get(tx_ref=data["tx_ref"])
        if booking:
            url = "https://paychangu.com/verify"
            params = {
                "transaction_id":data.transaction_id
            }
            headers = {
                "content-type":"application/json",
                "Authorization": f"Bearer {os.environ["PAYCHANGU_API_KEY"]}"
            }
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == HTTP_200_OK:
                payment = Payment.objects.get(booking=booking.id)
                payment.status = "approved"
                payment.paid_at = datetime.now()
                payment.save()
                booking.status = "approved"
                room = booking.room
                try:
                    room.add_occupant(user)
                    return Response({"succes":f"Sucessfully assigned to room {room.number}"}, status=201)
                except Exception as e:
                    print(f"Error while assigning user to room: {str(e)}")
                    return Response({"Failure":f"Failed to assign user to room {room.number}"}, status=400)


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data 
        room = Room.objects.get(location=data["location"], number=data["number"])
        if room.status == "unavailable" or room.status == "occupied":
            return Response({"error":"Room unavailable"}, status=400)
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, cost=room.price, status="pending")
            return Response({"data":serializer.data}, status=201)
        return Response({"error":"Failed to book desired room"}, status=400)
