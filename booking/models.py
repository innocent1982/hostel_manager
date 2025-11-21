from django.db import models
from user.models import (Room)
from django.conf import settings

User = settings["AUTH_USER_MODEL"]

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("failed", "Failed"),
        ("canceled", "Canceled")
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")
    created_at = model.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("failed", "Failed"),
        ("canceled", "Canceled")
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")
    trans_id = models.CharField(max_length=100)
    paid_at = models.DateTimeField(null=True, blank=False)
    created_at = modes.DateTimeField()

   


