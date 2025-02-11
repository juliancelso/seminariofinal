from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .permissions import IsAdminUser  # Importamos el permiso personalizado

User = get_user_model()

class UserCreateView(APIView):
    permission_classes = [IsAdminUser]  # Solo admins pueden acceder
    
    def post(self, request):
        print(f"🔍 Usuario autenticado: {request.user}")
        print(f"🔍 role_id: {getattr(request.user, 'role_id', 'No tiene role_id')}")
        
        if request.user.role_id != 1:
            return Response({"error": "No tienes permisos para crear usuarios."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        user = User.objects.create(
            email=data.get("email"),
            password=data.get("password"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            role_id=data.get("role_id"),
        )
        return Response({"message": "Usuario creado con éxito"}, status=status.HTTP_201_CREATED)
        print(f"🔍 Usuario autenticado: {request.user}")
        print(f"🔍 role_id: {getattr(request.user, 'role_id', 'No tiene role_id')}")

