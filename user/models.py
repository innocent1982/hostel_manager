from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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
    image = models.ImageField(upload_to="images/locations")
    description = models.CahrField(max_length=500)
    rooms = models.IntegerField()
    capacity = models.IntegerField()


class Room(models.Model):
    ROOM_STATUS = [
        ("occupied", "Occupied"),
        ("free", "Free"),
        ("unavailabe", "Unavailable")
    ]
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number = models.IntegerField()
    capacity = models.IntegerField()
    occupants = models.ManyToManyField(User, blank=True)
    status = models.CharField(choices = ROOM_STATUS, max_length=11, default="free", null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def add_occupant(self, user):
        if self.occupants.count() >= 2:
            raise ValidationError("Room is full")
        self.occupants.add(user)

