# Generated by Django 4.2.6 on 2023-11-02 12:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0011_remove_task_carimage_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='ano',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='cilindrada',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='car',
            name='km',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)]),
        ),
        migrations.AlterField(
            model_name='car',
            name='marca',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='car',
            name='modelo',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(upload_to='cars/coches/'),
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
