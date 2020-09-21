# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, cos, sin, atan2
from dynopy.agents.robot2D import Robot2D
from dynopy.data_objects.state import State_2D
from dynopy.motion_planning.RIG_tree import RIG_tree
from dynopy.motion_planning.tree_analysis import update_information, identify_fusion_nodes, pick_path_max_I, \
    pick_path_max_R, prune_step, plot_tree


class Volunteer2D(Robot2D):
    def __init__(self, name: str, state):
        super().__init__(name, state)

        self.V = []
        self.E = []
        self.V_closed = []
        self.B = None
        self.channel_list = {}      # name : path
        self.information_shared = {}

    def initialize_channels(self, agents):
        for agent in agents:
            if agent.get_name != self.name:
                self.channel_list.update({agent.get_name(): agent.get_path()})
                self.information_shared.update({agent.get_name(): 0.0})

    def get_tree(self):
        return self.V, self.E

    def step(self):
        """
        moves the agent in the commanded direction
        :param
        :return:
        """
        self.execute_planning_cycle()
        plot_tree(self.E, "lightcoral")
        root = self.path.pop()
        self.path_log.append(root)
        self.V = [x for x in self.V if x != root]
        self.E = [x for x in self.E if x[0] != root]

        action = self.trajectory.pop()
        x0, y0 = self.state.get_position()
        theta, r = action
        x1 = x0 + r*cos(theta)
        y1 = y0 + r*sin(theta)
        state = State_2D(x1, y1)

        self.state = state
        self.trajectory_log.append(action)
        self.update_information()

        if root.get_fusion():
            for channel in root.get_fusion():
                self.fuse(channel)

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

    def execute_planning_cycle(self):
        self.expand_tree()
        self.select_path()
        plot_tree(self.E, 'blue')
        self.prune_passed_nodes()
        self.generate_trajectory()

    def fuse(self, channel):
        pass

    def expand_tree(self):
        # TODO: handle this closed node business
        self.V, self.E, self.V_closed = RIG_tree(self.V, self.E, self.V_closed, self.get_X_free(), self.get_X_free(),
                                                 self.get_pdf(), self.get_position(), self.cfg)

    def select_path(self):
        for agent, path in self.channel_list.items():
            identify_fusion_nodes(self.V, path, agent, 1)
        update_information(self.V, self.E, self.pdf, self.cfg["gamma"], self.channel_list)
        # update_reward()

        # TODO: pick path based on reward function

        # self.path = pick_path_max_I(self.V, self.E)
        self.path = pick_path_max_R(self.V, self.E)

    def prune_passed_nodes(self):
        self.V, self.E = prune_step(self.V, self.E, self.path)
        # TODO: prune the closed list


