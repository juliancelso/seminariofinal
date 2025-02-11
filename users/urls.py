from django.urls import path
from .views import UserCreateView  # Importar la vista correctamente

urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='users-create'),  # Definir correctamente la URL
]