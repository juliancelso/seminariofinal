from django.urls import include, path

urlpatterns = [
    path('auth/', include('users.urls.auth')),  # 🔹 Maneja el login
    path('users/', include('users.urls.users')),  # 🔹 Maneja los usuarios (solo si existe el archivo users.py)
    path('dashboard/', include('users.urls.dashboard')),  # 🔹 Maneja el dashboard
]