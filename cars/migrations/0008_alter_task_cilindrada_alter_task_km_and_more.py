# Generated by Django 4.2.6 on 2023-10-29 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_alter_task_ano'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='cilindrada',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='car',
            name='km',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='car',
            name='precioVenta',
            field=models.CharField(max_length=4),
        ),
    ]
