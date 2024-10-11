import face_recognition
import cv2
import numpy as np
import base64
import os
import pdfkit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import EnrollmentForm
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import re
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied






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

# views.py
import face_recognition
from django.core.files.uploadedfile import SimpleUploadedFile

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
        face_image = request.FILES.get('face_image')  # Nueva línea para obtener la imagen

        if password != password_check:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'generales/register.html', {...})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso. Por favor elija otro.')
            return render(request, 'generales/register.html', {...})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Procesamiento del reconocimiento facial
        if face_image:
            # Convertir la imagen en un formato adecuado para face_recognition
            image = face_recognition.load_image_file(face_image)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                face_encoding = face_encodings[0]
            else:
                messages.error(request, 'No se detectó ningún rostro en la imagen proporcionada.')
                return render(request, 'generales/register.html', {...})

        # Guardar el perfil con el encoding facial
        user_profile = UserProfile.objects.create(
            user=user,
            face_encoding=face_encoding.tobytes() if face_encodings else None
        )
        user_profile.save()

        student = Student.objects.create(
            name=name,
            lastname=lastname,
            dpi=dpi,
            date=date,
            telefhone=telephone,
            username=user,
            email=email,
            image=face_image
        )
        student.save()

        messages.success(request, 'Registro exitoso.')
        return redirect('paginaprincipal')

    return render(request, 'generales/register.html')


# views.py
from django.shortcuts import render
from .models import Course

def cursos(request):
    categories = [
        {'name': 'taxi', 'image': 'img/car-big.png'},
        {'name': 'motoraton', 'image': 'img/motoraton.png'},
        {'name': 'tuctuc', 'image': 'img/tuc-tuc.png'},
        {'name': 'mudanza', 'image': 'img/mudanza.png'},
    ]
    context = {'categories': categories}
    return render(request, 'generales/cursos.html', context)

def cursos_por_categoria(request, category):
    courses = Course.objects.filter(category=category)
    context = {'category': category, 'courses': courses}
    return render(request, 'generales/cursos_por_categoria.html', context)    


##############################33

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
    
    # Verificamos si el estudiante ya está inscrito en el curso
    enrollment = Enrollment.objects.filter(student=student, course=course).first()
    if enrollment:
        if enrollment.is_active:
            messages.warning(request, 'Ya estás inscrito en este curso.')
            return redirect('course_list')  # Redirigimos a la lista de cursos
        else:
            enrollment.is_active = True
            enrollment.save()
            course.enrolled_students += 1
            course.total_enrolled_students += 1
            course.save()
            messages.success(request, 'Te has matriculado nuevamente en el curso.')
            return redirect('my_courses')  # Redirigimos a la página donde se muestran los cursos matriculados
    
    # Verificamos si el curso está lleno
    if course.is_full:
        messages.error(request, 'Lo sentimos, el curso está lleno.')
        return redirect('course_list')  # Redirige a la lista de cursos si el curso está lleno
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.course = course  # Asegúrate de asignar el curso a la matrícula
            enrollment.save()
            
            # Actualizamos el número de estudiantes inscritos
            course.enrolled_students += 1
            course.total_enrolled_students += 1  # Asegúrate de incrementar también el total
            course.save()  # Guardamos los cambios en el curso

            messages.success(request, 'Te has matriculado exitosamente en el curso.')
            return redirect('my_courses')  # Redirigimos a la página donde se muestran los cursos matriculados
    else:
        form = EnrollmentForm(initial={'course': course})
    
    return render(request, 'generales/enroll.html', {'form': form, 'course': course})



@login_required
def course_list(request):
    student = get_object_or_404(Student, username=request.user)  # Obtener el estudiante actual
    courses = Course.objects.all()  # Obtener todos los cursos
    enrolled_courses = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    
    return render(request, 'generales/cursos.html', {
        'courses': courses,
        'enrolled_courses': list(enrolled_courses),
    })


@login_required
def my_courses(request):
    # Obtener el estudiante asociado al usuario actual
    student = Student.objects.get(username=request.user)

    # Obtener los cursos a los que está matriculado actualmente
    enrolled_courses = Enrollment.objects.filter(student=student, is_active=True)

    # Obtener el historial de inscripciones (expulsiones o desmatriculaciones)
    enrollment_history = EnrollmentHistory.objects.filter(student=student)

    return render(request, 'generales/my_courses.html', {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'enrollment_history': enrollment_history,  # Agregamos el historial al contexto
    })


# views.py

@login_required
def unenroll_course(request, course_id):
    student = get_object_or_404(Student, username=request.user)  # Obtener el estudiante actual
    course = get_object_or_404(Course, id=course_id)  # Obtener el curso

    enrollment = Enrollment.objects.filter(student=student, course=course).first()
    if enrollment:
        enrollment.is_active = False  # Marcar la inscripción como inactiva
        enrollment.save()

        # Registrar el historial cuando el estudiante se desmatricula
        EnrollmentHistory.objects.create(
            student=enrollment.student,
            course=enrollment.course,
            teacher=enrollment.course.teacher,  # Aseguramos que se registre el docente
            grade=enrollment.grade  # Guardamos la nota actual si existe
        )

        # Actualizamos el cupo de estudiantes inscritos en el curso
        if course.enrolled_students > 0:
            course.enrolled_students -= 1
            course.save()  

        messages.success(request, f'Te has desmatriculado del curso "{course.name}".')
    else:
        messages.error(request, f'No estás matriculado en el curso "{course.name}".')

    return redirect('my_courses')



def get_stored_image_path(username):
    # Define el nombre del archivo basado en el nombre de usuario
    path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'face_images')
    if not os.path.exists(path):
        os.makedirs(path)  # Crea el directorio si no existe
    return os.path.join(path, f"{username}.png")

def login_with_face(request):
    if request.method == 'POST':
        # Obtener datos de la imagen y el nombre de usuario
        image_data = request.POST.get('image')
        username = request.POST.get('username')
        
        # Asegúrate de que la imagen se reciba correctamente
        if not image_data or not username:
            return JsonResponse({'error': 'No se recibió la imagen o el nombre de usuario.'})

        # Procesar la imagen aquí (opcionalmente, almacénala)
        # Eliminar el prefijo 'data:image/jpeg;base64,' del dataUrl
        image_data = image_data.split(',')[1]  # Extraer solo los datos base64
        image_data = base64.b64decode(image_data)  # Decodificar la imagen

        # Guardar la imagen en el directorio especificado
        image_path = f'statics/img/face_images/{username}.jpg'
        with open(image_path, 'wb') as img_file:
            img_file.write(image_data)

        return JsonResponse({'message': 'Foto recibida y almacenada.'})

    return render(request, 'generales/login_with_face.html')

def send_confirmation_email(request):
    if request.method == "POST":
        # Obtén el estudiante a partir del usuario autenticado
        try:
            student = Student.objects.get(username=request.user)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el estudiante relacionado con este usuario.'})

        # Obtén los cursos matriculados para el estudiante
        enrolled_courses = Enrollment.objects.filter(student=student)

        # Verifica si el estudiante tiene cursos matriculados
        if enrolled_courses.exists():
            courses_list = ', '.join([enrollment.course.name for enrollment in enrolled_courses])
            subject = "Confirmación de Matrícula"
            message = f"Estás matriculado en los siguientes cursos: {courses_list}"
            from_email = 'noreply@tudominio.com'  # Remitente ficticio

            # Enviar correo
            send_mail(subject, message, from_email, [student.email])  # Envía el correo al email del estudiante

            return JsonResponse({'message': 'Correo enviado correctamente.'})
        else:
            return JsonResponse({'error': 'No tienes cursos matriculados.'})

    return JsonResponse({'error': 'Método no permitido.'})


def password_reset(request):
    context = {}
    return render(request,'generales/password_reset.html',context)



##################


def set_username_password(request, uidb64, token):
    try:
        # Decodificar el uid
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Verifica si el token es válido
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username and password:
                # Asigna el nuevo username y la contraseña
                user.username = username
                user.set_password(password)
                user.save()

                messages.success(request, 'Nombre de usuario y contraseña actualizados exitosamente.')
                return redirect('login')  # Redirige al login

        return render(request, 'generales/set_username_password.html', {'validlink': True, 'user': user})
    else:
        messages.error(request, 'El enlace es inválido o ha caducado.')
        return redirect('password_reset')
    
@login_required
def teacher_panel(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        raise PermissionDenied("No tienes permiso para acceder a esta página.")

    enrollments = Enrollment.objects.filter(course__teacher=teacher)

    if request.method == 'POST':
        # Asignar notas a los estudiantes
        for enrollment in enrollments:
            grade = request.POST.get(f'grade_{enrollment.id}')
            if grade:
                try:
                    enrollment.grade = float(grade)
                    enrollment.save()
                except ValueError:
                    messages.error(request, f'Nota inválida para {enrollment.student.name} {enrollment.student.lastname}.')
        
        # Expulsar (cobrar) a un estudiante
        if 'expel_student' in request.POST:
            enrollment_id = request.POST.get('expel_student')
            try:
                enrollment = Enrollment.objects.get(id=enrollment_id, course__teacher=teacher)
                
                # *** GUARDAR EL HISTORIAL ANTES DE ELIMINAR ***
                EnrollmentHistory.objects.create(
                    student=enrollment.student,
                    course=enrollment.course,
                    teacher=teacher,
                    grade=enrollment.grade,  # Guardamos la nota actual si existe
                    action_type='cobro'  # Especificamos que fue una expulsión/cobro
                )
                
                # *** ACTUALIZAR EL CUPO DEL CURSO ***
                if enrollment.course.enrolled_students > 0:
                    enrollment.course.enrolled_students -= 1  # Reducimos el número de estudiantes activos
                    enrollment.course.save()

                # Una vez registrado el historial, eliminamos la matrícula
                enrollment.delete()

                messages.success(request, 'Estudiante cobrado y eliminado correctamente del curso.')
            except Enrollment.DoesNotExist:
                messages.error(request, 'Inscripción no encontrada o no tienes permiso para cobrar este estudiante.')

        return redirect('teacher_panel')  # Evita resubmisiones de formulario

    # Obtener el historial de inscripciones del docente
    enrollment_history = EnrollmentHistory.objects.filter(teacher=teacher)

    return render(request, 'generales/teacher_panel.html', {
        'enrollments': enrollments,
        'enrollment_history': enrollment_history
    })


def generate_pdf_report(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    enrollments = Enrollment.objects.filter(course__teacher=teacher)

    context = {
        'enrollments': enrollments,
        'teacher': teacher,
        'base_url': request.build_absolute_uri('/')  # Obtener la URL base (http://127.0.0.1:8000/)
    }
    html = render_to_string('generales/pdf_report_template.html', context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')  # O sin ruta si está en PATH

    try:
        pdf = pdfkit.from_string(html, False, configuration=config)
    except Exception as e:
        messages.error(request, f'Error al generar PDF: {e}')
        return redirect('teacher_panel')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_alumnos.pdf"'
    return response


@login_required
def student_history(request):
    student = get_object_or_404(Student, user=request.user)

    # Filtrar el historial del cliente en base al estudiante
    enrollment_history = EnrollmentHistory.objects.filter(student=student)

    return render(request, 'generales/student_history.html', {
        'enrollment_history': enrollment_history
    })


@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    # Cursos activos del estudiante (matriculados actualmente)
    enrolled_courses = Enrollment.objects.filter(student=student, is_active=True)

    # Historial de inscripciones del estudiante (expulsiones y desmatriculaciones)
    enrollment_history = EnrollmentHistory.objects.filter(student=student)

    return render(request, 'generales/student_dashboard.html', {
        'enrolled_courses': enrolled_courses,
        'enrollment_history': enrollment_history,
    })
