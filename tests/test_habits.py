import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
class TestHabits(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.url = "/api/habits/"

    def test_create_habit(self):
        """Создание привычки."""
        data = {
            "name": "Чтение",
            "description": "10 страниц в день",
            "period_type": "daily",
            "frequency": 1,
            "time": "21:00:00",  # ← обязательно!
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
        # Создаём привычку с time
        Habit.objects.create(
            user=self.user,
            name="Тест1",
            period_type="daily",
            frequency=1,
            time="09:00:00",  # ← обязательно!
            is_pleasant=False,
            is_public=False,
        )
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_complete_habit(self):
        """Отметка выполнения."""
        habit = Habit.objects.create(
            user=self.user,
            name="Тест",
            period_type="daily",
            frequency=1,
            time="12:00:00",  # ← обязательно!
            is_pleasant=False,
            is_public=False,
        )
        url = f"{self.url}{habit.id}/complete/"
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_habit_limit_reminders(self):
        """Максимум 10 привычек с напоминаниями."""
        # Создаём 10 привычек с time
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                name=f"Limit {i}",
                period_type="daily",
                frequency=1,
                time="09:00:00",
                is_pleasant=False,
                is_public=False,
            )

        data = {
            "name": "11-я привычка",
            "period_type": "daily",
            "frequency": 1,
            "time": "10:00:00",  # 11-я с временем
            "is_pleasant": False,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "10 привычек" in str(response.data)

    def test_create_pleasant_no_time(self):
        """Приятная привычка не может иметь время."""
        data = {
            "name": "Приятная",
            "period_type": "daily",
            "frequency": 1,
            "time": "10:00:00",
            "is_pleasant": True,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Приятные привычки не могут иметь время" in str(response.data["non_field_errors"][0])

    def test_create_frequency_limit(self):
        """Частота не больше 7."""
        data = {
            "name": "Частая",
            "period_type": "weekly",
            "frequency": 8,  # больше 7
            "time": "10:00:00",
            "is_pleasant": False,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "больше 7 дней" in str(response.data) or "frequency" in str(response.data)
