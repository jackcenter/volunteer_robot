# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
import matplotlib.pyplot as plt
from config import config

cfg = config.get_parameters()


def update_information(V, E, epsilon_0, gamma):
    """
    Walk through the path and update information at each node.
    :param V: list of nodes
    :param E: list of edges
    :param epsilon: information in the environment
    :param gamma: sensor efficiency
    :return: List of nodes with updated information values
    """

    ol = [V[0]]
    cl = []
    epsilon_list = [epsilon_0]

    # while ol:
    #   calc new epsilon for last node in open list
    #       get information gained and adjust node value
    #       change epsilon value and normalize
    #       append epsilon to base_epsilon

    #   find neighbors of last node in open list
    #       if not in the closed list:
    #           add to ol
    #           loop
    #       else -> means no where to expand to:
    #           remove last appended epsilon
    #           move node to cl

    while ol:
        node = ol[-1]
        epsilon_k0 = epsilon_list[-1]
        I_new = get_information_gained(epsilon_k0, node.get_position(), cfg["gamma"])
        node.set_information(I_new)
        epsilon_k1 = update_epsilon(epsilon_k0, node)
        epsilon_list.append(epsilon_k1)

        neighbors_all = find_neighbors(node, E)
        neighbors_open = list(set(neighbors_all).difference(cl))

        if neighbors_open:
            ol.extend(neighbors_open)
        else:
            epsilon_list.pop()
            cl.append(node)
            ol.pop()


    # # expand the root
    # for root, leaf in E:
    #     branches = 0
    #     node = open_list.pop
    #     if node == root:
    #         open_list.append(leaf)
    #         branches += 1
    #
    #
    #
    # # Start at the root, take position and update epsilon with a depth first approach
    # #   find all leaves
    # #
    # # Find all leaves
    # x, y = node.get_position()
    # i_available = epsilon[x][y]
    # node.set_information(i_available)
    #
    # i_remaining = i_available * gamma
    # epsilon[x][y] = i_remaining

    pass


def get_information_gained(epsilon, pos, gamma):
    """
    returns the information gained
    :param epsilon:
    :param pos:
    :param gamma: coefficient for the rate at which information is gained compared to information available
    :return:
    """
    return 0


def update_epsilon(epsilon, node):
    return 0


def find_neighbors(E, node):
    """

    :param E: list of edges
    :param node: base node
    :return: list of neighbors
    """
    return []


def identify_fusion_nodes(V_a, V_b, channel, fusion_range):
    """
    Look for nodes that are going to be in close proximity to other agents
    :param V_a: List of nodes for agent a (the volunteer)
    :param V_b: List of nodes for agent b (the independent agent)
    :param channel: agent the fusion will happen with
    :param fusion_range
    :return:
    """
    for node_b in V_b:
        for node_a in V_a:
            if node_a.get_distance_from(node_b) < fusion_range and node_a.compare_time(node_b):
                node_a.add_fusion(channel)
                print("fusion with {} found at: {}, k = {}".format(channel, node_a.get_position(), node_a.get_time()))


def pick_path(V, E):
    """
    picks a path simply based on the highest information in a path
    :param V: list of nodes
    :param E: list of directed node tuples
    :return: list of nodes that represent a path
    """

    max_node = max(V, key=lambda item: item.get_information())  # finds node with most information
    path = [max_node]

    searching = True

    while searching:
        searching = False
        for root, leaf in E:
            if leaf == path[-1]:
                path.append(root)
                searching = True
                break

    return path


def plot_leaves(V):
    for node in V:
        x, y = node.get_position()
        plt.plot(x, y, '.', color='red', mfc='none')


def plot_tree(E, color='red'):

    for node_0, node_1 in E:
        x0, y0 = node_0.get_position()
        x1, y1 = node_1.get_position()
        x_ords = [x1, x0]
        y_ords = [y1, y0]
        plt.plot(x_ords, y_ords, ls='--', c=color)
