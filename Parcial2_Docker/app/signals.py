from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import Teacher
from profiles.models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Teacher, Course, Student, UserProfile, Enrollment, EnrollmentHistory, CustomerServiceForm, ActionHistory
@receiver(post_save, sender=Teacher)

def create_user_for_teacher(sender, instance, created, **kwargs):
    if created and instance.email:  # Solo si se crea un nuevo Teacher y tiene un email
        # Crear un username temporal basado en el email del profesor
        username = instance.email.split('@')[0] + "teacher"
        user = User.objects.create_user(username=username, email=instance.email)

        # Asocia el User creado con el Teacher
        instance.user = user
        instance.save()

        # Generar el enlace personalizado para configurar nombre de usuario y contraseña
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = reverse('set_username_password', kwargs={'uidb64': uid, 'token': token})
        full_reset_link = f"{settings.SITE_URL}{reset_link}"

        # Enviar el correo electrónico con el enlace
        send_mail(
            'Configura tu cuenta',
            f"Hola {instance.name},\n\nTu cuenta ha sido creada. Por favor, configura tu nombre de usuario y contraseña en el siguiente enlace: {full_reset_link}",
            'admin@miapp.com',
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Teacher)
def update_profile_image(sender, instance, created, **kwargs):
    """Cuando se crea o actualiza un Teacher, actualizar la imagen en Profile"""
    if instance.user:
        profile, _ = Profile.objects.get_or_create(user=instance.user)
        if instance.image:
            profile.photo = instance.image  # Copiar la imagen del Teacher a Profile
            profile.save()

@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Course)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=UserProfile)
@receiver(post_save, sender=Enrollment)
@receiver(post_save, sender=EnrollmentHistory)
@receiver(post_save, sender=CustomerServiceForm)
def log_save(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    ActionHistory.objects.create(
        user=instance.user if hasattr(instance, 'user') else None,
        action=action,
        model_name=sender.__name__,
        object_id=instance.id,
        changes=str(instance.__dict__)
    )

@receiver(post_delete, sender=Teacher)
@receiver(post_delete, sender=Course)
@receiver(post_delete, sender=Student)
@receiver(post_delete, sender=UserProfile)
@receiver(post_delete, sender=Enrollment)
@receiver(post_delete, sender=EnrollmentHistory)
@receiver(post_delete, sender=CustomerServiceForm)
def log_delete(sender, instance, **kwargs):
    ActionHistory.objects.create(
        user=instance.user if hasattr(instance, 'user') else None,
        action='delete',
        model_name=sender.__name__,
        object_id=instance.id,
        changes=str(instance.__dict__)
    )