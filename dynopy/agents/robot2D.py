# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import trunc
import matplotlib.pyplot as plt
import numpy as np
from config.config import load_agent_parameters
from dynopy.data_objects.node import Node
from dynopy.data_objects.state import State_2D


class Robot2D:
    def __init__(self, name: str, state):
        """

        :param name:
        :param color:
        :param state: [x position, y_position]
        """
        self.name = name
        self.state = state
        # self.pD = detection_prob    # probability of detection
        # self._pD = 1 - self.pD      # probability of no detection
        self.cfg = load_agent_parameters(name)

        self.pdf = None  # current probability distribution
        self.workspace = None       # current workspace
        self.c_space = None

        self.waypoints = []         # list of points the agent needs to reach
        self.path = []              # list of 2D positions
        self.trajectory = []        # last element, [-1], is the next action to take
        self.path_log = []
        self.trajectory_log = []    # stores actions taken in order, ie [0] is the first action
        self.state_log = []
        self.i_gained = 0

    def plot(self):
        x, y = self.get_position()
        plt.plot(x, y, 'x', color=self.cfg["color"])

    def plot_visited_cells(self):
        for node in self.path_log:
            x, y = node.get_position()
            plt.plot(x, y, 'o', color=self.cfg["color"], mfc='none')

    def plot_path(self):
        for node in self.path:
            x, y = node.get_position()
            plt.plot(x, y, '.', color=self.cfg["color"])

    def plot_pdf(self):
        rows, cols = self.pdf.shape
        for x in range(0, cols):
            for y in range(0, rows):
                size = self.pdf[y][x]*300
                plt.plot(x + 0.5, y + 0.5, color='white', marker='o', markersize=size)

    def get_name(self):
        return self.name

    def set_state(self, state):
        self.state = state

    def get_position(self):
        return self.state.get_position()

    def get_path(self):
        return self.path

    def set_workspace(self, ws):
        self.workspace = ws

    def initialize_pdf(self):
        self.pdf = self.workspace.pdf.copy()

    def get_pdf(self):
        return self.pdf

    def set_pdf(self, pdf):
        self.pdf = pdf

    def set_c_space(self):
        c1 = self.workspace.get_x_bounds()
        c2 = self.workspace.get_y_bounds()

        self.c_space = State_2D(c1, c2)

    def get_X_free(self):
        return self.c_space

    def get_information_gained(self):
        return self.i_gained

    def start(self, workspace):
        """
        Set initial conditions for the robot in a specified workspace
        :param workspace: Workspace object that describes the environment the agent is working in
        :return:
        """
        self.set_workspace(workspace)
        self.initialize_pdf()
        I_0 = self.get_information_available(self.state)
        start_node = Node.init_without_cost(self.state.get_position(), I_0, 0)
        self.path_log.append(start_node)
        self.state_log.append(self.state)

    def get_information_available(self, pos):
        """

        :return: information available in the specified grid cell.
        """
        if isinstance(pos, tuple):
            x, y = pos

        elif isinstance(pos, State_2D):
            x, y = pos.get_position()

        else:
            print("Error: data type unknown for get_information_available")
            print(type(pos))
            return None

        x = trunc(x)
        y = trunc(y)

        return self.pdf[y][x]

    def set_information_available(self, pos, value):
        if isinstance(pos, tuple):
            x, y = pos

        elif isinstance(pos, State_2D):
            x, y = pos.get_position()

        else:
            print("Error: data type unknown for get_information_available")
            print(type(pos))
            return None

        x = trunc(x)
        y = trunc(y)

        self.pdf[y][x] = value
        self.pdf = self.pdf / np.sum(self.pdf)  # normalize

    def update_information(self):
        """
        updated probability target is in current grid cell for the time step
        :return:
        """
        i_available = self.get_information_available(self.state)
        i_remaining = i_available * (1 - self.cfg["gamma"])
        self.set_information_available(self.state, i_remaining)

        i_gained = i_available - i_remaining
        self.state.set_information(i_gained)
        self.i_gained += i_gained
