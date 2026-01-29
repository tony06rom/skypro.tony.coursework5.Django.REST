from django.db import models

from users.models import User


class Habit(models.Model):
    PERIOD_DAILY = 1
    PERIOD_WEEKLY = 7

    PERIOD_CHOICES = [
        (PERIOD_DAILY, "Ежедневно"),
        (PERIOD_WEEKLY, "Еженедельно"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    place = models.CharField("Место", max_length=255, blank=True, null=True)
    time = models.TimeField("Время", help_text="Базовое время напоминания")
    is_pleasant = models.BooleanField("Приятная привычка", default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="used_as_reward_for",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveSmallIntegerField(
        "Периодичность (дни)",
        default=PERIOD_DAILY,
        choices=PERIOD_CHOICES,
    )
    reward = models.CharField(
        "Вознаграждение",
        max_length=255,
        blank=True,
        null=True,
    )
    execution_time = models.PositiveSmallIntegerField(
        "Время на выполнение (сек)",
        default=60,
    )
    is_public = models.BooleanField("Публичная", default=False)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id", "name"]

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
