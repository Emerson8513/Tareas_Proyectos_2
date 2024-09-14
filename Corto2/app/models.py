from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    teacher = models.CharField(max_length=50)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    codigocurso = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Teacher(models.Model):
    name = models.CharField(max_length=50)
    lastname= models.TextField()
    image = models.ImageField(null=True, blank=True)
    dpi= models.CharField(max_length=50)
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
    
class Student(models.Model):
    name = models.CharField(max_length=50)
    lastname= models.TextField()
    image = models.ImageField(null=True, blank=True)
    dpi= models.CharField(max_length=50)
    date = models.DateField()
    telefhone= models.CharField(max_length=50)
    username= models.OneToOneField('Student', on_delete=models.CASCADE, null=True, blank=True)
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