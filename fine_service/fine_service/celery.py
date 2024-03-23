import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fine_service.settings")
app = Celery("fine_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
