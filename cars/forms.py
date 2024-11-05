from django import forms
from .models import Car

class DateInput(forms.DateInput):
    input_type = 'text'  # Utiliza un campo de texto en lugar de un campo de fecha
    format = '%d/%m/%Y'  # Formato de fecha personalizado

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['matricula','marca', 'modelo', 'ano', 'cilindrada', 'km', 'precioVenta', 'FechaSubasta', ]
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'cilindrada': forms.NumberInput(attrs={'class': 'form-control'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
            'precioVenta': forms.NumberInput(attrs={'class': 'form-control'}),
            'FechaSubasta': forms.DateInput(attrs={'class': 'form-control'}),
            'carImage': forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
        }
class PaymentForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    direccion = forms.CharField(label='Dirección', max_length=200)
    ciudad = forms.CharField(label='Ciudad', max_length=100)

        