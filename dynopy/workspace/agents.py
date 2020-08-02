from math import pi, cos, sin
import matplotlib.pyplot as plt
import numpy as np


class Robot:
    def __init__(self, name: str, color: str, state: list, volunteer=False):
        """

        :param name:
        :param color:
        :param state: [x position, y_position, orientation]
        """
        self.name = name
        self.color = color
        self.state = state
        self.volunteer = volunteer

    def plot(self):
        x = self.state[0] + 0.5
        y = self.state[1] + 0.5
        plt.plot(x, y, 'x', color=self.color)

    def get_volunteer_status(self):
        return self.volunteer

    def step(self, action):
        """
        moves the agent in the commanded direction
        :param action: string: left, right, forward, or backward
        :return:
        """

        if action == 'left':
            turn = pi/2
        elif action == 'right':
            turn = -pi/2
        elif action == 'forward':
            turn = 0
        elif action == 'backward':
            turn = pi
        else:
            print("ERROR: robot action not understood. Needs to be left, right, forward, or backward")
            turn = 0

        x3_new = (self.state[2] + turn) % (2*pi)
        x1_new = cos(x3_new)
        x2_new = sin(x3_new)

        self.state[2] = x3_new
        self.state[0] += x1_new
        self.state[1] += x2_new
