from matplotlib import pyplot
from scipy.interpolate import interp1d
import sounddevice
import board
import controller
import audio
import numpy

# Top servo should be plugged into servo01
# Bottom servo should be plugged into servo02
# plug microphones into andrea sound card, use the mic symbol channel

devices = sounddevice.query_devices()

# Select Andrea SuperBeam
sounddevice.default.device = 8

b = board.Board(verbose=True)

# Set the bottom servo such that the ears are upright
b.set_servo1(0.9)

# Set the to servo such that the ears are centered
b.set_servo2(0.5)

# Set up interpolation, from angles to servo position
servo_position = interp1d([-90, 0, 95], [0, 0.5, 1], fill_value= (0, 1), bounds_error=False)

c = controller.Controller(1,0)

current_angle = 0

measurements =[]
print('Please be quiet for the calibration')
print('calibration:', end='')
for x in range(50):
    print('.', end='')
    iid, db, direction = audio.handle_audio()
    measurements.append(iid)
measurements = numpy.array(measurements)
bias = numpy.mean(measurements)
print('Done')
hist = pyplot.hist(measurements)
pyplot.vlines(bias, 0, numpy.max(hist[0]),'red', linewidth=3)
pyplot.show()
#%%
for x in range(500):
    iid, db, direction = audio.handle_audio()
    corrected_iid = iid - bias
    #if abs(corrected_iid) < 1: corrected_iid = 0
    output = c.get_output(corrected_iid, 0.1)
    current_angle = current_angle - output
    if current_angle < -85: current_angle = -85
    if current_angle > +85: current_angle = +85
    msg = '%+.2f   %+.2f   %.2f   %s' % (iid, current_angle, -output, direction)
    print(msg)
    new_servo_position = servo_position(current_angle)
    b.set_servo2(new_servo_position)