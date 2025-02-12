from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import re
from datetime import datetime, date

User = get_user_model()

class UserCreateView(APIView):
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