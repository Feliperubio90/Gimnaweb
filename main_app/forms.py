from django import forms
from .models import Cliente, Entrenador, Clase, Membresia
import re

class ClienteForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar Contraseña")

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'contraseña', 'telefono', 'membresia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'membresia': forms.Select(attrs={'class': 'form-control'}),
        }

    # Validación para el campo correo
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo:
            raise forms.ValidationError("Este campo es obligatorio.")
        if '@' not in correo:
            raise forms.ValidationError("El correo debe contener '@'.")
        if not (correo.endswith('.com') or correo.endswith('.cl')):
            raise forms.ValidationError("El correo debe terminar en .com o .cl.")
        return correo

    # Validación para el campo telefono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            raise forms.ValidationError("Este campo es obligatorio.")
        telefono_sin_espacios = telefono.replace(" ", "")
        if not re.match(r'^\+569\d{8}$', telefono_sin_espacios):
            raise forms.ValidationError("El número debe tener el formato chileno: +56 9 XXXXXXXX (ej: +56 9 12345678).")
        return telefono

    # Validación para el campo membresia
    def clean_membresia(self):
        membresia = self.cleaned_data.get('membresia')
        if not membresia:
            raise forms.ValidationError("Debes seleccionar una membresía.")
        return membresia

    # Validación de contraseñas
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("contraseña")
        confirm_password = cleaned_data.get("confirm_password")

        if not password:
            self.add_error('contraseña', "Este campo es obligatorio.")
        if password:
            if len(password) < 8:
                self.add_error('contraseña', "La contraseña debe tener al menos 8 caracteres.")
            if not any(char.isupper() for char in password):
                self.add_error('contraseña', "La contraseña debe contener al menos una letra mayúscula.")
            if not any(char.isdigit() for char in password):
                self.add_error('contraseña', "La contraseña debe contener al menos un número.")

        if password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        # Validar que no haya campos vacíos
        for field in self.cleaned_data:
            if not self.cleaned_data[field]:
                self.add_error(field, "Este campo es obligatorio.")
                
        return cleaned_data

class LoginForm(forms.Form):
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = '__all__'
        widgets = {
            'fecha_disponible': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_disponible_desde': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_disponible_hasta': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'
        widgets = {
            'horario': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cupos_maximos': forms.NumberInput(attrs={'class': 'form-control'}),
            'cupos_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'membresia': forms.Select(attrs={'class': 'form-control'}),
            'entrenador': forms.Select(attrs={'class': 'form-control'}),
        }        
###
class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }