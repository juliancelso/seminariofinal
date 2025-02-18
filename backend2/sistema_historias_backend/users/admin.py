from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models.user import User

class CustomUserAdmin(UserAdmin):
    pass