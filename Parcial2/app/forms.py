from django import forms
from .models import Enrollment
from .models import CustomerServiceForm
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']
        widgets = {
            'course': forms.HiddenInput()
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerServiceForm
        fields = ['puntualidad', 'limpieza_vehiculo', 'asistencia_conductor', 'conocimiento_rutas', 'seguridad', 'tarifas', 'facilidad_reserva', 'atencion_cliente', 'comodidad_vehiculo', 'experiencia_general']
