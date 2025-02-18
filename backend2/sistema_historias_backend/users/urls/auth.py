from django.urls import path
from users.views.auth import LoginView  # Importar la vista de login correctamente

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]