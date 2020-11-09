# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt


class Node:
    def __init__(self, position, cost=0, information=0.0, time=0, reward=0.0):
        """
        Data object that holds information for nodes used in motion planning.
        :param position: tuple with x and y locations
        :param cost: cost of node along path
        :param information: probability the target can be seen from the node position
        :param time: int for node time_step
        :param reward: the reward available in the selected node
        """
        self.pos = position
        self.c = cost
        self.i = information
        self.k = time
        self.r = reward
        self.f = []             # channels to fuse over

    def get_position(self):
        return self.pos

    def get_pretty_position(self, digits=2):
        pretty_pos = []
        for item in self.pos:
            pretty_pos.append(round(item, digits))

        return tuple(pretty_pos)

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

    def get_reward(self):
        return self.r

    def set_reward(self, reward):
        self.r = reward

    def get_fusion(self):
        return self.f

    def add_fusion(self, channel):
        self.f.append(channel)

    def check_fused(self, channel):
        if channel in self.f:
            return True

    @staticmethod
    def init_without_cost(position, information, time):
        return Node(position, information=information, time=time)

    def get_distance_from(self, node):
        """

        :param node: node to check distance between
        :return: euclidean distance apart
        """
        x1, y1 = self.get_position()
        x2, y2 = node.get_position()
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def compare_time(self, node):
        """

        :param node: node to compare time to
        :return: boolean indicating whether the two times are the same
        """
        if self.k == node.get_time():
            return True
        else:
            return False
