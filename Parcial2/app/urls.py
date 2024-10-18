# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import send_confirmation_email

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
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),
    path('login_with_face/', views.login_with_face, name='login_with_face'),
    path('send_confirmation_email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='generales/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='generales/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='generales/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='generales/password_reset_complete.html'), name='password_reset_complete'),
    path('set_username_password/<uidb64>/<token>/', views.set_username_password, name='set_username_password'),
    path('teacher_panel/', views.teacher_panel, name='teacher_panel'),
    # path('generate_pdf_report/', views.generate_pdf_report, name='generate_pdf_report'),
    path('cursos/<str:category>/', views.cursos_por_categoria, name='cursos_por_categoria'),
    path('rutas/', views.rutas, name='rutas'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_invoice_pdf/<int:enrollment_id>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),

]
