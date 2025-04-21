from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ClienteForm, LoginForm, EntrenadorForm, ClaseForm, MembresiaForm
from .models import Cliente, Administrador, Clase, Entrenador, Membresia

from django.contrib import messages


def home(request):
    membresia_competidor = Membresia.objects.get(nombre='Competidor')
    membresia_athlete = Membresia.objects.get(nombre='Pro Athlete')
    return render(request, 'main_app/home.html', {
        'membresia_competidor': membresia_competidor,
        'membresia_athlete': membresia_athlete
    })

def menu_admin(request):
    return render(request, 'main_app/menu_admin.html')

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
    clases = Clase.objects.all()
    dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado']

    # Creamos una estructura para el calendario
    calendario = {
        '08:00 - 09:00': {dia: '' for dia in dias_semana},
        '10:00 - 11:00': {dia: '' for dia in dias_semana},
        '18:00 - 19:00': {dia: '' for dia in dias_semana},
        '20:00 - 21:00': {dia: '' for dia in dias_semana},
    }

    for clase in clases:
        hora = clase.horario.strftime('%H:%M')
        dia = clase.horario.strftime('%A').lower()

        # Convertimos a español si es necesario
        dias_traducidos = {
            'monday': 'lunes',
            'tuesday': 'martes',
            'wednesday': 'miércoles',
            'thursday': 'jueves',
            'friday': 'viernes',
            'saturday': 'sábado',
        }

        dia = dias_traducidos.get(dia, dia)

        # Determinar el bloque de hora
        bloque = None
        if hora >= '08:00' and hora < '09:00':
            bloque = '08:00 - 09:00'
        elif hora >= '10:00' and hora < '11:00':
            bloque = '10:00 - 11:00'
        elif hora >= '18:00' and hora < '19:00':
            bloque = '18:00 - 19:00'
        elif hora >= '20:00' and hora < '21:00':
            bloque = '20:00 - 21:00'

        if bloque and dia in calendario[bloque]:
            calendario[bloque][dia] = {
                'nombre': clase.nombre,
                'entrenador': {
                    'primer_nombre': clase.entrenador.primer_nombre,
                    'apellido_paterno': clase.entrenador.apellido_paterno,
                        },
                'membresia': clase.membresia,
                'cupos_maximos': clase.cupos_maximos,
                'cupos_disponibles': clase.cupos_disponibles,
        }

    return render(request, 'main_app/calendarioActividades.html', {
        'calendario': calendario
    })


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
                        return redirect('menu_admin')  # Redirige al panel de administración
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

##CRUD CLIENTE##
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

##CRUD PROFESOR##
def lista_entrenadores(request):
    entrenadores = Entrenador.objects.all().order_by('primer_nombre')
    
    if request.method == 'POST':
        if 'id' in request.POST:
            entrenador = get_object_or_404(Entrenador, pk=request.POST['id'])
            form = EntrenadorForm(request.POST, request.FILES, instance=entrenador)
        else:
            form = EntrenadorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('lista_entrenadores')
    else:
        form = EntrenadorForm()

    context = {
        'form': form,
        'entrenadores': entrenadores
    }
    return render(request, 'main_app/admin_panel_entrenadores.html', context)


def editar_entrenador(request, entrenador_id):
    entrenador = get_object_or_404(Entrenador, pk=entrenador_id)

    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES, instance=entrenador)
        if form.is_valid():
            form.save()
            return redirect('lista_entrenadores')
    else:
        form = EntrenadorForm(instance=entrenador)

    entrenadores = Entrenador.objects.all().order_by('primer_nombre')
    context = {
        'form': form,
        'entrenadores': entrenadores
    }
    return render(request, 'main_app/admin_panel_entrenadores.html', context)


def eliminar_entrenador(request, entrenador_id):
    entrenador = get_object_or_404(Entrenador, pk=entrenador_id)
    entrenador.delete()
    return redirect('lista_entrenadores')

##CRUD CLASES##
def clases_view(request):
    clases = Clase.objects.all()
    form = ClaseForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('clases')

    return render(request, 'main_app/admin_panel_clases.html', {
        'form': form,
        'clases': clases
    })

def editar_clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    form = ClaseForm(request.POST or None, instance=clase)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('clases')

    clases = Clase.objects.all()
    return render(request, 'main_app/admin_panel_clases.html', {
        'form': form,
        'clases': clases
    })

def eliminar_clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    clase.delete()
    return redirect('clases')
##
# Vista para agregar o editar una membresía
def agregar_editar_membresia(request, membresia_id=None):
    if membresia_id:
        membresia = get_object_or_404(Membresia, id=membresia_id)
    else:
        membresia = None
    
    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_membresias')
    else:
        form = MembresiaForm(instance=membresia)
    
    return render(request, 'main_app/admin_panel_membresias.html', {'form': form})

# Vista para listar todas las membresías
def lista_membresias(request):
    membresias = Membresia.objects.all()
    return render(request, 'main_app/admin_panel_membresias.html', {'membresias': membresias})

# Vista para eliminar una membresía
def eliminar_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    if request.method == 'POST':
        membresia.delete()
        return redirect('admin_panel_membresias')
    return render(request, 'main_app/eliminar_membresia_confirmar.html', {'membresia': membresia})

def editar_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            form.save()
            return redirect('admin_panel_membresias')
    else:
        form = MembresiaForm(instance=membresia)
    return render(request, 'main_app/editar_membresia.html', {'form': form, 'membresia': membresia})

def admin_panel_membresias(request):
    membresias = Membresia.objects.all()

    if request.method == 'POST' and 'descripcion' in request.POST:
        membresia_id = request.POST.get('membresia_id')
        nueva_descripcion = request.POST.get('descripcion')

        membresia = get_object_or_404(Membresia, id=membresia_id)

        membresia.descripcion = nueva_descripcion
        membresia.save()
        return redirect('admin_panel_membresias')  # Asegúrate de que este nombre coincide con tu url

    return render(request, 'main_app/admin_panel_membresias.html', {
        'membresias': membresias
    })
    
def membresia_competidor(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    return render(request, 'main_app/membresiaCompetidor.html', {'membresia': membresia})

def membresia_pro_athlete(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    return render(request, 'main_app/membresiaProAthlete.html', {'membresia': membresia})