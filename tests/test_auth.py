import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@pytest.mark.django_db
class TestAuth(APITestCase):
    def test_register(self):
        """Тест регистрации."""
        url = "/api/auth/register/"
        data = {
            "username": "testuser",
            "password": "testpass123",
            "telegram_chat_id": "123456789",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "testuser"

        # Проверяем, что пользователь создался
        user = User.objects.get(username="testuser")
        assert user.telegram_chat_id == "123456789"

    def test_register_duplicate_username(self):
        """Дубликат username."""
        User.objects.create_user(username="testuser", password="testpass123")
        url = "/api/auth/register/"
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
