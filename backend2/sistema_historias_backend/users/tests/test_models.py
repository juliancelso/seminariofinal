from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    """UPDATE VALIDATION"""

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

    """ DELETE VALIDATION"""

    # Logic low
    def test_soft_delete_user(self):
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
        
        user.delete()
        
        user_from_db = User.all_objects.filter(pk=user.pk).first()

        self.assertIsNotNone(user_from_db)
        self.assertFalse(user_from_db.is_active)

    def test_deleted_user_is_not_queryable(self):
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

        user.delete()

        user_exists = User.objects.filter(email="janedoe@example.com").first()

        self.assertFalse(user_exists)