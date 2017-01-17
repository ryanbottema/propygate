import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

relay_control_channels = [11, 12, 13, 15]
temp_channel = 4
fan_control_channels = []
num_tracked_temps = 10

loop_time = 60 * 2  # 2 minutes


class TempProbe(object):

    # input_channel = temp_channel

    def __init__(self, sn):

        self.input = '/sys/bus/w1/devices/' + sn + '/w1_slave'
        # GPIO.setup(TempProbe.input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_temp(self):

        stream = open(self.input)
        reading = stream.read()
        stream.close()
        data = int(reading.split('t=')[1])
        temp = data / 1000.

        return temp


class Fan(object):

    def __init__(self, c):

        self.on = False
        self.controller = c

    def turn_on(self):
        if not self.on:
            # do turbn on
            self.on = True

    def turn_off(self):
        if self.on:
            # do turn off
            self.on = False


class RelayController(object):

    output_channel = None
    on = False

    def __init__(self, oc):

        self.output_channel = oc
        GPIO.setup(oc, GPIO.OUT, initial=GPIO.LOW)

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


class SeedBox(object):

    temp_ideal = None

    temp_low_low = None
    temp_low = None
    temp_high = None
    temp_high_high = None
    temp_probe = None
    fan = None
    relay_controller = None

    last_num_temps = []

    def __init__(self, ti, tp, f, rc):
        self.temp_ideal = ti
        self.temp_low_low = ti - 3
        self.temp_low = ti - 1
        self.temp_high = ti + 1
        self.temp_high_high = ti + 3
        self.temp_probe = tp
        self.fan = f
        self.relay_controller = rc

    def change_temps(self, c):
        self.temp_low_low += c
        self.temp_low += c
        self.temp_high += c
        self.temp_high_high += c

    def calc_ideals(self):

        av_temp = sum(self.last_num_temps)/len(self.last_num_temps)
        if av_temp > self.temp_ideal + 3:
            self.change_temps(-1)
        elif av_temp > self.temp_ideal + 1:
            self.change_temps(-0.5)
        elif av_temp < self.temp_ideal - 3:
            self.change_temps(1)
        elif av_temp < self.temp_ideal - 1:
            self.change_temps(0.5)
        else:
            print 'Great temp control'

    def heat_control(self):

        curr_temp = self.temp_probe.get_temp()
        if len(self.last_num_temps) < num_tracked_temps:
            self.last_num_temps.append(curr_temp)
        else:
            self.last_num_temps.pop(0)
            self.last_num_temps.append(curr_temp)

        self.calc_ideals()

        if curr_temp < self.temp_low_low:
            self.relay_controller.turn_on()
            self.fan.turn_off()
        elif curr_temp < self.temp_low:
            self.fan.turn_off()
        elif curr_temp < self.temp_high:
            self.relay_controller.turn_off()
        else:
            self.relay_controller.turn_off()
            self.fan.turn_on()


class SeedBoxes(object):

    boxes = []
    record_file_name = None

    def __init__(self):
        self.record_file_name = rfn
        # TODO write file header

    def add_box(self, b):
        self.boxes.append(b)

    def go_control(self):
        for b in self.boxes:
            b.heat_control()

    def record(self):
        for b in self.boxes:
            file = open(self.record_file_name + date, 'a')
            # TODO write line: open file and close again
            # self.record_file.write()
            file.close()


def runner():

    seed_boxes = SeedBoxes('seed_records.txt')
    seed_boxes.add_box(SeedBox(30, TempProbe('TempProbe1'), Fan('FanContoller1'), RelayController(11)))
    seed_boxes.add_box(SeedBox(30, TempProbe('TempProbe2'), Fan('FanContoller2'), RelayController(12)))
    seed_boxes.add_box(SeedBox(30, TempProbe('TempProbe3'), Fan('FanContoller3'), RelayController(13)))

    run = 'Patrick Watson'
    while run == 'Patrick Watson':

        seed_boxes.go_control()
        seed_boxes.record()

        # TODO wait timer here loop_time
