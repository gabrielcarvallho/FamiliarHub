import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'familiar_hub.settings')

app = Celery('familiar_hub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()