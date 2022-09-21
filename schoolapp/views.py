from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from schoolapp.models import Estudiante, Programa, LogAuditor
from schoolapp.forms import ProgramaForm, EstudianteForm, UserForm, LoginForm

def register(request):
    contexto = dict()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                email=email,
                last_name=last_name
            )
            mensaje = f"Usuario {user.username} es almacenado correctamente"
        else:
            messages.error(request, 'Verifique los datos ingresado. Intentar de nuevo')
        return render(request, 'mensaje.html', {'mensaje': mensaje}) 
    else:
        user = UserForm()
        contexto['userform'] = user
        return render(request, 'cuenta/registrar.html', contexto)

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Las credenciales proporcionadas no son correctas')
                return redirect(reverse('login'))        
        else:
            messages.error(request, 'Verifique los datos ingresado. Intentar de nuevo')
            return redirect(reverse('login'))
    else:
        form = LoginForm()
        return render(request, 'cuenta/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect(reverse('login'))
    
def home(request):
    return render(request,'index.html')

@login_required(login_url='/login/')
def listar_estudiante(request):
    estudiantes = Estudiante.objects.all()
    contexto = {
        'estudiantes': estudiantes
    }
    return render(request, 'estudiante/listar.html', contexto)

@login_required(login_url='/login/')
def crear_estudiante(request):
    contexto = dict()
    contexto['accion'] = 'Crear'
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El estudiante fue almacenado correctamente')
            return redirect(reverse('listar-estudiantes'))
        else:
            messages.error(request, 'Los datos enviados desde el formulario no son validos')
            return redirect(reverse('crear-estudiantes'))
    else:
        form = EstudianteForm()
        contexto['boton'] = 'Guardar'
        contexto['form'] = form
        return render(request, 'estudiante/form.html', contexto) 

@login_required(login_url='/login/')  
def actualizar_estudiante(request, id):
    estudiante = Estudiante.objects.get(id=id)
    contexto = dict()
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, 'El estudiante fue actualizado correctamente')
            return redirect(reverse('listar-estudiantes'))
        else:
            messages.error(request, 'Los datos enviados desde el formulario no son validos')
            return redirect(f'/actualizar/estudiante/{id}')
    else:
        form = EstudianteForm(instance=estudiante)
        contexto['form']=form
        contexto['boton'] = 'Actualizar'
        return render(request, 'estudiante/form.html', contexto)

@login_required(login_url='/login/')  
def eliminar_estudiante(request, id):
    try:
        estudiante = Estudiante.objects.get(id=id)
        estudiante.delete()
        messages.success(request, 'El estudiante fue eliminado correctamente')
    except ObjectDoesNotExist:
        messages.error(request, "No se encontró el estudiante solicitado")    
    return redirect(reverse('listar-estudiantes'))

@login_required(login_url='/login/')
def crear_programa(request):
    if request.method == 'POST':
        form = ProgramaForm(request.POST)
        contexto = dict()
        if form.is_valid():
            try:
                form.save()
                LogAuditor.objects.create(mensajeError="Se guardo el programa correctamente")
            except ValueError as e:
                LogAuditor.objects.create(mensajeError=e)
            contexto['mensaje'] = "El programa se almacenó correctamente"
        else:
            contexto['mensaje'] = "Error al almacenar el programa"
        return render(request, 'programa/mensaje.html', contexto)
    else:
        programaForm = ProgramaForm()
        contexto = {
            'programaForm': programaForm,
            'boton': 'Guardar',
            'accion': 'Crear'
            }
        return render(request, 'programa/form_programa.html', contexto)

@login_required(login_url='/login/')
def actualizar_program(request, id):
    try:
        programa = Programa.objects.get(id=id)
    except ObjectDoesNotExist:
        mensaje = "El programa que pretender editar no existe"
        LogAuditor.objects.create(mensajeError=mensaje)
        return HttpResponse(mensaje)
        
    contexto = dict()
    if request.method == 'POST':
        form = ProgramaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            contexto['mensaje'] = "El programa fue editado correctamente"
        else:
            contexto['mensaje'] = "Error al almacenar el programa"
        return render(request, 'programa/mensaje.html', contexto)
    else:
        programForm = ProgramaForm(instance=programa)
        contexto['programaForm'] = programForm
        contexto['boton'] = 'Editar'
        contexto['accion'] = 'Editar'
        return render(request, 'programa/form_programa.html', contexto)