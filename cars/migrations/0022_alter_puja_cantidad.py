# Generated by Django 4.2.6 on 2023-11-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0021_puja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puja',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]