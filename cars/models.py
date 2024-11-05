from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator  # Importa MaxValueValidator

# Create your models here.
# Que se vean los payments de los coches
class Car(models.Model):
    matricula = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    ano = models.PositiveSmallIntegerField()
    cilindrada = models.DecimalField(max_digits=3, decimal_places=1)
    km = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2)
    FechaSubasta = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    validado = models.BooleanField(default=False) #Se entiende por validado que se ha pagado
    publicado = models.BooleanField(default=False)


    def __str__(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Año: {self.ano}, Matrícula: {self.matricula}, Cilindrada: {self.cilindrada}, Kilómetros: {self.km}, Precio de venta: {self.precioVenta}, Fecha de subasta: {self.FechaSubasta},  ID: {self.id}, Validado: {self.validado}"

class Imagen(models.Model):
    coche = models.ForeignKey(Car, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='theme/static/img/')

    def __str__(self):
        return f"Imagen de {self.coche.title} ({self.coche.marca} {self.coche.modelo}) - {self.coche.imagenes.count()} imágenes"

    
class Pago(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)  # Campo booleano para el estado de pago
    transaccion = models.CharField(max_length=20, null=True)  # Campo para el ID de transacción
    car = models.OneToOneField(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='pago')  # Agrega esta línea

    def __str__(self):
        estado_pago = "Pagado" if self.pagado else "No Pagado"
        info_coche = f"{self.car.marca} {self.car.modelo} {self.car.matricula}" if self.car else "No hay coche asociado"
        return f"Estado de Pago: {estado_pago}, Usuario: {self.user_id.username}, Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}, ID de transacción: {self.transaccion}, Monto: {self.monto},  Coche: {info_coche}"

class Puja(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usuario: {self.user.id} Coche: {self.car.id} Puja: {self.cantidad}, Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
