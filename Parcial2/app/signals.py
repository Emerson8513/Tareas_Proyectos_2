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
