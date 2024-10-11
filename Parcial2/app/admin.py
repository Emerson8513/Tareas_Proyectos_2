from django.contrib import admin
from .models import *


admin.site.register(Course)
# admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Enrollment)

from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    fields = ['name', 'lastname', 'image', 'dpi', 'email']  # Los campos que deseas mostrar en el admin

admin.site.register(Teacher, TeacherAdmin)