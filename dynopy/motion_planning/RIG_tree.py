# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, cos, sin, trunc, pi
from time import process_time
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from config import config
from dynopy.data_objects.node import Node
from tree_analysis import plot_tree

cfg = config.get_parameters()


def RIG_tree(V,  E, V_closed, X_all, X_free, epsilon, x_0, parameters):
    """

    :param V: node list for a prebuilt tree
    :param E: edge list for a prebuilt tree
    :param V_closed: list of nodes that can't be expanded
    :param X_all: workspace
    :param X_free: free space
    :param epsilon: environment
    :param x_0: initial state
    :param parameters: dictionary of neccessary values: step size, budget, nearest neighbor radius, input samples, and
    time limit for expansion
    :return: a list of nodes and edges
    """
    # Initialize cost C, information I, starting node x_0, node list V, edge list E, and tree T
    np.random.seed(769)      # 50 with lambda = 0 shows a weird error where agents decides to ignore a good path
    d = parameters["step_size"]
    B = parameters["budget"]
    R = parameters["radius"]
    input_samples = parameters["samples"]
    t_limit = parameters["t_limit"]

    if not V:
        I_init = initial_information(x_0, epsilon)      # Initial node information
        C_init = 0                                      # Initial node cost
        n_0 = Node(x_0, C_init, I_init, 0)              # Initial node
        V = [n_0]                                       # Node list
        V_closed = []                                   # Closed node list
        E = []                                          # Edge list

    # Sample configuration space of vehicle and find nearest node
    t_0 = process_time()
    while process_time() - t_0 < t_limit:
        x_sample = sample(X_all)
        n_nearest = nearest(x_sample, list(set(V).difference(V_closed)))
        x_feasible = steer(n_nearest.get_position(), x_sample, d, input_samples, 'y.')

        # find near points to be extended
        # print("Full list: {}".format(V))
        # print("Closed list: {}".format(V_closed))
        # print("Open list: {}".format(list(set(V).difference(V_closed))))
        n_near = near(x_feasible, list(set(V).difference(V_closed)), R)

        for node in n_near:
            if node.get_time() >= parameters.get("budget"):
                continue

            # extend towards new point
            x_new = steer(node.get_position(), x_feasible, d, input_samples)

            if collision(node.get_position(), x_new, X_free):
                continue

            C_x_new = evaluate_cost(node.get_position(), x_new)
            C_new = node.get_cost() + C_x_new

            if in_range_of_home(parameters["home"], x_new, C_new, parameters["budget"]):
                I_new = information(node.get_information(), x_new, epsilon)
                # C_x_new = evaluate_cost(node.get_position(), x_new)
                # C_new = node.get_cost() + C_x_new
                k_new = node.get_time() + 1             # represents one time step, could be actual time
                n_new = Node(x_new, C_new, I_new, k_new)

                if prune(n_new):
                    pass

                else:
                    # add edge and node
                    E.append((node, n_new))
                    V.append(n_new)
                    if n_new.get_cost() > B:
                        V_closed.append(n_new)

            if cfg["plot_full"]:
                plot_tree(E)
                plot_expansion(x_sample, x_feasible, node.get_position(), x_new)

    return V, E, V_closed


def initial_information(x_0, epsilon):
    """
    takes initial position and determines information gained from being there for one time step.
    :param x_0: initial state
    :param epsilon: environment pdf
    :return: initial information
    """
    x, y = trunc(x_0[0]), trunc(x_0[1])
    return epsilon[x][y]


def sample(X_all):
    """
    samples the configuration space for a random node position
    :param X_all:
    :return:
    """
    x_min, x_max = X_all.get_x_position()
    y_min, y_max = X_all.get_y_position()

    x = random_sample(x_min, x_max)
    y = random_sample(y_min, y_max)

    return x, y


def random_sample(a, b):
    """

    :param a: lower bound
    :param b: upper bound
    :return: random value between a and b
    """
    r = np.random.rand()
    return a + r*(b - a)


def nearest(x_s, V_open):
    """
    finds the node in the tree closest to the sampled position
    :param x_s: sampled position
    :param V_open: set of nodes that are still open
    :return: the node with a position closest to the sampled position
    """

    node_nearest = V_open[0]
    min_dist = get_distance(x_s, node_nearest.get_position())

    for node in V_open:
        test_dist = get_distance(x_s, node.get_position())

        if test_dist < min_dist:
            node_nearest = node
            min_dist = test_dist

    return node_nearest


def get_distance(x1, x2):
    """

    :param x1: first x, y position
    :param x2: second x, y position
    :return: euclidean distance apart
    """
    return sqrt((x2[0] - x1[0])**2 + (x2[1] - x1[1])**2)


def steer(x_0, x_sample, d, samples, marker='g.'):
    """

    :param x_0: position of the nearest node
    :param x_sample: sampled position
    :param d: step size of the agent
    :param samples: number of inputs to sample
    :param marker: color for plotting
    :return: x_feasible, a feasible position
    """
    # sample dynamics starting at x_nearest state
    x_nearest = x_0
    d_nearest = get_distance(x_0, x_sample)

    # sample between -1 and 1 for x and y then normalize to 0
    uniform = stats.uniform(loc=0, scale=2*pi)

    for i in range(0, samples):
        theta_rand = uniform.rvs()
        x_rand = x_0[0] + d*cos(theta_rand)
        y_rand = x_0[1] + d*sin(theta_rand)
        rand_pos = (x_rand, y_rand)
        d_rand = get_distance(rand_pos, x_sample)

        if cfg["plot_full"]:
            plt.plot(x_rand, y_rand, marker)

        if d_rand < d_nearest:
            x_nearest = rand_pos
            d_nearest = d_rand

    return x_nearest


def near(x_feasible, V_open, R):
    """

    :param x_feasible: feasible position found
    :param V_open: set of nodes that are still open
    :param R: nearest neighbor radius parameter
    :return: list of nodes near x_feasible
    """
    nodes_near = []

    for node in V_open:
        x_node = node.get_position()
        d = get_distance(x_node, x_feasible)

        if d < R:
            nodes_near.append(node)

    return nodes_near


def collision(x_n_near, x_new, X_free):
    """
    No collision checking is done at the moment, assuming no obstacles
    :param x_n_near:
    :param x_new:
    :param X_free:
    :return:
    """
    # TODO: actually check for obstacles
    return False


def in_range_of_home(x_home, x_new, cost, budget):

    range_current = get_distance(x_home, x_new)
    range_max = budget - cost       # - range_current

    if range_current <= range_max:
        return True

    else:
        return False


def information(I_n_near, x_new, epsilon):
    """
    Takes the current information gained on the branch and adds it to the information that can be gained from moving to
    the new position.
    :param I_n_near: information in the near node
    :param x_new: new node position
    :param epsilon: environment
    :return: new information
    """
    # TODO: needs to account for a changing pdf
    x, y = trunc(x_new[0]), trunc(x_new[1])

    try:
        I_new = epsilon[x][y]
    except IndexError:
        I_new = 0       # outside the workspace bounds, no information to be gained

    I_total = I_n_near + I_new
    return I_total


def evaluate_cost(x_n_near, x_new):
    """
    Simply uses the distance traveled as the cost.
    :param x_n_near: position of nearest node
    :param x_new: position of new node
    :return:
    """
    cost = get_distance(x_n_near, x_new)
    return cost


def prune(n_new):
    """
    check if the new node should be pruned and delete if needed
    :param n_new:
    :return:
    """
    # TODO: function is being bypassed for now
    return False


def plot_expansion(x_sample, x_feasible, node_pos, x_new):
    """
    used to troubleshoot issues with the tree expansion
    :return:
    """
    plt.plot(x_sample[0], x_sample[1], 'bx')
    plt.plot(x_feasible[0], x_feasible[1], 'yo')
    plt.plot(node_pos[0], node_pos[1], 'k.')
    plt.plot(x_new[0], x_new[1], 'kx')
    plt.axis('equal')
    plt.show()
    pass
