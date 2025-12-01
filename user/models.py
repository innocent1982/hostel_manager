from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 
from django.contrib.auth import get_user_model
from booking.models import Room


class User(AbstractUser):
    ROLES = [
        ("tenant", "Tenant"),
        ("landlord", "Landlord")
    ]

#    student_id = models.CharField(max_length=10)
    role = models.CharField(choices=ROLES, default="tenant", max_length=8)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=True)
    email_verified = models.BooleanField(default=False)
    email_code = models.CharField(max_length=86)
    rent_due = models.DateTimeField()

    def save(self, validated_data, *args, **kwargs):
        room = self.room 
        if room:
            time = datetime.now()
            due = time + timedelta(months=1)
            self.rent_due = due
        super().save(*args, **kwargs)


