from celery import Celery

from src.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "deribit_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "src.tasks.fetch_prices.fetch_and_store_prices",
        "schedule": 60.0,
        "args": (),
    }
}
