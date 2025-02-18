from rest_framework import status
from users.tests.base_test import BaseTestCase

class TestUserView(BaseTestCase):

    def test_login_successful(self):
        """🔹 El login debe devolver un token válido"""
        user = self.users["admin"]
        response = self.client.post("/api/auth/login/", {
            "email": user.email,
            "password": f"SecurePass{user.role_id}"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        """🔹 No debe permitir login con credenciales incorrectas"""
        user = self.users["admin"]
        response = self.client.post("/api/auth/login/", {
            "email": user.email,
            "password": "WrongPassword"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_access(self):
        """🔹 El dashboard debe estar accesible solo para usuarios autenticados"""
        self.authenticate_as("admin")
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)