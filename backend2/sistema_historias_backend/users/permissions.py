from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permiso para administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == 1

class IsCoordinator(permissions.BasePermission):
    """Permiso para coordinadores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == 2

class IsDataEntry(permissions.BasePermission):
    """Permiso para Data Entry"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == 3

class IsAgent(permissions.BasePermission):
    """Permiso para Agentes"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_id == 4