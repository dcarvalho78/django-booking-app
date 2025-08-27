from django.contrib import admin
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','user','service','created_at')
    list_filter = ('created_at',)
