
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor','Doctor'),
        ('patient','Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    slot = models.ForeignKey(Availability, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
