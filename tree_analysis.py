# !/usr/bin/env python
# -*- coding: utf-8 -*-

from math import trunc
import matplotlib.pyplot as plt
import numpy as np
from config import config

# ================================
# THIS VERSION HAS BEEN DEPRECATED
# ================================

cfg = config.get_parameters()


def update_information(V, E, epsilon_0):
    """
    Walk through the path and update information at each node.
    :param V: list of nodes
    :param E: list of edges
    :param epsilon_0: information in the environment
    :return: List of nodes with updated information values
    """

    ol = [V[0]]     # open list
    bl = []         # branch list for visited nodes
    cl = []         # closed list

    epsilon_list = [epsilon_0]

    while ol:
        node = ol[-1]
        epsilon = epsilon_list[-1]

        if node not in bl:
            I_gained = get_information_gained(epsilon, node, cfg["gamma"])
            I_parent = bl[-1].get_information() if bl else 0
            node.set_information(I_gained + I_parent)

        neighbors_all = find_neighbors(E, node)
        neighbors_open = list(set(neighbors_all).difference(cl))

        if neighbors_open:
            ol.extend(neighbors_open)
            bl.append(node)

            I_parent = bl[-1].get_information() if bl else 0
            I_gained = node.get_information() - I_parent

            epsilon_new = update_epsilon(epsilon, node, I_gained)
            epsilon_list.append(epsilon_new)

        elif node in bl:
            ol.pop()
            bl.pop()
            cl.append(node)
            epsilon_list.pop()

        else:
            ol.pop()
            cl.append(node)


def get_information_gained(epsilon, node, gamma):
    """
    returns the information gained
    :param epsilon:
    :param node:
    :param gamma: coefficient for the rate at which information is gained compared to information available
    :return:
    """
    I_available = get_information_available(epsilon, node)
    I_gained = gamma*I_available
    return I_gained


def update_epsilon(epsilon_k0, node, I_gained):

    I_available = get_information_available(epsilon_k0, node)
    I_remaining = I_available - I_gained
    epsilon_k1 = set_information_available(epsilon_k0.copy(), node, I_remaining)
    return epsilon_k1


def get_information_available(epsilon, node):
    x, y = node.get_position()
    x = trunc(x)
    y = trunc(y)
    I_available = epsilon[x][y]
    return I_available


def set_information_available(epsilon, node, value):
    x, y = node.get_position()
    x = trunc(x)
    y = trunc(y)
    epsilon[x][y] = value
    epsilon = normalize_pdf(epsilon)
    return epsilon


def normalize_pdf(pdf):
    return pdf / np.sum(pdf)


def find_neighbors(E, node):
    """

    :param E: list of edges
    :param node: base node
    :return: list of neighbors
    """
    neighbors_list = []
    for parent, child in E:
        if node == parent:
            neighbors_list.append(child)
    return neighbors_list


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


def prune_step(V, E, path):
    ol = []
    cl = []

    for root, leaf in E:
        if root == path[-1] and leaf != path[-2]:
            ol.append(leaf)

    while ol:
        node = ol[-1]
        neighbors_all = find_neighbors(E, node)
        neighbors_open = list(set(neighbors_all).difference(cl))

        if neighbors_open:
            ol.extend(neighbors_open)

        else:
            ol.pop()
            cl.append(node)

    V = delete_nodes(V, cl)
    E = delete_edges_by_leaf(E, cl)
    return V, E


def delete_nodes(V, nodes):
    V = [x for x in V if x not in nodes]
    return V


def delete_edges_by_leaf(E, leafs):
    E = [x for x in E if x[1] not in leafs]
    return E


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


def print_information_in_nodes(V):
    print()
    print("Information in nodes:")

    for node in V:
        print("Time step: {}, Pos: {}, Info: {} \n".format(node.get_time(), node.get_pretty_position(),
                                                           node.get_information()))
