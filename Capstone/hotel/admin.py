from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(RoomTypePrice)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Booking)