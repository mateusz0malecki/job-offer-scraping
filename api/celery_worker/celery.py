from celery import Celery
from celery.schedules import crontab

from settings import get_settings

app_settings = get_settings()

BROKER_URL = app_settings.celery_broker_url
BACKEND_URL = app_settings.celery_result_backend

app = Celery(
    'celery_worker',
    backend=BACKEND_URL,
    broker=BROKER_URL,
    include=['celery_worker.tasks']
)

app.conf.beat_schedule = {
    "setup_links_pracuj": {
        "task": "get_links_pracuj",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
    "setup_offers_pracuj": {
        "task": "get_offers_info_pracuj",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
    "setup_links_gowork": {
        "task": "get_links_gowork",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
    "setup_offers_gowork": {
        "task": "get_offers_info_gowork",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
}

if __name__ == '__main__':
    app.start()
