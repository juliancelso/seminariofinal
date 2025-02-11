from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestUserView(APITestCase):
    def setUp(self):
        self.users = {
            "admin": User.objects.create(
                first_name="Julián Celso",
                last_name="Ginzburg",
                email="julian.ginzburg@example.com",
                password="SecurePass123",
                dni="44482922",
                role_id=1,
                phone="1167083386",
                department="Cardiology",
                birth_date="2002-09-21"
            ),
            "coordinator": User.objects.create(
                first_name="Luciano Danilo",
                last_name="Peluso",
                email="luciano.peluso@example.com",
                password="SecurePass123",
                dni="42058469",
                role_id=2,
                phone="123-456-7890",
                department="Pediatrics",
                birth_date="2002-04-27"
            ),
            "data_entry": User.objects.create(
                first_name="Celeste Lucía",
                last_name="Ginzburg",
                email="celeste.ginzburg@example.com",
                password="SecurePass123",
                dni="46258478",
                role_id=3,
                phone="123-456-7890",
                department="Pediatrics",
                birth_date="2005-05-06"
            ),
            "agent": User.objects.create(
                first_name="Ana Paula",
                last_name="Anaisi",
                email="ana.anaisi@example.com",
                password="SecurePass123",
                dni="27086668",
                role_id=4,
                phone="123-456-7890",
                department="Pediatrics",
                birth_date="2002-04-27"
            )
        }
        
        for user in self.users.values():
            Token.objects.create(user=user)

    def test_user_creation_permissions(self):
        data = {
            "email": "nuevo.usuario@example.com",
            "password": "testpass123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "role_id": 3,
            "dni": "12345678",  # 🔹 Agregado
            "department": "Pediatrics",  # 🔹 Agregado
            "birth_date": "2000-01-01"  # 🔹 Agregado
        }
        
        for role, user in self.users.items():
            token = Token.objects.get(user=user)
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
            
            response = self.client.post('/api/users/create/', data)
            
            if user.role_id == 1:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"El admin debería poder crear usuarios pero falló para {role}")
                self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
            else:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, f"El rol {role} NO debería poder crear usuarios pero la API lo permitió")