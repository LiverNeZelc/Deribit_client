# Deribit client

Этот проект собирает текущие index price BTC/USD и ETH/USD с Deribit, сохраняет их в PostgreSQL и делает доступными через внешнее API на FastAPI. Для регулярного сбора данных используется Celery.

## Что реализовано
- Асинхронный клиент к Deribit на aiohttp
- Получение цен для тикеров btc_usd и eth_usd
- Сохранение тикера, цены и времени в формате UNIX timestamp в PostgreSQL
- FastAPI API с тремя GET-методами:
  - получение всех сохранённых данных по валюте
  - получение последней цены
  - получение цены по дате
- Celery-задача, запускаемая каждую минуту
- Поддержка локального запуска и запуска через Docker Compose
- Unit-тесты для основных методов

## Архитектура проекта
- [src/client/deribit_client.py](src/client/deribit_client.py) — клиент Deribit
- [src/db/models.py](src/db/models.py) — модель записи цены
- [src/db/session.py](src/db/session.py) — асинхронные сессии и инициализация БД
- [src/services/price_service.py](src/services/price_service.py) — сервис доступа к данным
- [src/api/main.py](src/api/main.py) — FastAPI endpoints
- [src/tasks/fetch_prices.py](src/tasks/fetch_prices.py) — Celery task
- [src/tasks/celery_app.py](src/tasks/celery_app.py) — конфигурация Celery

## Требования
- Python 3.12+
- PostgreSQL
- Redis
- Docker и Docker Compose (по желанию)

## Локальный запуск
1. Создайте и активируйте виртуальное окружение.
2. Установите зависимости:
   - pip install -r requirements.txt
3. Создайте базу PostgreSQL и настройте переменные окружения в [.env](.env) или [.env.example](.env.example).
4. Запустите API:
   - uvicorn src.api.main:app --reload
5. Запустите Celery worker и beat:
   - celery -A src.tasks.celery_app.celery_app worker --loglevel=info
   - celery -A src.tasks.celery_app.celery_app beat --loglevel=info

Пример переменных окружения:
- DB_HOST=localhost
- DB_PORT=5432
- DB_NAME=deribit
- DB_USER=postgres
- DB_PASSWORD=postgres
- DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/deribit
- CELERY_BROKER_URL=redis://localhost:6379/0
- CELERY_RESULT_BACKEND=redis://localhost:6379/1

## Запуск через Docker Compose
Из корня проекта:
- docker compose up --build

После запуска:
- API будет доступно на http://localhost:8000
- PostgreSQL — на localhost:5432
- Redis — на localhost:6379

## API
Все методы GET и требуют обязательный query-параметр ticker.

- GET /prices?ticker=btc_usd — получить все сохранённые записи по валюте
- GET /prices/latest?ticker=btc_usd — получить последнюю цену валюты
- GET /prices/by-date?ticker=btc_usd&date=2026-07-30 — получить цены за указанную дату

## Design decisions
1. Асинхронная архитектура
   - HTTP-запросы к Deribit и работа с PostgreSQL реализованы асинхронно, чтобы приложение оставалось отзывчивым.
2. Чистая архитектура и разделение ответственности
   - Клиент, сервис, API и Celery-задача вынесены в отдельные модули для простоты поддержки и тестирования.
3. Конфигурация через окружение
   - Настройки базы данных и Redis задаются через переменные окружения, что делает приложение удобным для локального запуска и контейнеров.
4. Celery для фоновых задач
   - Периодическое получение данных вынесено в Celery, чтобы основной API не зависел от фоновой загрузки.

## Тестирование
Запуск тестов:
- pytest -q

