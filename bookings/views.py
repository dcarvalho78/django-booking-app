from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from services.models import Service
from .models import Booking

TAX_RATE = Decimal("0.10")


@login_required
def booking_form(request, pk):
    service = get_object_or_404(Service, pk=pk)

    booked_ranges = (
        Booking.objects
        .filter(service=service, start_date__isnull=False, end_date__isnull=False)
        .values("start_date", "end_date")
    )

    if request.method == "POST":
        start_raw = request.POST.get("start_date")
        end_raw = request.POST.get("end_date")

        try:
            start_date = date.fromisoformat(start_raw)
            end_date = date.fromisoformat(end_raw)
        except Exception:
            messages.error(request, "Please choose valid dates.")
            return render(request, "bookings/booking_form.html", {
                "service": service,
                "booked_ranges": booked_ranges,
            })

        today = timezone.localdate()
        if start_date < today:
            messages.error(request, "Start date cannot be in the past.")
            return render(request, "bookings/booking_form.html", {
                "service": service,
                "booked_ranges": booked_ranges,
                "start_value": start_date.isoformat(),
                "end_value": end_date.isoformat(),
            })

        if end_date < start_date:
            messages.error(request, "End date cannot be before start date.")
            return render(request, "bookings/booking_form.html", {
                "service": service,
                "booked_ranges": booked_ranges,
                "start_value": start_date.isoformat(),
                "end_value": end_date.isoformat(),
            })

        overlap = Booking.objects.filter(
            service=service,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()
        if overlap:
            messages.error(request, "This period is already booked.")
            return render(request, "bookings/booking_form.html", {
                "service": service,
                "booked_ranges": booked_ranges,
                "start_value": start_date.isoformat(),
                "end_value": end_date.isoformat(),
            })

        booking = Booking.objects.create(
            user=request.user,
            service=service,
            start_date=start_date,
            end_date=end_date,
        )
        return redirect("order_success", booking_id=booking.id)

    return render(request, "bookings/booking_form.html", {
        "service": service,
        "booked_ranges": booked_ranges,
    })


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("service")
        .order_by("-created_at")
    )

    total_spent = Decimal("0.00")
    today = timezone.localdate()

    for b in bookings:
        if b.start_date and b.end_date and b.service and b.service.price is not None:
            days = (b.end_date - b.start_date).days + 1
            price_per_day = Decimal(b.service.price)
            subtotal = price_per_day * days
            tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
            total = (subtotal + tax).quantize(Decimal("0.01"))
        else:
            days = 0
            subtotal = Decimal("0.00")
            tax = Decimal("0.00")
            total = Decimal("0.00")

        b.computed_days = days
        b.computed_subtotal = subtotal
        b.computed_tax = tax
        b.computed_total = total
        total_spent += total

    stats = {
        "total_bookings": bookings.count(),
        "total_spent": total_spent.quantize(Decimal("0.01")),
        "upcoming_bookings": bookings.filter(start_date__gte=today).count(),
    }

    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings,
        "stats": stats,
    })


@login_required
def order_success(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("service"),
        pk=booking_id,
        user=request.user,
    )

    if booking.start_date and booking.end_date and booking.service and booking.service.price is not None:
        days = (booking.end_date - booking.start_date).days + 1
        price_per_day = Decimal(booking.service.price)
        subtotal = price_per_day * days
        tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
        total = (subtotal + tax).quantize(Decimal("0.01"))
    else:
        days = 0
        price_per_day = None
        subtotal = Decimal("0.00")
        tax = Decimal("0.00")
        total = Decimal("0.00")

    return render(request, "bookings/order_success.html", {
        "booking": booking,
        "days": days,
        "price_per_day": price_per_day,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "tax_rate_percent": int(TAX_RATE * 100),
    })
