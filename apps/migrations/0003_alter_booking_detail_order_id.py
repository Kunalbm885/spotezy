# Generated by Django 4.0.2 on 2022-10-16 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_booking_detail_booked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_detail',
            name='Order_id',
            field=models.CharField(max_length=80),
        ),
    ]