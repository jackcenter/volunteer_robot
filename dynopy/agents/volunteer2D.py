# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, cos, sin, atan2
from config import config
from dynopy.agents.robot2D import Robot2D
from dynopy.data_objects.state import State_2D
from dynopy.motion_planning.RIG_tree import RIG_tree
from dynopy.motion_planning.tree_analysis import update_information, identify_fusion_nodes, pick_path, prune_step,\
    plot_tree


class Volunteer2D(Robot2D):
    def __init__(self, name: str, color: str, state, detection_prob):
        super().__init__(name, color, state, detection_prob)

        self.V = []
        self.E = []
        self.B = None
        self.channel_list = {}      # name : path

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

    def fuse(self):
        pass

    def expand_tree(self):
        cfg = config.get_parameters()
        V, E = RIG_tree(cfg["step_size"], cfg["budget"], self.get_X_free(), self.get_X_free(),
                        self.get_pdf(), self.get_position(), cfg["radius"], cfg["t_limit"])

        return V, E

    def select_path(self, V, E):
        update_information(V, E, self.pdf)
        for agent, path in self.channel_list.items():
            identify_fusion_nodes(V, path, agent, 2)
        self.path = pick_path(V, E)

    def prune_passed_nodes(self, V, E):
        prune_step(V, E, self.path)

    def execute_planning_cycle(self):
        V, E = self.expand_tree()
        self.select_path(V, E)
        plot_tree(E, 'blue')
        V, E = prune_step(V, E, self.path)
        self.generate_trajectory()
        return V, E
