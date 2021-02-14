# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Input_2D:
    def __init__(self, direction, distance):
        self.u1 = direction
        self.u2 = distance
        self.state_names = {"u1": "direction", "u2": "distance"}

    def get_direction(self):
        return self.u1

    def get_distance(self):
        return self.u2
