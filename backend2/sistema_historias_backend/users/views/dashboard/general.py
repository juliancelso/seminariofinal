from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role_actions = {
            1: ["Gestionar usuarios", "Ver reportes", "Perfil", "Cerrar sesión"],
            2: ["Gestionar historiales médicos", "Perfil", "Cerrar sesión"],
            3: ["Ingresar nuevo historial médico", "Visualizar historiales médicos", "Perfil", "Cerrar sesión"],
            4: ["Ingresar nuevo registro", "Perfil", "Cerrar sesión"],
        }

        actions = role_actions.get(request.user.role_id, ["Perfil", "Cerrar sesión"])
        return Response({"actions": actions}, status=200)
