from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Payment

@login_required
def pay_booking(request, booking_id):
    payment = get_object_or_404(Payment, booking_id=booking_id, booking__user=request.user)
    payment.status = 'paid'
    payment.save()
    messages.success(request, 'Zahlung verbucht. Vielen Dank!')
    return redirect('my_bookings')
