# Generated by Django 4.2.6 on 2023-11-02 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0013_rename_user_pago_user_id_remove_pago_car_car_pago_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='matricula',
            field=models.CharField(default='LTC7070', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pago',
            name='transaccion',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='FechaSubasta',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='pago_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.pago'),
        ),
    ]
