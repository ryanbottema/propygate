from django.conf import settings
from django.db import models
from django.utils import timezone

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BOARD)
    GPIO_IS_IN = {True: GPIO.IN, False: GPIO.OUT}
    GPIO_IS_HIGH = {True: GPIO.HIGH, False: GPIO.LOW}
except:
    pass


class RaspPi(models.Model):
    model = models.CharField(max_length=128)

    notes = models.TextField(blank=True, null=True)


class RaspPiChannel(models.Model):
    rpi = models.ForeignKey(RaspPi)

    is_input = models.BooleanField(default=True)
    is_low = False
    serial_num = models.IntegerField()
    input_string = models.CharField(max_length=256)
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

    def __unicode__(self):
        return 'IO Channel %s %s' % (self.serial_num, '(input)' if self.is_input else '(output)')


class TempProbe(models.Model):
    channel = models.ForeignKey(RaspPiChannel)
    notes = models.TextField(blank=True, null=True)
    serial_num = models.CharField(max_length=16)

    def get_temp(self):
        stream = open(self.channel.get_input())
        reading = stream.read()
        stream.close()
        data = int(reading.split('t=')[1])
        temp = data / 1000.
        return temp

    def __unicode__(self):
        return 'TempProbe on %s' % self.channel.serial_num


class RelayController(models.Model):
    channel = models.ForeignKey(RaspPiChannel, unique=True)
    plug = models.IntegerField(unique=True)

    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return 'Relay on channel %s' % self.channel.serial_num

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
    light = models.ForeignKey(RelayController, blank=True, null=True, related_name='enviro_light')
    heater = models.ForeignKey(RelayController, blank=True, null=True, related_name='enviro_heater')
    temp_probe = models.ForeignKey(TempProbe, blank=True, null=True)
    temp_probe_change_current = models.ForeignKey(
        'enviro.TempProbeChange', blank=True, null=True, related_name='enviro_temp_probe_current'
    )

    name = models.CharField(max_length=32)
    notes = models.TextField(blank=True, null=True)

    def get_current_temp(self):
        return TempRecord.objects.filter(enviro=self).latest()

    def __unicode__(self):
        return 'Enviro %s' % self.name


class TempRecord(models.Model):
    enviro = models.ForeignKey(Enviro)
    temperature = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        get_latest_by = 'id'


class TempProbeChange(models.Model):
    datetime_changed = models.DateTimeField()
    enviro = models.ForeignKey(Enviro)

    measurement_frequency = models.PositiveSmallIntegerField()
    temp_ideal = models.DecimalField(max_digits=3, decimal_places=1)
    temp_low_low = models.DecimalField(max_digits=3, decimal_places=1)
    temp_low = models.DecimalField(max_digits=3, decimal_places=1)
    temp_high = models.DecimalField(max_digits=3, decimal_places=1)
    temp_high_high = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        ordering = ['datetime_changed'] 

    def save(self, *args, **kwargs):
        if self.pk is not None:
            tpc = TempProbeChange(
                datetime_changed=timezone.now(),
                enviro=self.enviro,
                measurement_frequency=self.measurement_frequency,
                temp_ideal=self.temp_ideal,
                temp_low_low=self.temp_low_low,
                temp_low=self.temp_low,
                temp_high=self.temp_high,
                temp_high_high=self.temp_high_high
            )
            tpc.save(force_insert=True)
            self.enviro.temp_probe_change_current = self
            self.enviro.save()
        else:
            super(TempProbeChange, self).save(*args, **kwargs)
