from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="ID Telegram-чата для напоминаний по привычкам",
    )

    def __str__(self) -> str:
        return self.username
