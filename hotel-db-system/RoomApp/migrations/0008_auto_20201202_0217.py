# Generated by Django 3.1.3 on 2020-12-01 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomApp', '0007_auto_20201130_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out',
            field=models.DateTimeField(),
        ),
    ]
