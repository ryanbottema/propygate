# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propygate.settings.local')
# app = Celery('propygate', broker='redis://127.0.0.1:6379', include=['propygate.propygate_core.tasks'])
#
# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propygate.settings.local')


## Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('propygate', include=['propygate.propygate_core.tasks'])

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


from celery.schedules import crontab
app.conf.beat_schedule = {
    'check_enviros_every_5min': {
        'task': 'check_enviro',
        'schedule': 5 * 60,   # in seconds
        'args': (1,),   # assume enviro id of 1
    },
    # 'add-every-5-seconds': {
    #     'task': 'multiply_two_numbers',
    #     'schedule': 5.0,
    #     'args': (16, 16)
    # },
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
}
