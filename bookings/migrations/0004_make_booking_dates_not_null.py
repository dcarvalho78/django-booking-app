from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_backfill_booking_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='start_date',
            field=models.DateField(null=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(null=False),
        ),
    ]
