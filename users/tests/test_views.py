from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

User = get_user_model()

class TestUserView(TestCase):
    def setUp(self):
        """Se ejecuta antes de cada test para crear usuarios de prueba."""
        self.admin = User.objects.create(
            first_name="Julián Celso",
            last_name="Ginzburg",
            email="julian.ginzburg@example.com",
            password="SecurePass123",
            dni="44482922",
            role_id=1,
            phone="1167083386",
            department="Cardiology",
            birth_date="2002-09-21"
        )

        self.coordi = User.objects.create(
            first_name="Luciano Danilo",
            last_name="Peluso",
            email="luciano.peluso@example.com",
            password="SecurePass123",
            dni="42058469",
            role_id=2,
            phone="123-456-7890",
            department="Pediatrics",
            birth_date="2002-04-27"
        )

        self.data = User.objects.create(
            first_name="Celeste Lucía",
            last_name="Ginzburg",
            email="celeste.ginzburg@example.com",
            password="SecurePass123",
            dni="46258478",
            role_id=3,
            phone="123-456-7890",
            department="Pediatrics",
            birth_date="2005-05-06"
        )

        self.agent = User.objects.create(
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