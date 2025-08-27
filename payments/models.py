from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    STATUS = [('pending','pending'), ('paid','paid'), ('failed','failed')]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.pk} ({self.status})"
