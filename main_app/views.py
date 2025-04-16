from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ClienteForm, LoginForm
from .models import Cliente, Administrador

from django.contrib import messages

def home(request):
    return render(request, 'main_app/home.html')

def weather_key(request):
    return JsonResponse({'api_key': '02vnq5e841rw5wjcj3z85f200ij16if7f8mn6fxe'})

def register(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # o redirige donde quieras
    else:
        form = ClienteForm()
    return render(request, 'main_app/register.html', {'form': form})

def membresia_competidor(request):
    return render(request, 'main_app/membresiaCompetidor.html')

def membresia_pro_athlete(request):
    return render(request, 'main_app/membresiaProAthlete.html')

def calendario_actividades(request):
    return render(request, 'main_app/calendarioActividades.html')

def galeria_multimedia(request):
    return render(request, 'main_app/galeriaMultimedia.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            
            # Si el correo termina en @admin.com, es un Administrador
            if correo.endswith('@adminweb.com'):
                try:
                    admin = Administrador.objects.get(correo_administrador=correo)
                    if admin.contraseña_administrador == contraseña:  # ⚠ En producción usa hash
                        request.session['admin_id'] = admin.id
                        request.session['admin_nombre'] = admin.primer_nombre
                        messages.success(request, f'¡Bienvenido administrador, {admin.primer_nombre}!')
                        return redirect('panel_admin')  # Redirige al panel de administración
                    else:
                        messages.error(request, 'Contraseña de administrador incorrecta.')
                except Administrador.DoesNotExist:
                    messages.error(request, 'No existe una cuenta de administrador con ese correo.')
            else:
                # Caso Cliente normal
                try:
                    cliente = Cliente.objects.get(correo=correo)
                    if cliente.contraseña == contraseña:  # ⚠ En producción usa hash
                        request.session['cliente_id'] = cliente.id
                        request.session['cliente_nombre'] = cliente.nombre
                        messages.success(request, f'¡Bienvenido, {cliente.nombre}!')
                        return redirect('calendario_actividades')  # Redirige al área de clientes
                    else:
                        messages.error(request, 'Contraseña incorrecta.')
                except Cliente.DoesNotExist:
                    messages.error(request, 'No existe una cuenta con ese correo.')
    else:
        form = LoginForm()

    return render(request, 'main_app/login.html', {'form': form})


def panel_admin(request):
    clientes = Cliente.objects.all()
    form = ClienteForm()

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')

    return render(request, 'main_app/admin_panel.html', {'form': form, 'clientes': clientes})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = ClienteForm(instance=cliente)
    clientes = Cliente.objects.all()
    return render(request, 'main_app/admin_panel.html', {'form': form, 'clientes': clientes})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    cliente.delete()
    return redirect('panel_admin')