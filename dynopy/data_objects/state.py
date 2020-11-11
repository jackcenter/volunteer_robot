# !/usr/bin/env python
# -*- coding: utf-8 -*-


class State_2D:
    def __init__(self, x_pos, y_pos, info=0, time=0):
        self.x1 = x_pos
        self.x2 = y_pos
        self.x3 = info
        self.k = time
        self.state_names = {"x1": "x position", "x2": "y position", "x3": "information"}

    def get_position(self):
        return self.x1, self.x2

    def set_position(self, x, y):
        self.x1 = x
        self.x2 = y

    def get_x_position(self):
        return self.x1

    def set_x_position(self, x):
        self.x1 = x

    def get_y_position(self):
        return self.x2

    def set_y_position(self, y):
        self.x2 = y

    def get_information(self):
        return self.x3

    def set_information(self, I):
        self.x3 = I

    def get_time(self):
        return self.k

    def set_time(self, time):
        self.k = time

    def copy(self):
        return State_2D(self.x1, self.x2, self.x3)

    @staticmethod
    def create_from_tuple(pos, info=0, time=0):
        return State_2D(pos[0], pos[1], info, time)
