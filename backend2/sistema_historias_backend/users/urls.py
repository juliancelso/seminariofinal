from django.urls import path
from .views import UserCreateView, UserListView, LoginView, DashboardView

urlpatterns = [
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]