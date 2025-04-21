from django.db import models


class Cliente(models.Model):
    MEMBERSHIP_CHOICES = [
        ('Competitor', 'Competitor'),
        ('Pro Athlete', 'Pro Athlete'),
    ]

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    membresia = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)

    def __str__(self):
        return self.nombre

class Administrador(models.Model):
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    correo_administrador = models.EmailField(unique=True)
    contraseña_administrador = models.CharField(max_length=128)  

    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno}"

from django.db import models

from django.db import models

class Entrenador(models.Model):
    MEMBRESIA_CHOICES = [
        ('Competitor', 'Competitor'),
        ('Pro Athlete', 'Pro Athlete'),
    ]

    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=100)
    membresia = models.CharField(max_length=20, choices=MEMBRESIA_CHOICES)
    cotizacion = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_disponible = models.DateField()
    imagen = models.ImageField(upload_to='entrenadores/', null=True, blank=True)
    hora_disponible_desde = models.TimeField(default='08:00')
    hora_disponible_hasta = models.TimeField(default='21:00')

    def __str__(self):
        return f'{self.primer_nombre} {self.apellido_paterno} - {self.especialidad}'

    
class Clase(models.Model):
    MEMBRESIA_CHOICES = [
        ('Competitor', 'Competitor'),
        ('Pro Athlete', 'Pro Athlete'),
    ]

    nombre = models.CharField(max_length=100)
    horario = models.DateTimeField()
    cupos_maximos = models.PositiveIntegerField()
    cupos_disponibles = models.PositiveIntegerField()
    membresia = models.CharField(max_length=20, choices=MEMBRESIA_CHOICES)
    entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE, related_name='clases')

    def __str__(self):
        return f'{self.nombre} - {self.horario.strftime("%d/%m/%Y %H:%M")}'    
###
class Membresia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre