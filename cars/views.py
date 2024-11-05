from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# try and except IntegrityError:
from cars.decorators import allowed_users, unauthenticated_user, admin_only
from .forms import PaymentForm, CarForm
from .models import Imagen, Car, Pago, Puja
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import sys

import stripe








# Create your views here.
# @admin_only
def home(request):
    cars = Car.objects.filter(publicado=True)
    car_images = {}  # A dictionary to store images for each car
    car_pujas = {}  # A dictionary to store the last bid for each car


    for car in cars:
        images = Imagen.objects.filter(coche=car)
        car_images[car] = images
        # Get the last bid for this car
        last_bid = Puja.objects.filter(car=car).order_by('-fecha').first()
        if last_bid:
            car_pujas[car] = last_bid.cantidad
        else:
            car_pujas[car] = 'No hay pujas aún'
    return render(request, 'home.html', {'cars': cars, 'car_images': car_images, 'car_pujas': car_pujas})


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            if User.objects.filter(username=username).exists():
                return HttpResponse("Usuario ya existe")
            else:
                try:
                    user = User.objects.create_user(
                        username=username, 
                        password=request.POST['password1'],
                        email=request.POST['email'] 
                        )
                    group, created = Group.objects.get_or_create(name='customer')
                    user.groups.add(group)
                    user.save()
                except Exception as e:
                    # Handle specific exceptions here
                    print(str(e))
                """send_mail(
                    'Contact Form',
                    'Hola',
                    'settings.EMAIL_HOST_USER',
                    'rengo1234@gmail.com',
                    fail_silently=False
                )"""
                mailTemplate = render_to_string(
                    'email.html', {'username': user.username})

                msg = EmailMultiAlternatives(
                    "Subject", "Texto", "rengo1234@gmail.com", ["rengo1234@gmail.com"])
                msg.attach_alternative(mailTemplate, "text/html")
                msg.send()
                """email = EmailMessage(
                    "Subject",
                    mailTemplate,
                    settings.EMAIL_HOST_USER,
                    ["rengo1234@gmail.com"]
                    )
                email.fail_silently = False

                email.send()"""
                messages.success(request, ' Correo enviado ')

                print("Email enviado")
                login(request, user)
                return redirect('car')

        return HttpResponse("Password no coinciden")
    
def processImage(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear un objeto Car con los datos del formulario, incluyendo la imagen
            car = form.save(commit=False)
            car.user = request.user  # Asigna el usuario actual
            car.save()
            return redirect('car')
    # Si la solicitud no es POST o el formulario no es válido, puedes agregar un manejo de errores aquí
    # Por ejemplo, mostrar un mensaje de error o redirigir a una página de error

#Mis coches - Para usuarios que ya han enviado y pagado el coche a subastar
@login_required
def car(request):
    cars = Car.objects.filter(user=request.user,validado=True)
    car_images = {}  # A dictionary to store images for each car

    for car in cars:
        images = Imagen.objects.filter(coche=car)
        car_images[car] = images

    return render(request, 'car.html', {'cars': cars, 'car_images': car_images})

#Admin - Coches para revisar y publicar
@login_required
def cochesEnviados(request):
    cars = Car.objects.filter(validado=True)
    car_images = {}  # A dictionary to store images for each car

    for car in cars:
        images = Imagen.objects.filter(coche=car)
        car_images[car] = images

    return render(request, 'cochesEnviados.html', {'cars': cars, 'car_images': car_images})

#ADMIN - Aprueba los coches para que pasen a la subasta
def aprobarCoche(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        car.publicado = True
        car.save()
        PujaInicial = Puja()
        PujaInicial.cantidad = 100
        PujaInicial.fecha = timezone.now()
        PujaInicial.car = car
        PujaInicial.user = request.user  # Asigna el usuario a la puja
        PujaInicial.save()
        return HttpResponse('El coche ' + str(car.matricula) + ' se ha publicado')
    except Car.DoesNotExist:
        return HttpResponse('No se encontró ningún coche con id=' + str(car_id))






def cochesAprobados(request):
    cars = Car.objects.filter()
    car_images = {}  # A dictionary to store images for each car

    for car in cars:
        images = Imagen.objects.filter(coche=car)
        car_images[car] = images

    return render(request, 'cochesEnviados.html', {'cars': cars, 'car_images': car_images})

@login_required
def complete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user=request.user)
    if request.method == 'POST':
        car.datecompleted = timezone.now()
        car.save()
        return redirect('car')


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('car')


@login_required
# @allowed_users(allowed_roles=['admin'])
def car_detail(request, car_id):
    if request.method == 'GET':
        car = get_object_or_404(Car, pk=car_id)
        form = CarForm(instance=car)

        # Retrieve associated images for the car
        # Adjust this query based on your model structure
        images = Imagen.objects.filter(coche=car)

        return render(request, 'car_detail.html', {'car': car, 'form': form, 'images': images})
    else:
        try:
            car = get_object_or_404(Car, pk=car_id, user=request.user)
            form = CarForm(request.POST, instance=car)
            form.save()
            return redirect('car')
        except ValueError:
            return render(request, 'car_detail.html', {'car': car, 'form': form, 'error': "Error updating car"})





# Configura la clave secreta de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY




# @unauthenticated_user


def create_car(request):
    if request.method == 'GET':
        return render(request, 'create_car.html', {
            'form': CarForm()
        })
    elif request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            new_car = form.save(commit=False)
            new_car.user = request.user
            new_car.save()

            # Crea una instancia de Pago (ajusta esto según tus datos reales)
            pago_instance = Pago(
                user_id=request.user,
                fecha=timezone.now(),
                monto=100,
            ) 
            # Asigna la instancia de Pago al coche
            new_car.pago_id = pago_instance
            pago_instance.save()

            for file in request.FILES.getlist('carImage'):
                imagen = Imagen(coche=new_car, imagen=file)
                imagen.save()

            return redirect('/cars/payment/'+str(new_car.id))
        else:
            return HttpResponse("Form is not valid")
    else:
        return render(request, 'create_car.html', {'form': CarForm})
        """except:
            return render(request, 'create_car.html',{
                'form':CarForm,
                'error':'Except:Please provide valid data'
            })"""

def payment(request, car_id):
    if request.method == 'GET':
        return render(
            request,
            'car_payment.html',
            {
                'car_id': car_id,

            })
    else:
        token = request.POST.get('stripeToken')
        form = PaymentForm(request.POST)
        monto = 200*100
        if form.is_valid():
            try:
                # Realiza el cargo en Stripe
                charge = stripe.Charge.create(
                    amount=monto,  # Monto en céntimos (100€)
                    currency='eur',
                    source=token,
                    description='Pago de 100€',
                )
                # return JsonResponse({'success': True})
            except stripe.error.CardError as e:
                print("Pago INValido",e)
                return JsonResponse({'error': str(e)})
            except stripe.error.StripeError as e:
                print("Pago INValido",e)
                return JsonResponse({'error': str(e)})
            try:
                car_instance = Car.objects.get(id=car_id)  # get the Car instance
            except Car.DoesNotExist:
                # handle the error, e.g. return an error message
                return HttpResponse('Car does not exist', status=400)
            #Pago valido
            payment = Pago()  # assuming Payment is your model name
            payment.user_id = request.user
            car_instance = Car.objects.get(id=car_id)  # get the Car instance
            car_instance.validado = True
            car_instance.save()
            payment.car = car_instance
            payment.fecha = timezone.now()
            payment.monto = monto
            payment.pagado = True
            payment.transaccion = token
            payment.save()
            print("Pago Valido")

            puja = Puja(user=request.user,car=car_instance,cantidad=100,fecha=timezone.now())
            puja.save()

            # Aquí puedes realizar acciones adicionales, como registrar el pago en tu base de datos
            return render(request, 'thanks.html')

        return render(request, 'thanks.html', {'form': form})


#Usuarios registrados que pujan
from django.db.models import Max

def pujar(request, car_id):
    # Asegurarse de que el usuario está autenticado
    if request.user.is_authenticated:
        user = request.user
        cantidadNuevaPuja = int(request.POST.get('puja'))
        
        # Obtener el coche o devolver un error 404 si no existe
        car = get_object_or_404(Car, id=car_id)

        # Obtener la puja más alta para este coche
        lastPuja = Puja.objects.filter(car=car).order_by('-cantidad').first()

        # Comprobar si el usuario actual ya tiene la puja más alta
        if lastPuja and lastPuja.user == user:
            messages.error(request, "No puedes pujar si ya tienes la puja más alta")
            #return HttpResponse("No puedes pujar si ya tienes la puja más alta")
        
        # Comprobar si la nueva puja es mayor que la última puja
        elif lastPuja is None or cantidadNuevaPuja > lastPuja.cantidad:
            # Comprobar si la nueva puja es un múltiplo de 100
            if cantidadNuevaPuja % 100 == 0:
                # Comprobar si la puja supera la última puja en al menos 100
                if lastPuja is None or cantidadNuevaPuja - lastPuja.cantidad >= 100:
                    # Crear una nueva puja
                    nuevaPuja = Puja(cantidad=cantidadNuevaPuja, car=car, user=user)
                    nuevaPuja.save()
                    messages.success(request, "Se ha realizado una nueva puja para el coche {car.matricula}")
                    #return HttpResponse(f'Se ha realizado una nueva puja para el coche {car.matricula}')
                else:
                    messages.error(request, "La puja debe superar la última puja en al menos 100")
                    #return HttpResponse('La puja debe superar la última puja en al menos 100')
            else:
                messages.error(request, "La puja debe ser un múltiplo de 100")
                #return HttpResponse('La puja debe ser un múltiplo de 100')
        else:
            messages.error(request, "La puja debe ser mayor que la última puja")
            #return HttpResponse('La puja debe ser mayor que la última puja')
    else:
        messages.error(request, "Debes iniciar sesión para realizar una puja")
        #return HttpResponse('Debes iniciar sesión para realizar una puja')
    return redirect('home')


