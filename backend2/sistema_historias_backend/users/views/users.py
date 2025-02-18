from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import re
from datetime import datetime, date
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

class UserListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"error": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.role_id == 1:
            users = User.objects.all().values("id", "email", "first_name", "last_name", "role_id", "dni", "department", "birth_date")
            return Response(users, status=status.HTTP_200_OK)
        else:
            user_data = {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "role_id": request.user.role_id,
                "dni": request.user.dni,
                "department": request.user.department,
                "birth_date": request.user.birth_date,
            }
            return Response(user_data, status=status.HTTP_200_OK)

class UserCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role_id != 1:
            return Response({"error": "No tienes permisos para crear usuarios."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        errors = {}

        if "@" not in data.get("email", ""):
            errors["email"] = "El email no es válido."

        if not re.fullmatch(r"^\d{7,8}$", data.get("dni", "")):
            errors["dni"] = "El DNI debe tener 7 u 8 dígitos numéricos."

        try:
            birth_date = datetime.strptime(data.get("birth_date", ""), "%Y-%m-%d").date()
            age = (date.today() - birth_date).days // 365
            if age < 18:
                errors["birth_date"] = "El usuario debe ser mayor de 18 años."
        except ValueError:
            errors["birth_date"] = "Fecha de nacimiento no válida."

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            role_id=data.get("role_id"),
            dni=data.get("dni"),
            department=data.get("department"),
            birth_date=data.get("birth_date")
        )
        user.set_password(data.get("password"))
        user.save()

        return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)