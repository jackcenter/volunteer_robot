# !/usr/bin/env python
# -*- coding: utf-8 -*-

class Node:
    def __init__(self, position, cost=0, information=0, time=0):
        """
        Data object that holds information for nodes used in motion planning.
        :param position: tuple with x and y locations
        :param cost: cost of node along path
        :param information: probability the target can be seen from the node position
        :param time: int for node time_step
        """
        self.pos = position
        self.c = cost
        self.i = information
        self.k = time

    def get_position(self):
        return self.pos

    def set_position(self, pos):
        self.pos = pos

    def get_cost(self):
        return self.c

    def set_cost(self, cost):
        self.c = cost

    def get_information(self):
        return self.i

    def set_information(self, i):
        self.i = i

    def get_time(self):
        return self.k

    def set_time(self, k):
        self.k = k

    @staticmethod
    def init_without_cost(position, information, time):
        return Node(position, information=information, time=time)
