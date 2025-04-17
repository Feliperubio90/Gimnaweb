from django.contrib import admin
from .models import Cliente , Administrador, Entrenador, Clase



# Register your models here.
admin.site.register(Cliente)
admin .site.register(Administrador)
admin.site.register(Entrenador)
admin.site.register(Clase)