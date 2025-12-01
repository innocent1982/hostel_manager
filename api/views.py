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
from rest_framework import status


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


class RoomView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.filter(status="free")
        if rooms:
            boys = RoomSerializer(data=rooms.objects.filter(location="boys"), many=True)
            bus = RoomSerializer(data=rooms.objects.filter(location="bus"), many=True)
            mansion = RoomSerializer(data=rooms.objects.filter(location="mansion"), many=True)
            ngombe = RoomSerializer(data=rooms.objects.filter(location="ngombe"), many=True)

            data = {
                "boys":boys,
                "bus":bus,
                "mansion":mansion,
                "ngombe":ngombe
            }
            return Response({"data":data}, status=200)
        else:
            return Response({"error":"All rooms are occupied"}, status=400)



@api_view(['GET'])
def trigger_payment(request):
    url = "https://paychangu.com/payments/initiate" 
    booking = Booking.objects.get(email=request.data[email])
    if booking:
        payment_data = {
            "amount":booking.amount,
            "email":booking.email,
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
            send_mail(
                subject="Complete payment for room at Angonia",
                message=f"Click the link to finish paying up for room {payment_url}",
                send_mail="innocentkamesa05@gmail.com",
                recipient_list = [booking.email],
                fail_silently=False
            )
            return Response({"url":payment_url}, status=200)
    else:
        return Response({"error":"failed to initiate payment, Booking not found"}, status=400)

import secrets
import string

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


from datetime import datetime
class PaymentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
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
                booking.save()
            
                try:
                    room = Room.objects.get(number=booking.room)
                    name = booking.name
                    email = booking.email
                    phone = booking.phone
                    password = generate_password()
                    serializer = UserSerializer(data={"username":name, "password":password, "email":email, "phone":phone})
                    if serializer.is_valid():
                        serializer.save(room=room)
                        data = serializer.data
                        room.add_occupant(data.id)
                        send_mail(
                            subject= "Successful user creation",
                            message=f"""
                            You were successfully assigned to room {room.number}. The following are your account details,
                            You can change them anytime:
                            username: {data.username}
                            password: {password}
                            email: {data.email}
                            """,
                            from_email = "innocentkamesa05@gmail.com",
                            recipient_list = [data.email],
                            fail_silently=False
                        )
                        return Response({"mesage":"Successfully registered"}, status=200)
           
                    return Response({"error":f"Failed to create user account {serializer.errors}"}, status=404)
                except Exception as e:
                    print(f"Error while assigning user to room: {str(e)}")
                    return Response({"Failure":f"Failed to assign user to room {room.number}"}, status=400)
            else:
                booking.status = "failed"
                return Response({"error, payment verrification failed"}, status=400)

    
class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data 
        room = Room.objects.get(number=data["number"])
        if room.status == "unavailable" or room.status == "occupied":
            return Response({"error":"Room unavailable"}, status=400)
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(amount=room.price, status="pending")
            return Response({"data":serializer.data}, status=201)
        return Response({"error":"Failed to book desired room"}, status=400)
