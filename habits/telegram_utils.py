import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str) -> None:
    """Отправляет сообщение в Telegram."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        print("Failed to send Telegram message")
