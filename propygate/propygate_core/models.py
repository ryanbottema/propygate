import subprocess

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.utils import timezone

#try:
import RPi.GPIO as GPIO
from RPi.GPIO import output, setup, input

GPIO.setmode(GPIO.BOARD)
GPIO_IS_IN = {True: GPIO.IN, False: GPIO.OUT}
GPIO_IS_HIGH = {True: GPIO.HIGH, False: GPIO.LOW}
IS_ERROR = False
#except Exception as e:
#    GPIO_IS_IN = {True: 'INPUT!', False: 'OUTPUT!'}
#    GPIO_IS_HIGH = {True: 'HIGH!', False: 'LOW!'}
#
#    def output(num, high_low):
#        print 'Beep Boop: Turning GPIO %s %s' % (num, high_low)
#
#    def setup(num, is_input, initial=None):
#        print 'Beep Boop: Setting up GPIO channel %s as %s with initial %s.' % (num, is_input, initial)
#
#    IS_ERROR = e


def _print(what):
    print_file = open('/home/propygate/logs/print.log', 'a')
    print_file.write('\n%s' % what)
    print_file.close()
    

def _output(chan_num, high_low):
    try:
        output(chan_num, high_low)
    except RuntimeError:
        setup(chan_num, False, initial=GPIO_IS_HIGH[False])
        output(chan_num, high_low)


def _output_status(chan_num):
    try:
        state = input(chan_num)
    except RuntimeError:
        setup(chan_num, False, initial=GPIO_IS_HIGH[False])
        state = input(chan_num)
    return state
        

class RaspPi(models.Model):
    model = models.CharField(max_length=128)

    notes = models.TextField(blank=True, null=True)


class RaspPiChannel(models.Model):
    rpi = models.ForeignKey(RaspPi, on_delete=models.CASCADE)

    is_low = models.BooleanField(default=True)
    is_input = models.BooleanField(default=True)
    channel_num = models.IntegerField()
    input_string = models.CharField(blank=True, null=True, max_length=256)
    notes = models.TextField(blank=True, null=True)

    def setup(self):
        setup(self.channel_num, GPIO_IS_IN[bool(self.is_input)], initial=GPIO_IS_HIGH[False])

    def toggle_high_low(self):
        if not bool(self.is_input):
            if _output_status(self.channel_num) == 0:
                turn = GPIO.HIGH
            else:
                turn = GPIO.LOW
            self.is_low = not self.is_low
            
            self.save()
            _output(self.channel_num, turn)

    def turn_low(self):
        if not bool(self.is_input):
            if _output_status(self.channel_num) == 1:
                self.is_low = False
                self.save()
                _output(self.channel_num, GPIO.LOW)

    def turn_high(self):
        if not bool(self.is_input):
            if _output_status(self.channel_num) == 0:
                self.is_low = True
                self.save()
                _output(self.channel_num, GPIO.HIGH)

    def __unicode__(self):
        return 'IO Channel %s %s' % (self.channel_num, '(input)' if self.is_input else '(output)')


class TempProbe(models.Model):
    channel = models.ForeignKey(RaspPiChannel, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    serial_num = models.CharField(max_length=16)
    
    def get_temp(self):
        stream = open('/sys/bus/w1/devices/28-%s/w1_slave' % self.serial_num)
        reading = stream.read()
        stream.close()
        data = int(reading.split('t=')[1])
        temp = data / 1000.
        return temp

    def __unicode__(self):
        return 'TempProbe %s' % self.serial_num

    def get_input(self):
        return self.channel.input_string % self.serial_num


class RelayController(models.Model):
    channel = models.ForeignKey(RaspPiChannel, unique=True, on_delete=models.CASCADE)
    plug = models.CharField(unique=True, max_length=32)

    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return 'Relay on channel %s' % self.channel.channel_num

    def toggle_on_off(self):
        self.channel.toggle_high_low()
        RelayControllerToggle.objects.create(relay_controller=self, is_on=not self.channel.is_low)
        
    def turn_on(self):
        #if self.channel.is_low:
        self.channel.turn_high()
        RelayControllerToggle.objects.create(relay_controller=self, is_on=True)
            
    def turn_off(self):
        #if not self.channel.is_low:
        self.channel.turn_low()
        RelayControllerToggle.objects.create(relay_controller=self, is_on=False)


class Enviro(models.Model):
    light = models.ForeignKey(RelayController, blank=True, null=True, related_name='enviro_light', on_delete=models.SET_NULL)
    heater = models.ForeignKey(RelayController, blank=True, null=True, related_name='enviro_heater', on_delete=models.SET_NULL)
    temp_probe = models.ForeignKey(TempProbe, blank=True, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=32)
    notes = models.TextField(blank=True, null=True)

    def record_temp(self):
        if self.temp_probe:
            temp = TempRecord(enviro=self, temperature=self.temp_probe.get_temp())
            temp.save()
            return temp

    def get_current_temp(self):
        return TempRecord.objects.filter(enviro=self).latest()

    def get_current_ideals(self):
        return Ideals.objects.filter(enviro=self).latest()

    def __unicode__(self):
        return 'Enviro %s' % self.name


class TempRecord(models.Model):
    enviro = models.ForeignKey(Enviro, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    datetime_recorded = models.DateTimeField()

    class Meta:
        get_latest_by = 'datetime_recorded'

    def save(self, *args, **kwargs):
        self.datetime_recorded = timezone.now()
        return super(TempRecord, self).save(*args, **kwargs)


class RelayControllerToggle(models.Model):

    relay_controller = models.ForeignKey(RelayController, on_delete=models.CASCADE)
    datetime_toggled = models.DateTimeField()
    is_on = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'datetime_toggled'
        ordering = ['datetime_toggled']

    def save(self, *args, **kwargs):
        self.datetime_toggled = timezone.now()
        return super(RelayControllerToggle, self).save(*args, **kwargs)


class Ideals(models.Model):
    datetime_changed = models.DateTimeField(blank=True, null=True)
    enviro = models.ForeignKey(Enviro, on_delete=models.CASCADE)

    temp_ideal = models.DecimalField(max_digits=3, decimal_places=1)
    temp_low_low = models.DecimalField(max_digits=3, decimal_places=1)
    temp_low = models.DecimalField(max_digits=3, decimal_places=1)
    temp_high = models.DecimalField(max_digits=3, decimal_places=1)
    temp_high_high = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        ordering = ['datetime_changed']
        get_latest_by = 'datetime_changed'
        verbose_name_plural = 'Ideals'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            tpc = Ideals(
                datetime_changed=timezone.now(),
                enviro=self.enviro,
                temp_ideal=self.temp_ideal,
                temp_low_low=self.temp_low_low,
                temp_low=self.temp_low,
                temp_high=self.temp_high,
                temp_high_high=self.temp_high_high
            )
            tpc.save(force_insert=True)
        else:
            super(Ideals, self).save(*args, **kwargs)


