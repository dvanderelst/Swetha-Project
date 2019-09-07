import time
import numpy
import device
import util



class Board(device.BoardDevice):
    def __init__(self, ser_port=False, verbose=True):
        """
        Creates a Board object and connects to the physical board.
        :param ser_port: Boolean. If not False, the connection will use the provided port
        :param verbose: If True, some diagnistic messages are written to screen
        """
        self.servo1 = 0
        self.servo2 = 1
        self.led1 = 2
        self.led2 = 3
        self.pot = 4
        self.photo = 5

        self.photo_min = 30
        self.photo_max = 210

        self.pot_min = 0.25
        self.pot_max = 234

        self.min_servo = 544
        self.center_servo = 1410
        self.max_servo = 2400
        self.offset_servo = 0
        device.BoardDevice.__init__(self, ser_port, verbose)

    def test_connection(self):
        try:
            self.get_photo()
            self.get_pot()
            self.set_led1(True)
            self.set_led2(True)
            time.sleep(0.25)
            self.set_led1(False)
            self.set_led2(False)
            return True
        except:
            return False

    def get_photo(self):
        """ Gets the normalized level of the photocell.

        :return: float
            Level of the photocell in the range [0, 1].
        """
        photo = self.device.get_position(self.photo)
        photo = util.normalize(photo, self.photo_min, self.photo_max)
        return photo

    def get_pot(self):
        """Get the normalized level of the potentiometer.

        :return: float
            Level of the potentiometer in the range [0, 1].
        """
        pot = self.device.get_position(self.pot)
        pot = 1 - util.normalize(pot, self.pot_min, self.pot_max)
        return pot

    def set_servo(self, nr, target, raw):
        """
        Set servo with number nr to target position target.

        :param nr: ID of the servo
        :param target: Target position, in the range [0,1]
        :param raw: Boolean. If True, target position is supposed to be in steps
        """
        new = target
        if not raw:
            new = numpy.interp(target, [0, 0.5, 1], [self.min_servo, self.center_servo + self.offset_servo, self.max_servo])
            print(new)

        self.device.set_target(nr, int(new))

    def set_led(self, nr, value):
        if value: new = self.max_servo
        if not value: new = self.min_servo
        result = self.device.set_target(nr, new)
        return result

    def set_leds(self, l1, l2):
        """Shortcut to set both LEDs at the same time.

        :param l1: State of LED 1
        :type l1: Bool
        :param l2: State of LED 2
        :type l2: Bool
        :return: None
        """
        result1 = self.set_led1(l1)
        result2 = self.set_led2(l2)
        return result1, result2

    def set_servo1(self, position, raw=False):
        """ Set the position of servo 1.

        :param position: Normalized target position [0, 1] for the servo.
        :type position: Float
        :param raw: If true, position is given in steps.
        :type raw: Bool
        :return: None
        """
        self.set_servo(self.servo1, position, raw)

    def set_servo2(self, target, raw=False):
        """ Set the position of servo 2.
        """
        self.set_servo(self.servo2, target, raw)

    def set_led1(self, value):
        """Set state of LED 1.

        :param value: State of LED 1.
        :type value: Bool
        :return: None
        """
        result = self.set_led(self.led1, value)
        return result

    def set_led2(self, value):
        """Set state of LED 2."""
        result = self.set_led(self.led2, value)
        return result

    def stop_all(self):
        """Set all motors to a neutral position and switch of both LEDs.

        :return: None
        """
        self.set_servo1(0.5)
        self.set_servo2(0.5)
        self.set_led1(False)
        self.set_led2(False)

    def calibrate_channel(self, channel, n=10):
        mx = 0
        mn = 1000
        for x in range(0, n):
            time.sleep(1)
            print('.', end='')
            value = self.device.get_position(channel)
            if value > mx: mx = value
            if value < mn: mn = value
        print()
        return mn, mx

    def calibrate_photo(self):
        """ Function to calibrate the photocell. A number of measurements will be taken. The recorded minimum and 
        maximum values are used to normalize subsequent measurements.

        :return: Minimum and maximum value.
        """
        print('Calibrating photocell', end='')
        mn, mx = self.calibrate_channel(self.photo, 5)
        self.photo_min = mn
        self.photo_max = mx
        return mn, mx

    def calibrate_pot(self):
        """ Function to calibrate the potentiometer. A number of measurements will be taken. The recorded minimum and 
        maximum values are used to normalize subsequent measurements.

        :return: Minimum and maximum value.
        """
        print('Calibrating pot', end='')
        mn, mx = self.calibrate_channel(self.pot, 10)
        self.pot_min = mn
        self.pot_max = mx
        return mn, mx


if __name__ == "__main__":
    board = Board()
    for x in range(5):
        board.set_led1(True)
        time.sleep(0.25)
        board.set_led1(False)
        time.sleep(0.25)
