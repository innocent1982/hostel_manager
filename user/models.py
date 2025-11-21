from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ("tenant", "Tenant"),
        ("landlord", "Landlord")
    ]

    student_id = models.CharField(max_length=10)
    role = models.CharField(choices=ROLES, default="tenant", max_length=8)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=True)
    email_verified = models.BooleanField(default=False)
    email_code = models.CharField(max_length=86)


class Location(models.Model):
    name = models.CharField(max_length=20)
    description = models.CahrField(max_length=200)
    rooms = models.IntegerField()
    capacity = models.IntegerField()


class Room(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number = models.IntegerField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
