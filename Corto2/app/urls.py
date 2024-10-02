# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.paginaprincipal, name='paginaprincipal'),
    path('student/', views.student, name='estudiantes'),
    path('teaching/', views.teaching, name='docentes'),
    path('cursos/', views.cursos, name='cursos'),
    path('portafolio/', views.portafolio, name='portafolio'),
    path('register/', views.register, name='registro'),
    path('login/', views.login_view, name='login'),  # URL para iniciar sesión
    path('logout/', views.logout_view, name='logout'),  # URL para cerrar sesión
]
