import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
class TestHabits(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            telegram_chat_id="123456789",
        )
        self.client.force_authenticate(user=self.user)
        self.url = "/api/habits/"
        self.public_url = "/api/habits/public/"

    def test_create_habit(self):
        """Создание привычки."""
        data = {
            "name": "Чтение",
            "place": "Дом",
            "time": "21:00:00",
            "periodicity": 1,
            "execution_time": 60,
            "is_pleasant": False,
            "is_public": False,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Чтение"

        # Проверяем привязку к пользователю
        habit = Habit.objects.get(id=response.data["id"])
        assert habit.user == self.user

    def test_list_habits(self):
        """Список своих привычек."""
        # Создаём привычку
        Habit.objects.create(
            user=self.user,
            name="Тест1",
            place="Дом",
            time="09:00:00",
            periodicity=1,
            execution_time=60,
            is_pleasant=False,
            is_public=False,
        )
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_public_habits(self):
        """Публичные привычки."""
        Habit.objects.filter(is_public=True).delete()
        Habit.objects.create(
            user=self.user,
            name="Публичная",
            place="Парк",
            time="08:00:00",
            periodicity=1,
            execution_time=60,
            is_public=True,
        )
        self.client.force_authenticate(user=None)
        response = self.client.get(self.public_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Публичная"

    def test_pagination(self):
        """Пагинация 5 на страницу."""
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                name=f"Тест {i}",
                place="Дом",
                time="09:00:00",
                periodicity=1,
                execution_time=60,
                is_pleasant=False,
                is_public=False,
            )

        # Пагинация своих
        response = self.client.get(f"{self.url}?page=1")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 5
        assert response.data["count"] == 7

        # Пагинация публичных
        self.client.force_authenticate(user=None)
        response = self.client.get(f"{self.public_url}?page=1")
        assert "results" in response.data

    def test_validation_periodicity(self):
        """Периодичность > 7 — ошибка."""
        data = {
            "name": "Редкая",
            "place": "Дом",
            "time": "10:00:00",
            "periodicity": 8,
            "execution_time": 60,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "periodicity" in str(response.data)

    def test_validation_execution_time(self):
        """Время выполнения > 120 — ошибка."""
        data = {
            "name": "Долгая",
            "place": "Дом",
            "time": "10:00:00",
            "periodicity": 1,
            "execution_time": 130,  # ← ОШИБКА!
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "120 секунд" in str(response.data)

    def test_validation_pleasant_reward(self):
        """Приятная + награда — ошибка."""
        data = {
            "name": "Приятная",
            "place": "Дом",
            "time": "10:00:00",
            "periodicity": 1,
            "execution_time": 60,
            "is_pleasant": True,
            "reward": "Кофе",  # ← ОШИБКА!
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "приятной привычки" in str(response.data)
