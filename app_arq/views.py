from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
import os
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proyecto, Trabajador, Material, Mensaje
from .forms import MensajeForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def inicio(req):

    return render(req, "inicio.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/app_arq')  
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtelo de nuevo.')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def es_superusuario(user):
    return user.is_superuser

@user_passes_test(es_superusuario, login_url='/Inicio/')
def crear_superusuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True 
            user.is_superuser = True
            user.save()
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'resgister_super.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/app_arq/login')

def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            return redirect('bandeja_entrada')
    else:
        form = MensajeForm()
    return render(request, 'enviar_mensaje.html', {'form': form})


def bandeja_entrada(request):
    mensajes_recibidos = Mensaje.objects.filter(destinatario=request.user)
    return render(request, 'bandeja_entrada.html', {'mensajes': mensajes_recibidos})

def eliminar_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id)
    mensaje.eliminado = True
    mensaje.save()
    return redirect('bandeja_entrada')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Inicio')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def filtrar_proyectos(request):
    query = request.GET.get('q')
    proyectos = Proyecto.objects.filter(
        Q(titulo__icontains=query) 
    ) if query else Proyecto.objects.all()

    return render(request, 'proyect_list.html', {'proyectos': proyectos})

def filtrar_materiales(request):
    query = request.GET.get('q')
    materiales = Material.objects.filter(
        Q(nombre__icontains=query) | Q(barrio__icontains=query)
    ) if query else Material.objects.all()

    return render(request, 'material_list.html', {'materiales': materiales})

def filtrar_trabajadores(request):
    query = request.GET.get('q')
    puesto = request.GET.get('puesto')  
    disponibilidad = request.GET.get('disponibilidad')
    horario = request.GET.get('horario')
    trabajadores = Trabajador.objects.all()

    if query:
        trabajadores = trabajadores.filter(Q(nombre__icontains=query) | Q(apellido__icontains=query))

    if puesto:  
        trabajadores = trabajadores.filter(puesto=puesto)
    
    if disponibilidad:  
        trabajadores = trabajadores.filter(disponibilidad=disponibilidad)

    if horario:  
        trabajadores = trabajadores.filter(horario=horario)

    return render(request, 'trabajador_list.html', {'trabajadores': trabajadores})
    


class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    fields = ['titulo', 'descripcion', 'link', 'pdf', 'email', 'inversion'] 
    template_name = 'proyect_create.html'
    success_url = '/app_arq/lista_proyecto/'
    login_url = '/app_arq/login/'
    context_object_name = "proyecto"
    
    def form_valid(self, form):
        proyecto = form.save(commit=False)
        proyecto.user = self.request.user
        proyecto.save()
        return super().form_valid(form)

class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    template_name = 'proyect_update.html'
    fields = ['titulo', 'descripcion', 'link', 'pdf', 'email', 'inversion'] 
    success_url = '/app_arq/lista_proyecto/'
    login_url = '/app_arq/login/'
    context_object_name = "proyecto"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'proyect_delete.html'
    success_url = '/app_arq/lista_proyecto/'
    login_url = '/app_arq/login/'

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "proyect_list.html"
    context_object_name = "proyectos"
    login_url = '/app_arq/login/'


class TrabajadorCreateView(LoginRequiredMixin, CreateView):
    model = Trabajador
    fields = ['nombre', 'apellido', 'numero', 'email', 'cv', 'puesto', 'horario', 'disponibilidad']
    template_name = "trabajador_create.html"
    success_url = '/app_arq/lista_trabajador/'
    login_url = '/app_arq/login/'

    def form_valid(self, form):
        trabajador = form.save(commit=False)
        trabajador.user = self.request.user
        trabajador.save()
        return super().form_valid(form)


class TrabajadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Trabajador
    template_name = 'trabajador_delete.html'
    success_url = '/app_arq/lista_trabajador'
    login_url = '/app_arq/login/'


    def delete(self, request, *args, **kwargs):
        trabajador = self.get_object()

        if trabajador.cv:
            ruta_archivo = trabajador.cv.path

            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
        return super().delete(request, *args, **kwargs)

class TrabajadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Trabajador
    template_name = 'trabajador_update.html'
    fields = ['nombre', 'apellido', 'numero', 'email', 'cv', 'puesto', 'horario', 'disponibilidad']
    success_url = '/app_arq/lista_trabajador'
    login_url = '/app_arq/login/'

class TrabajadorListView(LoginRequiredMixin, ListView):
    model = Trabajador
    template_name = 'trabajador_list.html'
    context_object_name = 'trabajadores'
    success_url = '/app_arq/lista_trabajador'
    login_url = '/app_arq/login/'

class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    fields = ['nombre', 'numero', 'email', 'barrio'] 
    template_name = 'material_create.html'
    success_url = '/app_arq/lista_material/'
    login_url = '/app_arq/login/'
    context_object_name = "material"
    
    def form_valid(self, form):
        material = form.save(commit=False)
        material.user = self.request.user
        material.save()
        return super().form_valid(form)


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = 'material_delete.html'
    success_url = '/app_arq/lista_material'
    login_url = '/app_arq/login/'
    context_object_name = "material"


class TrabajadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Trabajador
    template_name = 'trabajador_delete.html'
    success_url = '/app_arq/lista_trabajador'
    login_url = '/app_arq/login/'


class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    template_name = 'material_update.html'
    fields =  ['nombre', 'numero', 'email', 'barrio'] 
    success_url = '/app_arq/lista_material'
    login_url = '/app_arq/login/'

class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    template_name = 'material_list.html'
    context_object_name = 'materiales'
    success_url = '/app_arq/lista_material'
    login_url = '/app_arq/login/'

