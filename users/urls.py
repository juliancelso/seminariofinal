from django.urls import path
from .views import UserCreateView, UserListView, LoginView

urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='users-create'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('login/', LoginView.as_view(), name='login'),
]