from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.paginaprincipal, name='paginaprincipal'),
    path('student/', views.student, name='estudiantes'),
    path('teaching/', views.teaching, name='docentes'),
    path('course/', views.course, name='cursos'),
    path('portafolio/', views.portafolio, name='portafolio'),
    path('register/', views.register, name='registro'),
    path('cursos/', views.cursos, name='cursos'),
]