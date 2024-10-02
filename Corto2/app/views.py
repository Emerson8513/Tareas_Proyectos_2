from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import re


MAX_FAILED_ATTEMPTS = 3
LOCKOUT_TIME = timedelta(minutes=30)  # Bloquear por 30 minutos

def paginaprincipal(request):
    context = {}
    return render(request,'generales/paginaprincipal.html',context)

def student(request):
    student = Student.objects.all()
    context = {'student':student}
    context = {}
    return render(request,'generales/student.html',context)

def teaching(request):
    teacher = Teacher.objects.all()
    context = {'teacher':teacher}
    context = {}
    return render(request,'generales/teaching.html',context)

def portafolio(request):
    context = {}
    return render(request,'generales/portafolio.html',context)

from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        lastname = request.POST['lastname']
        dpi = request.POST['DPI']
        date = request.POST['date']
        telephone = request.POST['telephone']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pwd']
        password_check = request.POST['pwd-repeat']

        if password != password_check:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'generales/register.html',{
                'name':name,
                'lastname':lastname,
                'dpi':dpi,
                'date':date,
                'telephone':telephone,
                'username':username,
                'email':email,
            })
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{12,}$', password):
                    messages.error(request, 'La contraseña debe tener al menos 12 caracteres, incluyendo una letra mayúscula, un número y un carácter especial.')
                    return render(request, 'generales/register.html', {...})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso. Por favor elija otro.')
            return render(request, 'generales/register.html', {
                'name': name,
                'lastname': lastname,
                'dpi': dpi,
                'date': date,
                'telephone': telephone,
                'username': username,
                'email': email,
            })

            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        student = Student.objects.create(
            name=name,
            lastname=lastname,
            dpi=dpi,
            date=date,
            telefhone=telephone,
            username=user,
            email=email,
            # password=password,
            # password_check=password_check,
        )
        student.save()

        messages.success(request, 'Registro exitoso.')
        return redirect('paginaprincipal')  

    return render(request, 'generales/register.html')

    

def cursos(request):
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request,'generales/cursos.html',context)


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         # Autenticar al usuario
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)  
#             messages.success(request, 'Inicio de sesión exitoso.')
#             return redirect('paginaprincipal')  
#         else:
#             messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
#             return render(request, 'generales/login.html')

#     return render(request, 'generales/login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return render(request, 'generales/login.html')

        
        profile, created = UserProfile.objects.get_or_create(user=user)

        if profile.is_locked:
            
            profile.unlock()
            if profile.is_locked:
                messages.error(request, 'Tu cuenta está bloqueada. Intenta más tarde.')
                return render(request, 'generales/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            profile.failed_attempts = 0
            profile.save()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('paginaprincipal')
        else:
            profile.failed_attempts += 1
            if profile.failed_attempts >= MAX_FAILED_ATTEMPTS:
                profile.is_locked = True
                profile.lockout_time = timezone.now() + LOCKOUT_TIME
                messages.error(request, f'Tu cuenta ha sido bloqueada por {LOCKOUT_TIME.total_seconds() // 60} minutos.')
            else:
                messages.error(request, f'Contraseña incorrecta. Intentos fallidos: {profile.failed_attempts}')
                messages.error(request,f'Despues de 3 Intentos su cuenta sera bloqueada')
            profile.save()

    return render(request, 'generales/login.html')

def logout_view(request):
    logout(request)  
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')  