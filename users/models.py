from django.contrib.auth.models import AbstractUser
from django.db import models  # Para definir los campos

class User(AbstractUser):
    ROLE_CHOICES = [
        (1, 'Administrator'),
        (2, 'Coordinator'),
        (3, 'Data Entry'),
        (4, 'Agent')
    ]
    dni = models.CharField(max_length=15, unique=True)
    role_id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=4)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Genera automáticamente el username basado en el primer nombre y primer apellido"""
        if not self.username:  # Solo genera un username si no existe uno
            first_name = self.first_name.split()[0].lower()  # Primer nombre en minúsculas
            last_name = self.last_name.split()[0].lower()  # Primer apellido en minúsculas
            base_username = f"{first_name}.{last_name}"
            username = base_username
            counter = 1

            # Asegurarnos de que el username sea único
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            self.username = username  # Asigna el username final

        super().save(*args, **kwargs)  # Guarda el usuario normalmente

    groups = None
    user_permissions = None