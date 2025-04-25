from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

from .views import home, weather_key, register, login_view, panel_admin, editar_cliente, eliminar_cliente

urlpatterns = [
    path('api/weather-key/', weather_key, name='weather_key'),
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),
    path('membresia-competidor/<int:membresia_id>/', views.membresia_competidor, name='membresia_competidor'),
    path('membresia-pro-athlete/<int:membresia_id>/', views.membresia_pro_athlete, name='membresia_pro_athlete'),    
    path('calendario-actividades/', views.calendario_actividades, name='calendario_actividades'),
    path('galeria-multimedia/', views.galeria_multimedia, name='galeria_multimedia'),
    path('admin-panel-usuario/', views.panel_admin, name='panel_admin'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('menu-admin/', views.menu_admin, name='menu_admin'),
    path('entrenadores/', views.lista_entrenadores, name='lista_entrenadores'),
    path('entrenadores/editar/<int:entrenador_id>/', views.editar_entrenador, name='editar_entrenador'),
    path('entrenadores/eliminar/<int:entrenador_id>/', views.eliminar_entrenador, name='eliminar_entrenador'),
    path('clases/', views.clases_view, name='clases'),
    path('clases/editar/<int:id>/', views.editar_clase, name='editar_clase'),
    path('clases/eliminar/<int:id>/', views.eliminar_clase, name='eliminar_clase'),
    # Elimina la ruta 'admin/membresias/' que está causando conflicto
    path('panel_membresias/', views.admin_panel_membresias, name='panel_membresias'),
    path('admin-panel/membresias/', views.lista_membresias, name='admin_panel_membresias'),
    path('admin-panel/membresias/editar/<int:membresia_id>/', views.agregar_editar_membresia, name='editar_membresia'),
    path('admin-panel/membresias/agregar/', views.agregar_editar_membresia, name='agregar_membresia'),
    path('admin-panel/membresias/eliminar/<int:membresia_id>/', views.eliminar_membresia, name='eliminar_membresia'),
    path('agendar/', views.agendar_clase, name='agendar_clase'),
    path('cotizaciones/', views.lista_entrenadores, name='lista_entrenadores'),
]
