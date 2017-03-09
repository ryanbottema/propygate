from __future__ import absolute_import, unicode_literals
from propygate.celery import app

from django.utils import timezone

from . import models

from celery.utils.log import get_task_logger
logger = get_task_logger('celery.task')


@app.task
def check_enviro(enviro_id):
    
    try:
        enviro = models.Enviro.objects.get(pk=enviro_id)
    
        temp_probe = enviro.temp_probe
        heater = enviro.heater
        light = enviro.light
        ideals = enviro.temp_probe_change_current
        
        logger.info('Checking enviro' + str(enviro_id))
    
        temp = enviro.record_temp() if temp_probe else None
            
        if ideals and temp and heater:
            tl = ideals.temp_low
            tll = ideals.temp_low_low
            th = ideals.temp_high
            thh = ideals.temp_high_high
            
            if temp < tll:
                heater.turn_on()
            elif temp > tl:
                heater.turn_off()
                
        hour = timezone.now().hour
        
        if light:
            if hour > 5 and hour < 22:
                light.turn_on()
            else:
                light.turn_off()
        
    except Exception as e:
        logger.info('Error: ' + str(e))
