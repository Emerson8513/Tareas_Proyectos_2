from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    teacher = models.CharField(max_length=50)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    codigocurso = models.CharField(max_length=50)
    capacity = models.IntegerField(default=30)  # Capacidad máxima del curso
    enrolled_students = models.IntegerField(default=0)  # Almacena el número de estudiantes inscritos
    
    def __str__(self):
        return self.name
    
    @property
    def is_full(self):
        """Verifica si el curso ha alcanzado su capacidad máxima."""
        return self.enrolled_students >= self.capacity

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    dpi = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

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
    
    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"
    

