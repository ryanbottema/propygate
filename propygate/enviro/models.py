
from django.conf import settings
from django.db import models

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO_IS_IN = {True: GPIO.IN, False: GPIO.OUT}
    GPIO_IS_HIGH = {True: GPIO.HIGH, False: GPIO.LOW}
except:
    pass


class RaspPi(models.Model):

    model = models.CharField()

    notes = models.TextField(blank=True, null=True)


class RaspPiChannel(models.Model):

    rpi = models.ForeignKey(RaspPi)

    is_input = models.BooleanField(default=True)
    is_low = False
    serial_num = models.IntegerField()
    input_string = models.CharField()
    notes = models.TextField(blank=True, null=True)

    def get_input(self):
        return self.input_string % self.serial_num

    def setup(self):
        GPIO.setup(self.serial_num, GPIO_IS_IN[bool(self.is_input)], initial=GPIO_IS_HIGH[False])

    def toggle_high_low(self):
        if bool(self.is_input):
            self.is_low = not self.is_low
            GPIO.output(self.serial_num, GPIO_IS_HIGH[self.is_low])

    def turn_low(self):
        if bool(self.is_input):
            self.is_low = False
            GPIO.output((self.serial_num, GPIO_IS_HIGH[self.is_low]))

    def turn_high(self):
        if bool(self.is_input):
            self.is_low = True
            GPIO.output((self.serial_num, GPIO_IS_HIGH[self.is_low]))


class TempProbe(models.Model):

    channel = models.ForeignKey(RaspPiChannel)
    notes = models.TextField(blank=True, null=True)

    def get_temp(self):
        stream = open(self.channel.get_input())
        reading = stream.read()
        stream.close()
        data = int(reading.split('t=')[1])
        temp = data / 1000.
        return temp


class RelayController(models.Model):

    channel = models.ForeignKey(RaspPiChannel, unique=True)
    plug = models.IntegerField(unique=True)

    notes = models.TextField(blank=True, null=True)

#
# class Light(models.Model):
#
#     relay_controller = models.ForeignKey(RelayController)
#
#     notes = models.TextField(blank=True, null=True)
#
#
# class Heater(models.Model):
#
#     relay_controller = models.ForeignKey(RelayController)
#
#     notes = models.TextField(blank=True, null=True)


class Enviro(models.Model):

    light = models.ForeignKey(RelayController, blank=True, null=True)
    heater = models.ForeignKey(RelayController, blank=True, null=True)
    temp_probe = models.ForeignKey(TempProbe, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)


class TempRecord(models.Model):

    enviro = models.ForeignKey(Enviro)
    temperature = models.DecimalField(max_digits=3, decimal_places=1)


class TempProbeChange(models.Model):

    datetime_changed = models.DateTimeField()
    enviro = models.ForeignKey(Enviro)

    measurement_frequency = models.PositiveSmallIntegerField()
    temp_ideal = models.DecimalField()
    temp_low_low = models.DecimalField()
    temp_low = models.DecimalField()
    temp_high = models.DecimalField()
    temp_high_high = models.DecimalField()



