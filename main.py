from scipy.interpolate import interp1d
import board
import time

#sd.default.device = "Andrea SuperBeam US"
#sd.default.device = 1
#print(sd.query_devices())


b = board.Board(verbose=True)

# Set the bottom servo such that the ears are upright
b.set_servo1(0.9)

# Set the to servo such that the ears are centered
b.set_servo2(0.5)

# Set up interpolation, from angles to servo position

servo_position = interp1d([-90, 0, 95], [0, 0.5, 1], fill_value= (0, 1), bounds_error=False)

# Test servo
angles = [-80, -60, -45, 0, 45, 60 , 80]
for angle in angles:
    position = servo_position(angle)
    b.set_servo2(position)
    print(angle, 'degrees')
    time.sleep(3)

