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
    path('loginteacher/', views.login_view_teacher, name='loginteacher'),  # URL para iniciar sesión
    path('logout/', views.logout_view, name='logout'),  # URL para cerrar sesión
    path('courses/', views.course_list, name='course_list'),  # La vista que lista los cursos
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),  # La vista para matricular
    path('my_courses/', views.my_courses, name='my_courses'),  # Asegúrate de que esté aquí
]
