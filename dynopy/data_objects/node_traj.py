# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Node:
    def __init__(self, state, u, cost=0, information=0.0, time=0, reward=0.0, fusion={}):
        """
        Data object that holds information for nodes used in motion planning.
        :param state: state object
        :param u: input object resulting in this node
        :param cost: cost of node along path
        :param information: probability the target can be seen from the node position
        :param time: int for node time_step
        :param reward: the reward available in the selected node
        :param fusion:
        """
        self.x = state
        self.u = u
        self.c = cost
        self.i = information
        self.k = time
        self.r = reward
        self.f = fusion
        self.g = False

    def get_x_position(self):
        return self.x.get_x_position()

    def get_y_position(self):
        return self.x.get_y_position()

    def get_position(self):
        return self.x.get_position()

    def set_position(self, pos):
        self.x.set_position(pos)

    def get_pretty_position(self, digits=2):
        pretty_pos = []
        for item in self.get_position():
            pretty_pos.append(round(item, digits))

        return tuple(pretty_pos)

    def get_state(self):
        return self.x

    def get_cost(self):
        return self.c

    def set_cost(self, c):
        self.c = c

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

    def set_reward(self, r):
        self.r = r

    def get_fusion(self):
        return self.f

    def set_fusion(self, f):
        self.f = f

    def get_goal_status(self):
        return self.g

    def set_goal_status(self, g):
        self.g = g

    def check_fused(self, channel):
        if channel in self.f:
            return True

    def compare_time(self, node):
        """

        :param node: node to compare time to
        :return: boolean indicating whether the two times are the same
        """
        if self.k == node.get_time():
            return True
        else:
            return False

    def copy(self):
        return Node(self.x, self.u, self.c, self.i, self.k, self.r, self.f)
