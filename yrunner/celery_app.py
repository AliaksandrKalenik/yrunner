from __future__ import absolute_import
import os
from celery import Celery

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yrunner.settings')

from django.conf import settings

app = Celery('yrunner')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_default_queue = 'default'
app.conf.task_routes = {

}
