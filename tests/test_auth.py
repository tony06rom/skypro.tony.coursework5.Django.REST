import pytest
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuth(APITestCase):
    def setUp(self):
        self.url_register = "/api/auth/register/"
        self.url_token = "/api/auth/token/"

    def test_register(self):
        """Тест регистрации."""
        data = {
            "email": "newuser@example.com",  # ← email вместо username!
            "password": "testpass123",
            "telegram_chat_id": "987654321",
        }
        response = self.client.post(self.url_register, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_register_duplicate_email(self):
        """Дубликат email."""
        # Создаём первого
        User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            telegram_chat_id="123456789",
        )

        data = {
            "email": "test@example.com",  # ← Дубликат!
            "password": "testpass123",
            "telegram_chat_id": "987654321",
        }
        response = self.client.post(self.url_register, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token(self):
        """Получение токена."""
        user = User.objects.create_user(
            email="tokenuser@example.com",
            password="testpass123",
            telegram_chat_id="111222333",
        )

        data = {
            "email": "tokenuser@example.com",  # ← email!
            "password": "testpass123",
        }
        response = self.client.post(self.url_token, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
