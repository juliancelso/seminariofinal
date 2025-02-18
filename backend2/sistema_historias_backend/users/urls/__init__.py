from django.urls import include, path

urlpatterns = [
    path("auth/", include("users.urls.auth")),
    path("dashboard/", include("users.urls.dashboard")),
    path("users/", include("users.urls.users")),
]