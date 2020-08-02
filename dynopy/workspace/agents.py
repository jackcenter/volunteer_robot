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

        self.waypoints = []
        self.path = []
        self.trajectory = []

    def plot(self):
        x = self.state[0] + 0.5
        y = self.state[1] + 0.5
        plt.plot(x, y, 'x', color=self.color)

    def get_volunteer_status(self):
        return self.volunteer

    def generate_path(self, w_0):
        """
        Could use any type of path planner here. This is just a straight line style implementation
        Assume waypoint 1 is the starting location
        :return:
        """
        start = self.waypoints[w_0]
        goal = self.waypoints[w_0 + 1]
        path = [start]

        # --- Straight line assumption ---
        x = start[0]
        y = start[1]
        goal_found = False

        # North
        if start[1] < goal[1]:
            while not goal_found:
                y += 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # East
        elif start[0] < goal[0]:
            while not goal_found:
                x += 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # South
        elif start[1] > goal[1]:
            while not goal_found:
                y -= 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # West
        elif start[0] > goal[0]:
            while not goal_found:
                x -= 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # Error
        else:
            print("ERROR: Something's wrong with the start or goal position for {}".format(self.name))

        return path


    def generate_trajectory(self):
        pass

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
