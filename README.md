![SkyPro_image](/data/images/for_readme_file/SkyPro.png)
![Python_image](/data/images/for_readme_file/Python.png)
![Git_image](/data/images/for_readme_file/Git.png)
![GitHub_image](/data/images/for_readme_file/GitHub.png)

# Пятый модуль. Django.REST. Курсовая работа №5


# 🎯 Трекер привычек

Backend для трекера полезных привычек с Telegram-уведомлениями и Celery.

[![Swagger](https://img.shields.io/badge/Swagger-API-blue)](http://127.0.0.1:8000/swagger/)
[![Tests](https://img.shields.io/badge/Tests-100%25-brightgreen)](https://github.com/tony06rom/skypro.tony.coursework5.Django.REST/actions)
[![Coverage](https://img.shields.io/badge/Coverage-80%25+-orange)](coverage/index.html)

## ✨ Функционал

- ✅ **JWT авторизация** и регистрация через API
- ✅ **CRUD привычек** с валидациями из ТЗ:
  - Максимум 10 привычек с напоминаниями
  - Приятные привычки без времени
  - Частота повторения ≤ 7 дней
- ✅ **Отметка выполнения** и история событий
- ✅ **Статистика** по привычкам
- ✅ **Автоматические напоминания** через **Celery + Redis + Telegram**
- ✅ **Swagger** документация API
- ✅ **Pytest** тесты (100% покрытие CRUD)
- ✅ **Flake8/Black** кодстайл

## 🛠 Запуск

### 1. Клонируй и установи зависимости
bash
git clone https://github.com/tony06rom/skypro.tony.coursework5.Django.REST
cd skypro.tony.coursework5.Django.REST
poetry install

### 2. База данных


poetry run python manage.py migrate
poetry run python manage.py createsuperuser

## 3. Redis (брокер для Celery)
redis-server  # или brew services start redis (macOS)

## 4. Запуск сервисов
# Терминал 1: Celery Worker
poetry run celery -A config worker -P solo -l info

# Терминал 2: Celery Beat (периодические задачи)
poetry run celery -A config beat -l info

# Терминал 3: Django
poetry run python manage.py runserver

## 5. Telegram бот
Создай бота у @BotFather

Добавь TELEGRAM_BOT_TOKEN=твой_токен в .env

Напиши боту /start → получи chat_id

В профиле /api/auth/me/ укажи свой chat_id

📱 API
Swagger | Redoc

| Эндпоинт                   | Метод                 | Описание                 |
|----------------------------|-----------------------| ------------------------ |
| /api/auth/register/        | POST                  | Регистрация              |
| /api/auth/me/              | GET/PATCH             | Профиль                  |
| /api/habits/               | GET/POST              | Список/создание привычек |
| /api/habits/{id}/          | GET/PUT/DELETE        | Привычка                 |
| /api/habits/{id}/complete/ | POST                  | Отметить выполнено       |
| /api/habits/{id}/stats/    | GET                   | Статистика               |
| api/habits/                | GET                   | Свои привычки            |
| /api/habits/public/        | GET                   | Публичные привычки       |
| api/habits/                | POST                  | Создать привычку         |

🧪 Тестирование
# API тесты
poetry run pytest tests/test_habits.py -v
poetry run pytest tests/test_auth.py -v

## 🚀 Быстрый старт с Docker

bash
# 1. Клонировать репозиторий
git clone <репозиторий>

# 2. Создать .env из примера
cp .env.example .env
# Отредактировать пароли в .env

# 3. Запустить
docker-compose up -d --build

## Архитектура (5 сервисов)

| Сервис        | Описание                | Порт                     |
|---------------|-------------------------|--------------------------|
| web           | Django DRF сервер       | 8000                     |
| db            | PostgreSQL 16           | 5433                     |
| redis         | Redis 7 (Celery broker) | Список/создание привычек |
| celery        | Celery worker           | Привычка                 |
| celery-beat   | Периодические задачи    | Отметить выполнено       |

## Структура docker-compose.yml

services:
  web:           # Django + миграции
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db, redis]
  db:            # PostgreSQL с healthcheck
    image: postgres:16-alpine
    env_file: .env
    volumes: [postgres_data:/var/lib/postgresql/data]
  redis:         # Celery broker
    image: redis:7-alpine
  celery:        # Фоновые задачи
    build: .
    env_file: .env
  celery-beat:   # Периодические задачи (каждую минуту)
    build: .
    env_file: .env
volumes: [postgres_data]
networks: [app-network]

## Переменные окружения (.env)

# База данных
POSTGRES_DB=habits
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_HOST=db

# Redis/Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Django
SECRET_KEY=your-secret-key
DEBUG=True

## Полезные команды

# Логи
docker-compose logs -f web        # сервер
docker-compose logs celery        # воркер
docker-compose logs db            # БД

# Консоль в контейнер
docker-compose exec web bash      # Django shell
docker-compose exec db psql       # PostgreSQL

# Перезапуск
docker-compose restart web        # только сервер
docker-compose up -d --build      # пересобрать

# Очистка
docker-compose down -v            # + volumes
===============================================================================================

Этот проект выполняется совместно с [SkyPro](https://sky.pro/)

#### Автор проекта: **Romanenko Anton**