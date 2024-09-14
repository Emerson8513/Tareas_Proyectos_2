from django.shortcuts import render

def main(request):
    context = {}
    return render(request,'generales/main.html',context)

def course(request):
    context = {}
    return render(request,'generales/course.html',context)

def student(request):
    context = {}
    return render(request,'generales/student.html',context)

def teaching(request):
    context = {}
    return render(request,'generales/teaching.html',context)

def portafolio(request):
    context = {}
    return render(request,'generales/portafolio.html',context)

def register(request):
    context = {}
    return render(request,'generales/register.html',context)