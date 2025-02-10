from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import date

User = get_user_model()

class TestUserModel(TestCase):

    """CREATE VALIDATIONS"""

    """
    USER CREATION VALIDATION
    """

    # Create user
    def test_create_user(self):
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            password="SecurePass123",
            dni="12345678",
            role_id=2,
            phone="123-456-7890",
            department="Cardiology",
            birth_date="1990-05-15"
        )

        user.save()
        print("Usuario creado correctamente")

    # Missing required fields        
    def test_create_user_missing_required_fields(self):
        required_fields = ["first_name", "last_name", "email", "password", "dni", "role_id", "department", "birth_date"]

        for field in required_fields:
            user_data = {
                'first_name': "John",
                'last_name': "Doe",
                'email': "johndoe@example.com",
                'password': "SecurePass123",
                'dni': "87654321",
                'role_id': 2,
                'phone': "123-456-7890",
                'department': "Cardiology",
                'birth_date': "1990-05-15"
            }
            
            user_data.pop(field)

            with self.assertRaises(ValidationError):
                user = User(**user_data)
                user.full_clean()
    print("No se ha podido crear el usuario debido a que faltaba información.")

    """
    DNI VALIDATION
    """

    # Duplicate DNI
    def test_create_user_with_duplicate_dni(self): 
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            password="SecurePass123",
            dni="12345678",
            role_id=2,
            phone="123-456-7890",
            department="Cardiology",
            birth_date="1990-05-15"
        )

        user.save()

        with self.assertRaises(ValidationError):
            user2 = User(
                first_name="Another",
                last_name="User",
                email="another@example.com",
                password="SecurePass123",
                dni="12345678",  # 🔥 Mismo DNI, debería fallar
                role_id=3,
                phone="999-999-9999",
                department="Neurology",
                birth_date="1995-08-20"
            )

            user2.save()
    print("No se ha podido crear el usuario debido a que ya existe el dni en la base de datos.")

    # More than 8 digits DNI
    def test_create_user_with_more_than_8_digits_dni(self):
        with self.assertRaises(ValidationError):
            user = User(
                first_name="Jane",
                last_name="Doe",
                email="janedoe@example.com",
                password="SecurePass123",
                dni="1234567843",
                role_id=2,
                phone="123-456-7890",
                department="Cardiology",
                birth_date="1995-08-20"
            )

            user.full_clean()
            user.save()
    print("No se ha podido crear el usuario debido a que el dni debe tener entre 7 y 8 dígitos.")

    # Less than 7 digits DNI
    def test_create_user_with_less_than_7_digits_dni(self):
        with self.assertRaises(ValidationError):
            user = User(
                first_name="Jane",
                last_name="Doe",
                email="janedoe@example.com",
                password="SecurePass123",
                dni="12343",
                role_id=2,
                phone="123-456-7890",
                department="Cardiology",
                birth_date="1995-08-20"
            )

            user.full_clean()
            user.save()
    print("No se ha podido crear el usuario debido a que el dni debe tener entre 7 y 8 dígitos.")

    # Non digits DNI    
    def test_create_user_with_non_digits_dni(self):
        with self.assertRaises(ValidationError):
            user = User(
                first_name="Jane",
                last_name="Doe",
                email="janedoe@example.com",
                password="SecurePass123",
                dni="12_e343",
                role_id=2,
                phone="123-456-7890",
                department="Cardiology",
                birth_date="1995-08-20"
            )

            user.full_clean()
            user.save()
    print("No se ha podido crear el usuario debido a que el dni debe tener entre 7 y 8 dígitos. No se permiten caracteres que no sean números.")

    """
    MAIL VALIDATION
    """

    # Duplicate mail
    def test_create_user_with_duplicate_mail(self): 
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            password="SecurePass123",
            dni="12345678",
            role_id=2,
            phone="123-456-7890",
            department="Cardiology",
            birth_date="1990-05-15"
        )

        user.save()

        with self.assertRaises(ValidationError):
            user2 = User(
                first_name="Another",
                last_name="User",
                email="janedoe@example.com",
                password="SecurePass123",
                dni="12345676",  # 🔥 Mismo DNI, debería fallar
                role_id=3,
                phone="999-999-9999",
                department="Neurology",
                birth_date="1995-08-20"
            )

            user2.save()
    print("No se ha podido crear el usuario debido a que ya existe el mail en la base de datos.")

    """
    DATE VALIDATION
    """

    # Less than 18
    def test_create_user_with_less_18(self):
        underage_date = date.today().replace(year=date.today().year - 17)

        with self.assertRaises(ValidationError):
            user = User(
                first_name="Jane",
                last_name="Doe",
                email="janedoe@example.com",
                password="SecurePass123",
                dni="12345678",
                role_id=2,
                phone="123-456-7890",
                department="Cardiology",
                birth_date=underage_date
            )

            user.full_clean()
            user.save()
    print("No se ha podido crear el usuario. El usuario debe ser mayor a 18 años.")

    """UPDATE VALIDATIONS"""

    """
    USER MODIFICATION VALIDATION
    """
    
    # Name or lastname modification
    def test_update_user(self):
        user = User( 
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            password="SecurePass123",
            dni="12345678",
            role_id=2,
            phone="123-456-7890",
            department="Cardiology",
            birth_date="1990-05-15"
        )
        user.save()

        old_username = user.username

        user.first_name = "John"
        user.last_name = "Smith"
        user.save()

        updated_user = User.objects.get(pk=user.pk)

        self.assertEqual(updated_user.first_name, "John")
        self.assertEqual(updated_user.last_name, "Smith")

        self.assertNotEqual(updated_user.username, old_username)
        self.assertEqual(updated_user.username, "john.smith")