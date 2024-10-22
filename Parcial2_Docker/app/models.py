from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import models

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    dpi = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"
    
    def __str__(self):
        return f"{self.name} {self.lastname}"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
# models.py

# models.py

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('taxi', 'Taxi'),
        ('motoraton', 'Moto Raton'),
        ('tuctuc', 'Tuc Tuc'),
        ('mudanza', 'Mudanza'),
    ]
    name = models.CharField(max_length=50, null=True, blank=True, default='Unnamed Course')  # Añadir un valor por defecto
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50, default='N/A')
    placa = models.CharField(max_length=10, default='N/A')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    capacity = models.IntegerField(default=1)
    enrolled_students = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='taxi')
    total_enrolled_students = models.IntegerField(default=0)  # Nuevo campo
    start_location = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo
    end_location = models.CharField(max_length=255, null=True, blank=True)    # Nuevo campo
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.name if self.name else 'Unnamed Course'
    
    @property
    def is_full(self):
        '''Devuelve True si el curso está lleno, False en caso contrario.'''
        return self.enrolled_students >= self.capacity

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Student(models.Model):
    name = models.CharField(max_length=50)
    lastname= models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    dpi= models.CharField(max_length=50)
    date = models.DateField()
    telefhone= models.CharField(max_length=50)
    username= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email= models.CharField(max_length=50)
    password= models.CharField(max_length=50)
    password_check= models.CharField(max_length=50)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

    #axes

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_attempts = models.IntegerField(default=0)  # Almacena los intentos fallidos
    is_locked = models.BooleanField(default=False)    # Indica si la cuenta está bloqueada
    lockout_time = models.DateTimeField(null=True, blank=True)  # Tiempo de bloqueo (si aplica)
    face_encoding = models.BinaryField(null=True, blank=True) 

    def unlock(self):
        """Desbloquea el usuario si ha pasado el tiempo de bloqueo."""
        if self.lockout_time and timezone.now() >= self.lockout_time:
            self.is_locked = False
            self.failed_attempts = 0
            self.lockout_time = None
            self.save()


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Agregar campo para notas
    start_location = models.CharField(max_length=255, null=True, blank=True)
    end_location = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Agregar campo para desactivar matrícula

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"
    

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['start_location', 'end_location', 'course']
        widgets = {
            'course': forms.HiddenInput(),
        }

class EnrollmentHistory(models.Model):
    ACTION_CHOICES = [
        ('desmatriculacion', 'Desmatriculación'),
        ('cobro', 'Cobro/Expulsión'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.FloatField(null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, default='desmatriculacion')
    expulsion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.course} - {self.expulsion_date}'




class CustomerServiceForm(models.Model):
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    puntualidad = models.CharField(max_length=255)
    limpieza_vehiculo = models.CharField(max_length=255)
    asistencia_conductor = models.CharField(max_length=255)
    conocimiento_rutas = models.CharField(max_length=255)
    seguridad = models.CharField(max_length=255)
    tarifas = models.CharField(max_length=255)
    facilidad_reserva = models.CharField(max_length=255)
    atencion_cliente = models.CharField(max_length=255)
    comodidad_vehiculo = models.CharField(max_length=255)
    experiencia_general = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Servicio al Cliente - {self.fecha_creacion}'
    


class ActionHistory(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} {self.object_id} at {self.timestamp}"
class RequestHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()
    response_body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.method} {self.path} at {self.timestamp}"