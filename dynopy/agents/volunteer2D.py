# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, cos, sin, atan2, trunc
import time
import matplotlib.patches as patch
import numpy as np
from dynopy.agents.robot2D import Robot2D
from dynopy.data_objects.state import State_2D
from dynopy.data_objects.input import Input_2D
import dynopy.motion_planning.IRRT as irrt
import dynopy.motion_planning.RIG_tree_R_based as RIG2
from dynopy.motion_planning.tree_analysis import update_information, identify_fusion_nodes, pick_path_max_I, \
    pick_path_max_R, prune_step, plot_tree, print_nodes_with_reward


class Volunteer2D(Robot2D):
    def __init__(self, name: str, cfg, state=None, irrt=False, plot_full=False):
        super().__init__(name, state, plot_full)

        self.cfg = cfg
        self.V = []
        self.E = []
        self.V_closed = []
        self.B = None
        self.channel_list = {}      # name : path
        self.channel_range = {}     # name : range
        self.information_shared = {}
        self.information_novel = {}
        self.irrt = irrt
        self.goals = []
        self.goal = None
        # TODO: add other agents planned paths as dict of channel: path

    def load_waypoints(self, waypoints, budget):
        self.cfg.update({"home": waypoints[0]})

    def get_budget_radius_object(self):
        x, y = self.cfg.get('home')
        radius = self.cfg.get("budget") - self.state.get_time()
        circle = patch.Circle((x, y), radius, fill=False, ec='yellow', ls='--', alpha=1)
        return circle

    # TODO: move this fusion stuff so all robots can do it
    def initialize_channels(self, agents):
        for agent in agents:
            if agent.get_name() != self.get_name():
                self.channel_list.update({agent.get_name(): agent.get_path()})
                self.information_shared.update({agent.get_name(): 0.0})
                self.information_novel.update({agent.get_name(): self.get_information_gained()})

                if agent.cfg.get("fusion_range") < self.cfg.get("fusion_range"):
                    f = agent.cfg.get("fusion_range")
                else:
                    f = self.cfg.get("fusion_range")

                self.channel_range.update({agent.get_name(): f})

                if self.irrt:
                    # setting agents locations as goal points
                    self.goals.append([agent.get_name(), agent.get_position(), 0])

        if self.irrt:
            self.goals.append(["home", self.cfg.get("home"), 0])
            self.goals.reverse()

            points = []

            for g in self.goals:
                points.append(g[1])

            # print(points)

            distances = []
            start = self.get_position()
            while points:
                g = points.pop()
                distances.append(irrt.get_distance(start, g))
                start = g

            min_dist = sum(distances)
            budgets = [trunc(self.cfg.get("budget")*x/min_dist) - 1 for x in distances]
            budgets.reverse()

            # b_sum = self.cfg.get("budget")
            for goal, budget in zip(self.goals, budgets):
                goal[2] = budget
                # b_sum -= budget
            # print(points)
            # print(distances)
            # print(self.goals)

            self.goal = self.goals.pop()

    def fuse(self, channel):
        """
        this function replaces real world comm range. In actual implementation agents should fuse whenever possible, or
        when simulating on hardware, whenever within some predefined distance like this.
        :param channel:
        :return:
        """
        pos1 = self.get_position()
        agent = next(x for x in self.workspace.get_agents() if x.get_name() == channel)

        _, distance = self.get_direction_and_distance(pos1, agent.get_position())
        if abs(distance) < self.channel_range.get(agent.get_name()):
            pdf1 = self.get_pdf()
            pdf2 = agent.get_pdf()

            for x, y in np.ndindex(pdf1.shape):

                if pdf2[x][y] < pdf1[x][y]:
                    pdf1[x][y] = pdf2[x][y]

            pdf1 = pdf1 / np.sum(pdf1)
            self.set_pdf(pdf1)
            self.information_shared.update({channel: self.get_information_gained()})
            novel_information = self.get_information_gained() - self.information_shared.get(channel)
            self.information_novel.update({channel: novel_information})

            if self.plot_full:
                print("{} and {} can fuse!".format(self.get_name(), agent.get_name()))
                print("Positions: {}, {}".format(self.get_position(), agent.get_position()))
                print("Distance: {}\n".format(distance))

    def get_tree(self):
        return self.V, self.E

    def get_nodes(self):
        return self.V

    def get_edges(self):
        return self.E

    def step(self):
        """
        moves the agent in the commanded direction
        :param
        :return:
        """

        self.execute_planning_cycle()

        if self.plot_full:
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
        k1 = root.get_time()            # TODO: simply takes node time, could update based on current time instead
        state = State_2D(x1, y1, theta, time=k1)

        self.trajectory_log.append(action)
        self.state = state
        self.state_log.append(self.state)
        self.update_information()

        for channel in self.channel_list.keys():
            self.fuse(channel)

        # TODO: update all channel paths

    def sample_dynamics(self, x_0):
        u1_range, u2_range = self.cfg.get("dynamics_range")

        r = np.random.rand(2)

        u1 = u1_range[0] + r[0]*(u1_range[1] - u1_range[0])
        u2 = u2_range[0] + r[1]*(u2_range[1] - u2_range[0])

        u = Input_2D(u1, u2)

        x_next = self.dynamics_function(x_0, u)

        return x_next, u

    @staticmethod
    def dynamics_function(x_0, u):
        theta = x_0.get_theta()
        theta += u.get_direction()

        x_new = x_0.get_x_position() + u.get_distance()*cos(theta)
        y_new = x_0.get_y_position() + u.get_distance()*sin(theta)

        k = x_0.get_time() + 1

        x = State_2D(x_new, y_new, theta, 0, k)
        return x

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

        # print(len(self.V))
        # self.get_state().print()
        # if not len(self.V):
        #     self.get_state().print()

        t_0 = time.process_time()
        self.expand_tree(self.irrt)

        t_1 = time.process_time() - t_0
        self.select_path(self.irrt)

        t_2 = time.process_time() - t_1 - t_0
        if self.plot_full:
            plot_tree(self.E, 'blue')
            # print_nodes_with_reward(self.get_tree()[0])
            # print(self.pdf)

        t_3 = time.process_time() - t_2 - t_1 - t_0
        self.prune_passed_nodes()

        t_4 = time.process_time() - t_3 - t_2 - t_1 - t_0
        self.generate_trajectory()

        t_5 = time.process_time() - t_4 - t_3 - t_2 - t_1 - t_0

        if self.irrt:
            self.check_at_goal()

        if self.plot_full:
            print("Time Step:\t{}\n Expanion:\t{}\n Selection:\t{}\n Pruning:\t{}\n Generation:\t{}\n".format(
                self.state.get_time(), t_1, t_2, t_4, t_5))

            print(" I Gained:\t{}".format(self.get_information_gained()))
            I_added = 0
            for channel, info in self.information_novel.items():
                print(" " + channel + ":\t\t{}".format(self.get_information_gained() - info))
                I_added += self.get_information_gained() - info

            print(" Reward:\t{}\n".format(I_added/len(self.channel_list)))

    def expand_tree(self, IRRT=False):
        # self.V, self.E, self.V_closed = RIG_tree(self.V, self.E, self.V_closed, self.get_X_free(), self.get_X_free(),
        #                                          self.get_pdf(), self.get_position(), self.cfg)

        if not IRRT:
            self.V, self.E = RIG2.RIG_tree(self.V, self.E, self.get_X_free(), self.get_X_free(), self.get_pdf(),
                                           self.get_state(), self.cfg, self.sample_dynamics, self.channel_list)
        else:
            # TODO needs to take waypoints from channel list as goal points and update as it goes
            self.V, self.E, self.V_closed = irrt.IRRT_tree(self.V, self.E, self.V_closed, self.get_X_free(),
                                                      self.get_X_free(), self.get_pdf(), self.get_state(), self.goal[1],
                                                      self.cfg, self.sample_dynamics, self.channel_list, self.goal[2])

        # print_nodes_with_reward(self.V)

    def select_path(self, IRRT=False):
        # for agent, path in self.channel_list.items():
        #     f = self.channel_range.get(agent)
        #     identify_fusion_nodes(self.V, path, agent, f)

        if not IRRT:
            RIG2.update_information(self.V, self.E, self.pdf, self.i_gained, self.information_shared, self.channel_list,
                                self.cfg)

            # self.path = pick_path_max_I(self.V, self.E)
            self.path = pick_path_max_R(self.V, self.E)

        else:
            RIG2.update_information(self.V, self.E, self.pdf, self.i_gained, self.information_shared, self.channel_list,
                                    self.cfg)

            self.path = irrt.pick_irrt_path(self.V, self.E)
            # TODO: finish this
            # print([x.get_position() for x in self.path])
            # print(self.get_position())

    def prune_passed_nodes(self):
        self.V, self.E = prune_step(self.V, self.E, self.path)
        # TODO: prune the closed list

    def update_information(self):
        """
        updated probability target is in current grid cell for the time step
        :return:
        """
        i_available = self.get_information_available(self.state)
        i_remaining = i_available * (1 - self.cfg["p_d"])
        self.set_information_available(self.state, i_remaining)

        i_gained = i_available - i_remaining
        self.state.set_information(i_gained)
        self.i_gained += i_gained
        for channel in self.information_novel.keys():
            info_k1 = self.information_novel.get(channel) + i_gained
            self.information_novel.update({channel: info_k1})

    def check_at_goal(self):

        # print(len(self.trajectory))

        if len(self.path) == 1 and self.path[0].get_goal_status:
            # print("At goal!")

            try:
                self.goal = self.goals.pop()
                self.V = []
                self.E = []
                self.V_closed = []
            except IndexError:
                pass
                # print("Home!")
