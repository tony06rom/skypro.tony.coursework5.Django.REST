from celery import shared_task
from django.utils import timezone

from .models import Habit
from .telegram_utils import send_telegram_message


@shared_task
def send_habit_reminders():
    """Ищет привычки по текущему времени и шлёт напоминания."""
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
    ).select_related("user")
    for habit in habits:
        chat_id = habit.user.telegram_chat_id
        if not chat_id:
            print("DEBUG: Пропуск, нет chat_id")
            continue
        text = f"⏰ Напоминание: {habit.name}\n📝 {habit.description}"
        send_telegram_message(chat_id, text)
