import os

from celery import Celery
from django.apps import AppConfig
from django.conf import settings


if not settings.configured:
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'settings.development'
    )


app = Celery('pbb')


class CeleryConfig(AppConfig):
    name = 'taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
