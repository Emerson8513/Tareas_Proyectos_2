from django.shortcuts import render
from .models import *

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

def register(request):
    context = {}
    return render(request,'generales/register.html',context)

def cursos(request):
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request,'generales/cursos.html',context)