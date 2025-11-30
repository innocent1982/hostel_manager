from rest_framework import serializers
from django.conf import settings
import uuid
from django.core.mail import send_mail
from booking.models import Booking, Payment
from user.models import Room 

User = settings["AUTH_USER_MODEL"] 


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "number", "capactiy", "location"
        ]




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs ={
            "password": {
                "write_only":True
            }
        }

    def create(self, validated_data):
        uuid_token = uuid.uuid4()
        try:
            instance = User.objects.create_user(
                username = validated_data["username"],
                password = validated_data["password"],
                email = validated_data["email"],
                student_id = validated_data["student_id"],
                email_code = str(uuid_token)
            )
            instance.save()
            try:
                url = f"http://127.0.0.1:8000/api/user/verify-email/?token={uuid_token}"
                response = send_mail(
                    subject = "Please verify your email to confirm signing up to Angonia hostels",
                    message = f"Click the link below to verify account:\n {link}",
                    from_email = "innocentkamesa05@gmail.com",
                    recipient_list = [
                        instance.email
                    ],
                    fail_silently = False
                )
            except Exception as e:
                print(f"An error occured while verifying email: {type(e)}")

            return instance

        except Exception as e:
            print(f"An error occured in create user in serializers: {type(e)}")
            raise serializers.ValidationError("Error in serializers create method")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["room", "id", "amount",  "name", "email", "phone", "status"]
        extra_kwargs = {
            "status":{
                "read_only":True 
            },
            "amount":{
                "read_only":True 
            }
        }


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
       "booking", "amount" 
        ]
