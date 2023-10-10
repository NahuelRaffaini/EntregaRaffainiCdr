from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', inicio, name="Inicio"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('crear_superusuario/', crear_superusuario, name='crear_superusuario'),
    path('logout/', logout_view, name='logout'),
    path('enviar_mensaje/', enviar_mensaje, name='enviar_mensaje'),
    path('bandeja_entrada/', bandeja_entrada, name='bandeja_entrada'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('eliminar/<int:mensaje_id>/', eliminar_mensaje, name='eliminar_mensaje'),
    path('crear_proyecto/', ProyectoCreateView.as_view(), name='crear_proyecto'),
    path('actualizar_proyecto/<pk>', ProyectoUpdateView.as_view(), name='actualizar_proyecto'),
    path('eliminar_proyecto/<pk>', ProyectoDeleteView.as_view(), name='eliminar_proyecto'),
    path('lista_proyecto/', ProyectoListView.as_view(), name='lista_proyecto'),
    path('filtrar_proyectos/', filtrar_proyectos, name='filtrar_proyectos'),
    path('filtrar_trabajadores/', filtrar_trabajadores, name='filtrar_trabajadores'),
    path('crear_trabajador/', TrabajadorCreateView.as_view(), name='crear_trabajador'),
    path('actualizar_trabajador/<pk>', TrabajadorUpdateView.as_view(), name='actualizar_trabajador'),
    path('eliminar_trabajador/<pk>', TrabajadorDeleteView.as_view(), name='eliminar_trabajador'),
    path('lista_trabajador/', TrabajadorListView.as_view(), name='lista_trabajador'),
    path('crear_material/', MaterialCreateView.as_view(), name='crear_material'),
    path('actualizar_material/<pk>', MaterialUpdateView.as_view(), name='actualizar_material'),
    path('eliminar_material/<pk>', MaterialDeleteView.as_view(), name='eliminar_material'),
    path('lista_material/', MaterialListView.as_view(), name='lista_material'),
    path('filtrar_materiales/', filtrar_materiales, name='filtrar_materiales')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)