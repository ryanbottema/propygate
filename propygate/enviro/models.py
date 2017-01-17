
from django.conf import settings
from django.db import models

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO_IS_IN = {True: GPIO.IN, False: GPIO.OUT}
    GPIO_IS_LOW = {True: GPIO.LOW, False: GPIO.HIGH}
except:
    pass


class RaspPi(models.Model):

    model = models.CharField()

    notes = models.TextField(blank=True, null=True)


class RaspPiChannel(models.Model):

    rpi = models.ForeignKey(RaspPi)

    is_input = models.BooleanField(default=True)
    serial_num = models.IntegerField()
    input_string = models.CharField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_input(self):
        return self.input_string % self.serial_num

    def setup(self):
        GPIO.setup(self.serial_num, GPIO_IS_IN[self.is_input], initial=GPIO_IS_LOW[True])


class TempProbe(RaspPiChannel):

    def __init__(self, *args, **kwargs):
        kwargs['is_input'] = True
        super(TempProbe, self).__init__(*args, **kwargs)

    def get_temp(self):
        stream = open(self.get_input())
        reading = stream.read()
        stream.close()
        data = int(reading.split('t=')[1])
        temp = data / 1000.
        return temp


class RelayController(RaspPiChannel):

    is_on = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        kwargs['is_input'] = False
        super(RelayController, self).__init__(*args, **kwargs)


    def turn_on(self):
        if not self.on:
            GPIO.output(self.output_channel, GPIO.HIGH)
            self.on = True

    def turn_off(self):
        if self.on:
            GPIO.output(self.output_channel, GPIO.LOW)
            self.on = False

    def is_on(self):
        return self.on
