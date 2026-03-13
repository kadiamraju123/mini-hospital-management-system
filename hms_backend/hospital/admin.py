
from django.contrib import admin
from .models import User, Availability, Appointment

admin.site.register(User)
admin.site.register(Availability)
admin.site.register(Appointment)
