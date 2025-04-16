from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'main_app/home.html')

def weather_key(request):
    return JsonResponse({'api_key': '02vnq5e841rw5wjcj3z85f200ij16if7f8mn6fxe'})

def register(request):
    return render(request, 'main_app/register.html')

def membresia_competidor(request):
    return render(request, 'main_app/membresiaCompetidor.html')

def membresia_pro_athlete(request):
    return render(request, 'main_app/membresiaProAthlete.html')

def calendario_actividades(request):
    return render(request, 'main_app/calendarioActividades.html')

def galeria_multimedia(request):
    return render(request, 'main_app/galeriaMultimedia.html')
