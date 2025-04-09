from django.urls import path
from . import views

from .views import home, weather_key, register

urlpatterns = [
    path('api/weather-key/', weather_key, name='weather_key'),
    path('', views.home, name='home'),
    path('register/', register, name='register'),
]