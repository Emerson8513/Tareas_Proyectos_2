from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import EnrollmentForm
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import re
from django.contrib.auth.decorators import login_required



MAX_FAILED_ATTEMPTS = 3
LOCKOUT_TIME = timedelta(minutes=30)  # Bloquear por 30 minutos

# views.py
from .models import Student, Teacher

def paginaprincipal(request):
    context = {}

    if request.user.is_authenticated:
        # Verificar si el usuario es un estudiante
        try:
            context['is_student'] = Student.objects.filter(username=request.user).exists()
        except Student.DoesNotExist:
            context['is_student'] = False

        # Verificar si el usuario es un docente
        try:
            context['is_teacher'] = Teacher.objects.filter(user=request.user).exists()
        except Teacher.DoesNotExist:
            context['is_teacher'] = False

        # Verificar si el usuario es un administrador
        context['is_admin'] = request.user.is_staff or request.user.is_superuser

    return render(request, 'generales/paginaprincipal.html', context)


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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return render(request, 'generales/login.html')

        # Obtener o crear el perfil del usuario
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Verificar si la cuenta está bloqueada
        if profile.is_locked:
            # Verificar si ha pasado el tiempo de bloqueo
            profile.unlock()
            if profile.is_locked:
                messages.error(request, 'Tu cuenta está bloqueada. Intenta más tarde.')
                return render(request, 'generales/login.html')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Restablecer los intentos fallidos al iniciar sesión correctamente
            profile.failed_attempts = 0
            profile.save()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('paginaprincipal')
        else:
            # Incrementar el conteo de intentos fallidos
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

def login_view_teacher(request):
    if request.method == 'POST':
        username = request.POST['username']  # El nombre de usuario proporcionado en el formulario
        password = request.POST['password']  # La contraseña proporcionada

        try:
            # Verificar si el usuario (docente) existe buscando por el nombre de usuario vinculado a User
            teacher = Teacher.objects.get(user__username=username)
        except Teacher.DoesNotExist:
            messages.error(request, 'El docente no existe.')
            return render(request, 'generales/loginteacher.html')

        # Autenticar al usuario usando el sistema de autenticación de Django
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, 'teacher'):  # Verificamos que sea un docente
                login(request, user)  # Iniciar sesión con Django
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('paginaprincipal')  # Redirigir a la página principal
            else:
                messages.error(request, 'No tienes permisos para iniciar sesión como docente.')
        else:
            messages.error(request, 'Contraseña incorrecta.')

    return render(request, 'generales/loginteacher.html')


def some_view(request):
    # Aquí se pasa la lógica que quieras
    context = {}
    
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user)
            context['is_student'] = True
        except Student.DoesNotExist:
            context['is_student'] = False

        try:
            teacher = Teacher.objects.get(email=request.user.email)
            context['is_teacher'] = True
        except Teacher.DoesNotExist:
            context['is_teacher'] = False

    return render(request, 'some_template.html', context)

@login_required
def enroll_in_course(request, course_id):
    student = get_object_or_404(Student, username=request.user)  # Buscamos el estudiante asociado al usuario actual
    course = get_object_or_404(Course, id=course_id)  # Obtenemos el curso seleccionado

    # Verificar si el estudiante ya está matriculado en el curso
    existing_enrollment = Enrollment.objects.filter(student=student, course=course).exists()
    
    if existing_enrollment:
        # Si ya está matriculado, mostrar un mensaje de error y redirigir
        messages.error(request, f'Ya estás matriculado en el curso "{course.name}".')
        return redirect('my_courses')

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.course = course
            enrollment.save()
            messages.success(request, f'Te has matriculado correctamente en "{course.name}".')
            return redirect('my_courses')  # Redirigimos a la página donde se muestran los cursos matriculados
    else:
        form = EnrollmentForm(initial={'course': course})
    
    return render(request, 'generales/enroll.html', {'form': form, 'course': course})


@login_required
def course_list(request):
    student = get_object_or_404(Student, username=request.user)  # Obtener el estudiante actual
    courses = Course.objects.all()  # Obtener todos los cursos
    # Obtener los IDs de los cursos en los que el estudiante está matriculado
    enrolled_courses = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    
    return render(request, 'generales/cursos.html', {
        'courses': courses,
        'enrolled_courses': list(enrolled_courses),  # Convertir a lista
    })


@login_required
def my_courses(request):
    # Obtener el estudiante asociado al usuario actual
    student = Student.objects.get(username=request.user)

    # Obtener los cursos a los que está matriculado
    enrolled_courses = Enrollment.objects.filter(student=student)

    return render(request, 'generales/my_courses.html', {
        'student': student,
        'enrolled_courses': enrolled_courses
    })