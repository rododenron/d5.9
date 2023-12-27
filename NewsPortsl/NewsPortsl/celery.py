import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortsl.settings')

app = Celery('NewsPortsl')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_message_news_for_last_week': {
        'task': 'News.tasks.send_message_news',
        'schedule': crontab(hour='8', day_of_week='1'),
    },
}

app.autodiscover_tasks()