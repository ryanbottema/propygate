from __future__ import absolute_import, unicode_literals
from propygate.celery import app

from . import models

from celery.utils.log import get_task_logger
logger = get_task_logger('celery.task')


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def check_enviro(enviro_id):
    
    try:
        enviro = models.Enviro.objects.get(pk=enviro_id)
    
        temp_probe = enviro.temp_probe
        heater = enviro.heater
        light = enviro.light
        ideals = enviro.temp_probe_change_current
    
        if temp_probe and ideals:
            pass
        print 'Checking enviro' + str(enviro_id)
        logger.info('Checking enviro' + str(enviro_id))

        models.TempRecord.objects.create(enviro=enviro, temperature=28)
    except Exception as e:
        logger.info('Error: ' + str(e))
