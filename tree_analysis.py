# !/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def update_information():
    """
    Walk through the tree and update information at each node. Should account for
    :return:
    """
    pass


def identify_fusion_nodes():
    """
    Look for nodes that are going to be in close proximity to other agents
    :return:
    """
    pass


def pick_path(V, E):
    """
    picks a path simply based on the highest information in a path
    :param V: list of nodes
    :param E: list of directed node tuples
    :return: list of nodes that represent a path
    """

    searching = True
    max_node = max(V, key=lambda item: item.get_information())  # finds node with most information
    path = [max_node]

    while searching:
        searching = False
        for root, leaf in E:
            if leaf == path[-1]:
                path.append(root)
                searching = True
                break

                # the node is not a leaf, so it is the root, so the search is complete

    # end when there isn't another edge found.
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
