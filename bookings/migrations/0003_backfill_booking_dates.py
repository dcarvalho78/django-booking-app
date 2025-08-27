from django.db import migrations
from django.utils.timezone import now

def backfill_dates(apps, schema_editor):
    Booking = apps.get_model('bookings', 'Booking')
    today = now().date()
    for b in Booking.objects.filter(start_date__isnull=True, end_date__isnull=True):
        # sinnvolle Defaults: beides auf heute
        b.start_date = today
        b.end_date = today
        b.save(update_fields=['start_date', 'end_date'])

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_add_booking_dates_nullable'),
    ]

    operations = [
        migrations.RunPython(backfill_dates, migrations.RunPython.noop),
    ]
