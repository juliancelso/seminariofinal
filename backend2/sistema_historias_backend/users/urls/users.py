from django.urls import path
from users.views.users import UserCreateView, UserListView  # Asegurar que estas vistas existen

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("", UserListView.as_view(), name="user-list"),
]