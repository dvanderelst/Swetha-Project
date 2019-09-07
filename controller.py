# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 20:28:51 2019

@author: rmulu
"""
#import control
from matplotlib import pyplot

#controller = control.Controller(0.5, 0.1)

class Controller:
    def __init__(self, kp, kd):
        self.previous_error = None
        self.kp = kp
        self.kd = kd

    def get_output(self, error, dt):
        if self.previous_error is None: self.previous_error = error
        derivative = (error - self.previous_error) / dt
        output = self.kp * error + self.kd * derivative
        self.previous_error = error
        return output

    def reset(self):
        self.previous_error = None


if __name__ == "__main__":
    # Demonstrate the PD controller

    # Make a controller with parameters
    # you can play with these values and see what happens
    controller = Controller(0.1, 0.01)

    # Set some value for the error
    error = 10

    # Run the controller for a number of time steps
    error_trace = []
    output_trace = []
    for x in range(10):
        output = controller.get_output(error, 1)

        # Use the output of the controller to reduce the error
        error = error - output

        error_trace.append(error)
        output_trace.append(output)

    pyplot.subplot(1, 2, 1)
    pyplot.plot(error_trace)
    pyplot.xlabel('Step')
    pyplot.ylabel('Error')
    pyplot.subplot(1, 2, 2)
    pyplot.plot(output_trace)
    pyplot.xlabel('Step')
    pyplot.ylabel('Controller output')
    pyplot.show()