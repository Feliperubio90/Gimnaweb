from django.urls import path
from . import views

from .views import home, weather_key, register

urlpatterns = [
    path('api/weather-key/', weather_key, name='weather_key'),
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('membresia-competidor/', views.membresia_competidor, name='membresia_competidor'),
    path('membresia-pro-athlete/', views.membresia_pro_athlete, name='membresia_pro_athlete'),
    path('calendario-actividades/', views.calendario_actividades, name='calendario_actividades'),
    path('galeria-multimedia/', views.galeria_multimedia, name='galeria_multimedia'),
]