from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
