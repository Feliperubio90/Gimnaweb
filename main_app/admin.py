from django.contrib import admin
from .models import Cliente , Administrador, Entrenador, Clase, Membresia



# Register your models here.
admin.site.register(Cliente)
admin .site.register(Administrador)
admin.site.register(Entrenador)
admin.site.register(Clase)

@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)