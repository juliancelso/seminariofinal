from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"🛑 Verificando permisos para {request.user}")
        return request.user and request.user.is_authenticated and request.user.role_id == 1