from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
import re
def paginaprincipal(request):
    context = {}
    return render(request,'generales/paginaprincipal.html',context)

def course(request):
    context = {}
    return render(request,'generales/course.html',context)

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
        return redirect('paginaprincipal')  # Redireccionar a la página principal después del registro

    return render(request, 'generales/register.html')

    

def cursos(request):
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request,'generales/cursos.html',context)
