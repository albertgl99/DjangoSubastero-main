from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Car, Pago, Puja  # Don't forget to import Puja

class CarAdmin(admin.ModelAdmin):
    readonly_fields = ('matricula',)

class PagoAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha',)  # assuming you want to make 'fecha' read-only

class PujaAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha',)  # assuming you want to make 'fecha' read-only

try:
    admin.site.register(Car, CarAdmin)
except AlreadyRegistered:
    pass

try:
    admin.site.register(Pago, PagoAdmin)
except AlreadyRegistered:
    pass

try:
    admin.site.register(Puja, PujaAdmin)  # Register Puja with PujaAdmin
except AlreadyRegistered:
    pass
