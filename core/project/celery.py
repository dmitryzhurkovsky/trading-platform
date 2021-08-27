import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'find-best-offers-every-minute': {
        'task': 'trading.tasks.find_best_offers_and_make_deal',
        'schedule': crontab(),
    },
}