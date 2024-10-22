from django.contrib import admin
from .models import *
from .models import Teacher


admin.site.register(Course)
# admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Enrollment)

admin.site.register(CustomerServiceForm)

class TeacherAdmin(admin.ModelAdmin):
    fields = ['name', 'lastname', 'image', 'dpi', 'email']  # Los campos que deseas mostrar en el admin

admin.site.register(Teacher, TeacherAdmin)

admin.site.register(ActionHistory)
admin.site.register(RequestHistory)