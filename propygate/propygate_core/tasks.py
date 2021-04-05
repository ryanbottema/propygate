from __future__ import absolute_import, unicode_literals

from celery.app import shared_task
from propygate_core.celery import app

from django.conf import settings
from django.utils import timezone

from . import models

from celery.utils.log import get_task_logger

logger = get_task_logger('celery.task')


def _print(what):
    print_file = open(settings.PRINT_LOG_FILE, 'a')
    print_file.write('\n%s' % what)
    print_file.close()


@app.task
def check_enviro(enviro_id):
    try:
        enviro = models.Enviro.objects.get(pk=enviro_id)

        temp_probe = enviro.temp_probe
        heater = enviro.heater
        light = enviro.light
        ideals = enviro.get_current_ideals()
        fan = enviro.fan

        temp = enviro.record_temp() if temp_probe else None
        _print('temp: ' + str(temp))

        if ideals and temp and heater:
            tl = ideals.temp_low
            tll = ideals.temp_low_low
            th = ideals.temp_high
            thh = ideals.temp_high_high

            if temp < tll:
                heater.turn_on()
            elif temp > tl:
                heater.turn_off()

        if ideals and temp and fan:
           tl = ideals.temp_low
           tll = ideals.temp_low_low
           th = ideals.temp_high
           thh = ideals.temp_high_high

           if temp > thh:
               fan.turn_on()
           elif temp < th:
               fan.turn_off()

        hour = timezone.localtime(timezone.now()).hour

        if light:
            if hour in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
                light.turn_on()
            else:
                light.turn_off()

    except Exception as e:
        logger.info('Error: ' + str(e))
        _print('Error: ' + str(e))


@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y