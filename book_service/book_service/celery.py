import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_service.settings")
app = Celery("book_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
