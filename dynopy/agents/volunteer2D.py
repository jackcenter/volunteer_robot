# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, cos, sin, atan2
from dynopy.agents.robot2D import Robot2D
from dynopy.data_objects.state import State_2D


class Volunteer2D(Robot2D):
    def step(self):
        """
        moves the agent in the commanded direction
        :param
        :return:
        """
        action = self.trajectory.pop()

        x0, y0 = self.state.get_position()
        theta, r = action
        x1 = x0 + r*cos(theta)
        y1 = y0 + r*sin(theta)
        state = State_2D(x1, y1)

        self.state = state
        self.trajectory_log.append(action)
        self.update_information()
        self.path_log.append(self.path.pop())

    def generate_trajectory(self):
        traj = []
        path = self.path.copy()
        w_1 = self.path_log[-1]

        while path:
            w_0 = w_1
            w_1 = path.pop()
            traj.append(self.get_direction_and_distance(w_0.get_position(), w_1.get_position()))

        traj.reverse()
        self.trajectory = traj

    @staticmethod
    def get_direction_and_distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        direction = atan2(y2-y1, x2-x1)
        return direction, distance
