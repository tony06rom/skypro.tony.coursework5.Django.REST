from django.db import models
from django.conf import settings


class Habit(models.Model):
    PERIOD_DAILY = "daily"
    PERIOD_WEEKLY = "weekly"

    PERIOD_CHOICES = [
        (PERIOD_DAILY, "Ежедневно"),
        (PERIOD_WEEKLY, "Еженедельно"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    period_type = models.CharField(
        max_length=16,
        choices=PERIOD_CHOICES,
        default=PERIOD_DAILY,
    )
    frequency = models.PositiveIntegerField(default=1)
    time = models.TimeField(help_text="Базовое время напоминания")
    is_pleasant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.user})"


class HabitEvent(models.Model):
    STATUS_DONE = "done"
    STATUS_MISSED = "missed"

    STATUS_CHOICES = [
        (STATUS_DONE, "Выполнена"),
        (STATUS_MISSED, "Пропущена"),
    ]

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="events",
    )
    performed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_DONE,
    )

    def __str__(self) -> str:
        return f"{self.habit} - {self.status}"
