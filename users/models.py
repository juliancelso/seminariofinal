from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, datetime

def validate_dni(value):
    if not value.isdigit():
        raise ValidationError("DNI must contain only numbers.")
    if len(value) not in [7, 8]:
        raise ValidationError("DNI must be 7 or 8 digits long.")

class User(AbstractUser):
    ROLE_CHOICES = [
        (1, 'Administrator'),
        (2, 'Coordinator'),
        (3, 'Data Entry'),
        (4, 'Agent')
    ]

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)
    dni = models.CharField(max_length=8, unique=True, blank=False, validators=[validate_dni])
    role_id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=4, blank=False)
    department = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=False)

    def clean(self):
        self.validate_birth_date()

    def validate_birth_date(self):
        if not self.birth_date:
            return  

        if isinstance(self.birth_date, str):
            self.birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d").date()

        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

        if age < 18:
            raise ValidationError("User must be at least 18 years old.")

    def generate_username(self):

        first_name = self.first_name.split()[0].lower()
        last_name = self.last_name.split()[0].lower()
        base_username = f"{first_name}.{last_name}"
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exclude(pk=self.pk).exists():
            username = f"{base_username}{counter}"
            counter += 1

        self.username = username

    def save(self, *args, **kwargs):
        if self.pk:
            existing_user = User.objects.get(pk=self.pk)
            if self.first_name != existing_user.first_name or self.last_name != existing_user.last_name:
                self.generate_username()
        else:
            self.generate_username()

        self.full_clean()
        super().save(*args, **kwargs)

    groups = None
    user_permissions = None