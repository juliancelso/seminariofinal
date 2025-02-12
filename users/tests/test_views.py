from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestUserView(APITestCase):
    def setUp(self):
        """Se ejecuta antes de cada test para crear usuarios de prueba."""
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

        # Asignar la contraseña antes de guardar cada usuario
        for user in self.users.values():
            user.set_password(f"SecurePass{user.role_id}")  # 🔹 Encripta la contraseña
            user.save()

        # Crear los tokens para cada usuario
        for user in self.users.values():
            Token.objects.get_or_create(user=user)

    def test_user_creation_permissions(self):
        for role, user in self.users.items():
            token = Token.objects.get(user=user)
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

            data = {
                "email": f"{role}_usuario@example.com",
                "password": "testpass123",
                "first_name": "Nuevo",
                "last_name": "Usuario",
                "role_id": 3,
                "dni": f"1234567{user.role_id}",
                "department": "Pediatrics",
                "birth_date": "2000-01-01"
            }

            response = self.client.post('/api/users/create/', data)

            print(f"Respuesta para {role}: {response.status_code} - {response.data}")

            if user.role_id == 1:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"El admin debería poder crear usuarios pero falló para {role}")
                self.assertTrue(User.objects.filter(email=data["email"]).exists())
            else:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, f"El rol {role} NO debería poder crear usuarios pero la API lo permitió")

    def test_invalid_email(self):
        admin = self.users["admin"]
        token = Token.objects.get(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            "email": "email-invalido",
            "password": "testpass123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "role_id": 3,
            "dni": "12345678",
            "department": "Pediatrics",
            "birth_date": "2000-01-01"
        }

        response = self.client.post('/api/users/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["errors"])

    def test_invalid_dni_length(self):
        admin = self.users["admin"]
        token = Token.objects.get(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            "email": "dni.usuario@example.com",
            "password": "testpass123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "role_id": 3,
            "dni": "12345",
            "department": "Pediatrics",
            "birth_date": "2000-01-01"
        }

        response = self.client.post('/api/users/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("dni", response.data["errors"])




    def test_invalid_dni_characters(self):
        admin = self.users["admin"]
        token = Token.objects.get(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            "email": "dni.usuario@example.com",
            "password": "testpass123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "role_id": 3,
            "dni": "1234abcd",
            "department": "Pediatrics",
            "birth_date": "2000-01-01"
        }

        response = self.client.post('/api/users/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("dni", response.data["errors"])


    def test_invalid_birth_date(self):
        admin = self.users["admin"]
        token = Token.objects.get(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            "email": "fecha.usuario@example.com",
            "password": "testpass123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "role_id": 3,
            "dni": "12345678",
            "department": "Pediatrics",
            "birth_date": "fecha-invalida"
        }

        response = self.client.post('/api/users/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data["errors"])


    def test_underage_user(self):
        admin = self.users["admin"]
        token = Token.objects.get(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            "email": "menor.usuario@example.com",
            "password": "testpass123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "role_id": 3,
            "dni": "12345678",
            "department": "Pediatrics",
            "birth_date": "2010-01-01"
        }

        response = self.client.post('/api/users/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data["errors"])

    def test_admin_can_view_all_users(self):
        admin = self.users["admin"]
        token = Token.objects.get(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.users))


    def test_non_admin_can_only_view_self(self):
        user = self.users["agent"]
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)


    def test_unauthenticated_request_is_rejected(self):
        self.client.credentials()

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_successful(self):
        """Un usuario puede iniciar sesión con email y contraseña correctos."""
        user = self.users["admin"]
        token = Token.objects.get(user=user)

        data = {
            "email": user.email,
            "password": f"SecurePass{user.role_id}"
        }

        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], token.key) 

    def test_login_invalid_email(self):
        data = {
            "email": "email-invalido@example.com",
            "password": "SecurePass123"
        }

        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


    def test_login_invalid_password(self):
        user = self.users["admin"]

        data = {
            "email": user.email,
            "password": "WrongPassword123"
        }

        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


    def test_login_missing_fields(self):
        data = {"email": "julian.ginzburg@example.com"}

        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)