# Generated by Django 4.2.6 on 2023-11-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0019_car_validado'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='publicado',
            field=models.BooleanField(default=False),
        ),
    ]
