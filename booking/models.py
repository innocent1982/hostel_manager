from django.db import models
from django.conf import settings
import uuid
#from django.utils import timestamp
from datetime import datetime

User = settings.AUTH_USER_MODEL

class Location(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="images/locations")
    description = models.CharField(max_length=500)
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




class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("failed", "Failed"),
        ("phase2", "phase2")
    ]
    room = models.IntegerField()
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=13)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")
    created_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tx_ref = models.CharField(max_length=100, unique=True, blank=True)

    def save(self):
        if not self.tx_ref:
            self.tx_ref = generate_tx_ref()
        super().save(*args, **kwargs)

    def generate_tx_ref(self):
        prefix = "book"
        time_stamp = int(datetime.now().timestamp())
        uuid = uuid.uuid4().hex[:8].upper()
        return f"{prefix}_{time_stamp}_{uuid}"



class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("failed", "Failed"),
        ("canceled", "Canceled")
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")
    trans_id = models.CharField(max_length=100, null=True, blank=False)
    paid_at = models.DateTimeField(null=True, blank=False)
    created_at = models.DateTimeField()

    def save(self):
        if not self.created_at:
            self.created_at = datetime.now()
        super().save(*args, **kwargs)



