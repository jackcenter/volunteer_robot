# !/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from dynopy.agents.volunteer2D import Volunteer2D


class Workspace:
    def __init__(self, boundary_coordinates, cfg, waypoints=None):
        """
        Contains information associated with an environment the agents can work in.
        TODO: add obstacle functionality
        :param boundary_coordinates: list of tuples
        :param cfg: list of dicts for gaussian parameters
        :param wp: list of lists of x, y tuples for default waypoints
        """
        self.boundary_coordinates = boundary_coordinates
        self.cfg = cfg
        self.default_waypoints = waypoints
        self.agents = []
        self.time_step = 0

        self.x_ordinates = [i[0] for i in self.boundary_coordinates]
        self.y_ordinates = [i[1] for i in self.boundary_coordinates]

        self.x_bounds = (min(self.x_ordinates), max(self.x_ordinates))
        self.y_bounds = (min(self.y_ordinates), max(self.y_ordinates))

        # self.map = None         # list of map coordinates
        self.pdf = None

    def plot(self):
        """
        Plots the environment boundaries as a black dashed line, the polygon obstacles, and the robot starting position
        and goal.
        :return: none
        """
        x_ords = self.x_ordinates.copy()
        x_ords.append(self.boundary_coordinates[0][0])

        y_ords = self.y_ordinates.copy()
        y_ords.append(self.boundary_coordinates[0][1])

        plt.plot(x_ords, y_ords, 'b-')

        x_min = self.x_bounds[0]
        x_max = self.x_bounds[1] + 1
        y_min = self.y_bounds[0]
        y_max = self.y_bounds[1] + 1

        plt.axis('equal')
        # plt.grid(b=None, which='major', axis='both')
        plt.xticks(range(x_min, x_max, 1))
        plt.yticks(range(y_min, y_max, 1))
        plt.xlabel(r"Easting, $\xi$ [kilometers]")
        plt.ylabel(r"Northing, $\eta$ [kilometers]")

        for agent in self.agents:

            if isinstance(agent, Volunteer2D):
                cfg_volunteer = agent.cfg
                break

        lamb = cfg_volunteer.get("lambda")
        steps = cfg_volunteer.get("budget")
        t_planning = cfg_volunteer.get("t_limit")
        gamma = cfg_volunteer.get("gamma")
        plt.suptitle("Volunteer Robot")
        plt.title(r"$\lambda$: {}, B: {}, t: {}, $\gamma$: {}".format(lamb, steps, t_planning, gamma))

        for robot in self.agents:
            robot.plot()
            robot.plot_visited_cells()
            if isinstance(robot, Volunteer2D):
                robot.plot_visited_cells_edges()
            robot.plot_path()

    def get_default_waypoints(self, n):
        return self.default_waypoints[n]

    def get_agents(self):
        return self.agents

    def get_time_step(self):
        return self.time_step

    def get_x_bounds(self):
        """

        :return: a tuple of the min and max x value
        """
        return self.x_bounds

    def get_y_bounds(self):
        """

        :return: a tuple of the min and max y value
        """
        return self.y_bounds

    def step(self):
        """
        Moves the workspace forward one time step
        :return:
        """
        for agent in self.agents:
            agent.step()

        self.time_step += 1

    def add_agent(self, agent):
        self.agents.append(agent)

    # def generate_grid(self):
    #     x_range = np.arange(self.x_bounds[0], self.x_bounds[1])
    #     y_range = np.arange(self.y_bounds[0], self.y_bounds[1])
    #
    #     coordinates = []
    #     for x in x_range:
    #         row = []
    #         for y in y_range:
    #             row.append((x, y))
    #
    #         coordinates.append(row)
    #
    #     self.map = coordinates

    def generate_initial_distribution(self, dx=1, dy=1):
        """
        Creates the initial distribution across the grid world.
        :param dx: grid size in the x direction
        :param dy: grid size in the y direction
        :param multi: generate from multiple gaussian distributions
        :return:
        """
        x_range = np.arange(self.x_bounds[0], self.x_bounds[1], dx)
        y_range = np.arange(self.y_bounds[0], self.y_bounds[1], dy)
        X, Y = np.meshgrid(x_range, y_range)
        pdf = np.zeros(X.shape)

        for gaussian in self.cfg:
            # guassian is a dict with 2D mean and variance
            x_norm = stats.norm(loc=gaussian.get("x_mean"), scale=gaussian.get("x_var"))
            y_norm = stats.norm(loc=gaussian.get("y_mean"), scale=gaussian.get("y_var"))

            pX = x_norm.pdf(X)
            pY = y_norm.pdf(Y)
            pdf += pX*pY

        # if multi:
        #     x_norm = stats.norm(loc=self.cfg.get("x_mean1"), scale=self.cfg.get("x_var1"))
        #     y_norm = stats.norm(loc=self.cfg.get("y_mean1"), scale=self.cfg.get("y_var1"))
        #     pX = x_norm.pdf(X)
        #     pY = y_norm.pdf(Y)
        #     self.pdf += pX * pY
        #
        #     x_norm = stats.norm(loc=self.cfg.get("x_mean2"), scale=self.cfg.get("x_var2"))
        #     y_norm = stats.norm(loc=self.cfg.get("y_mean2"), scale=self.cfg.get("y_var2"))
        #     pX = x_norm.pdf(X)
        #     pY = y_norm.pdf(Y)
        #     self.pdf += pX * pY

        self.pdf = pdf / np.sum(pdf)
