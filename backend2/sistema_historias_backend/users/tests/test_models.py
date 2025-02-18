from django.core.exceptions import ValidationError
from datetime import date
from users.tests.base_test import BaseTestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserModel(BaseTestCase):
    def test_create_valid_user(self):
        """Debe permitir crear un usuario válido"""
        user = self.users["admin"]
        user.full_clean()
        user.save()

    def assert_user_creation_fails(self, **invalid_fields):
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "SecurePass123",
            "dni": "12345678",
            "role_id": 2,
            "phone": "123-456-7890",
            "department": "Cardiology",
            "birth_date": "1990-01-01",
        }
        user_data.update(invalid_fields)

        with self.assertRaises(ValidationError):
            user = User(**user_data)
            user.full_clean()

    def test_create_user_missing_fields(self):
        """🔹 Debe fallar si falta un campo obligatorio"""
        required_fields = ["first_name", "last_name", "email", "dni", "role_id", "department", "birth_date"]

        for field in required_fields:
            self.assert_user_creation_fails(**{field: None})

    def test_create_user_duplicate_dni(self):
        """🔹 No debe permitir crear un usuario con un DNI duplicado"""
        self.assert_user_creation_fails(dni="44482922")  # Ya existe

    def test_create_user_invalid_dni(self):
        """🔹 No debe permitir DNI con caracteres no numéricos o longitud incorrecta"""
        self.assert_user_creation_fails(dni="abc1234")
        self.assert_user_creation_fails(dni="123")
        self.assert_user_creation_fails(dni="123456789")

    def test_create_user_duplicate_email(self):
        """🔹 No debe permitir emails duplicados"""
        self.assert_user_creation_fails(email="julian.ginzburg@example.com")

    def test_create_underage_user(self):
        """🔹 No debe permitir usuarios menores de 18 años"""
        underage_date = date.today().replace(year=date.today().year - 17)
        self.assert_user_creation_fails(birth_date=underage_date)