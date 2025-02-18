from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

User = get_user_model()

class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()  # 🔹 Asegurar que usamos APIClient de DRF
        
        # Definir los usuarios de prueba
        self.users = {
            "admin": User(
                first_name="Julián Celso",
                last_name="Ginzburg",
                email="julian.ginzburg@example.com",
                dni="44482922",
                role_id=1,
                phone="1167083386",
                department="Cardiology",
                birth_date="2002-09-21"
            ),
            "coordinator": User(
                first_name="Luciano Danilo",
                last_name="Peluso",
                email="coordinator.user@example.com",
                dni="42058469",
                role_id=2,
                phone="123-456-7890",
                department="Pediatrics",
                birth_date="2002-04-27"
            ),
            "data_entry": User(
                first_name="Celeste Lucía",
                last_name="Ginzburg",
                email="data.user@example.com",
                dni="46258478",
                role_id=3,
                phone="123-456-7890",
                department="Pediatrics",
                birth_date="2005-05-06"
            ),
            "agent": User(
                first_name="Ana Paula",
                last_name="Anaisi",
                email="agent.user@example.com",
                dni="27086668",
                role_id=4,
                phone="123-456-7890",
                department="Pediatrics",
                birth_date="2002-04-27"
            )
        }

        # Crear y guardar usuarios en la BD
        for user in self.users.values():
            user.set_password(f"SecurePass{user.role_id}")
            user.save()

        # Generar tokens de autenticación para cada usuario
        for user in self.users.values():
            Token.objects.get_or_create(user=user)

    def authenticate_as(self, role):
        """Función para autenticarse como un usuario específico"""
        user = self.users[role]
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return user