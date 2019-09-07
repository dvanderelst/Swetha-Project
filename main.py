from scipy.interpolate import interp1d
import sounddevice
import board
import controller
import audio
import numpy

devices = sounddevice.query_devices()
sounddevice.default.device = 6

b = board.Board(verbose=True)

# Set the bottom servo such that the ears are upright
b.set_servo1(0.9)

# Set the to servo such that the ears are centered
b.set_servo2(0.5)

# Set up interpolation, from angles to servo position
servo_position = interp1d([-90, 0, 95], [0, 0.5, 1], fill_value= (0, 1), bounds_error=False)

c = controller.Controller(1,0)

# Test servo
#angles = [-80, -60, -45, 0, 45, 60 , 80]
#for angle in angles:
#    position = servo_position(angle)
#    b.set_servo2(position)
#    print(angle, 'degrees')
#    time.sleep(3)
current_angle = 0

measurements =[]
for x in range(50):
    iid, db, direction = audio.handle_audio()
    measurements.append(iid)
    a = numpy.array(measurements)
    bias = numpy.median(a)

for x in range(500):
    iid, db, direction = audio.handle_audio()
    corrected_iid = iid - bias
    if abs(corrected_iid) < 1: corrected_iid = 0
    output = c.get_output(corrected_iid, 0.1)
    print(iid, direction, output)
    current_angle = current_angle - output
    if current_angle < -80: current_angle = -85
    if current_angle > +80: current_angle = +85
    print(current_angle)

    new_servo_position = servo_position(current_angle)
    b.set_servo2(new_servo_position)
    print('------------------------------------------------')