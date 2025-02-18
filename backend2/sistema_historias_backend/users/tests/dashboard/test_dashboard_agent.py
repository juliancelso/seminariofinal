from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestDashboardAgent(APITestCase):
    def setUp(self):
        super().setUp()
        self.agent = User(
            first_name="Ana Paula",
            last_name="Anaisi",
            email="agent.user@example.com",
            dni="27086668",
            role_id=4,
            phone="123-456-7890",
            department="Pediatrics",
            birth_date="2002-04-27"
        )
        self.agent.set_password("SecurePass4")
        self.agent.save()

        self.token = Token.objects.create(user=self.agent)

    def test_dashboard_agent(self):
        """El agente debe ver las opciones correctas en el Dashboard."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/dashboard/agent/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["actions"], ["Ingresar nuevo registro", "Perfil", "Cerrar sesión"])
