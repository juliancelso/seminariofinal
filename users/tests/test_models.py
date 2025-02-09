from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserModel(TestCase):
    def test_create_user(self):
        user = {
            'first_name': "John",
            'last_name': "Doe",
            'username': 'john.doe',
            'email': "johndoe@example.com",
            'password': "SecurePass123",
            'dni': "12345678",
            'role_id': 2,  # Supongamos que 2 es Coordinador
            'phone': "123-456-7890",
            'department': "Cardiology",
            'birth_date': "1990-05-15"
        }

        # Crear el usuario en la base de datos de prueba
        User.objects.create_user(**user)

        # Obtener el usuario recién creado
        user_created = User.objects.get(email="johndoe@example.com")

        # Verificar que los datos sean correctos
        self.assertEqual(user_created.email, "johndoe@example.com")
        self.assertEqual(user_created.dni, "12345678")
