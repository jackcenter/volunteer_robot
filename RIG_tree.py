from math import sqrt, cos, sin, trunc, pi
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from config import config
from dynopy.data_objects.node import Node


def RIG_tree(d,  B, X_all, X_free, epsilon, x_0, R, cycles=10):
    """

    :param d: single dynamic step
    :param B: budget
    :param X_all: workspace
    :param X_free: free space
    :param epsilon: environment
    :param x_0: initial state
    :param R: nearest neighbor radius
    :param cycles: number of times to sample and extend
    :return: a list of nodes and edges
    """
    # Initialize cost C, information I, starting node x_0, node list V, edge list E, and tree T
    cfg = config.get_parameters()
    input_samples = cfg["samples"]

    I_init = initial_information(x_0, epsilon)      # Initial node information
    C_init = 0                                      # Initial node cost
    n_0 = Node(x_0, C_init, I_init)                 # Initial node
    V = [n_0]                                       # Node list
    V_closed = []                                   # Closed node list
    E = []                                          # Edge list

    # Sample configuration space of vehicle and find nearest node
    count = 0
    while count < cycles:
        x_sample = sample(X_all)
        n_nearest = nearest(x_sample, list(set(V).difference(V_closed)))
        x_feasible = steer(n_nearest.get_position(), x_sample, d, input_samples, 'y.')

        # find near points to be extended
        # print("Full list: {}".format(V))
        # print("Closed list: {}".format(V_closed))
        # print("Open list: {}".format(list(set(V).difference(V_closed))))
        n_near = near(x_feasible, list(set(V).difference(V_closed)), R)

        for node in n_near:
            # extend towards new point
            x_new = steer(node.get_position(), x_feasible, d, input_samples)
            if no_collision(node.get_position(), x_new, X_free):
                I_new = information(node.get_information(), x_new, epsilon)
                C_x_new = evaluate_cost(node.get_position(), x_new)
                C_new = node.get_cost() + C_x_new
                n_new = Node(x_new, C_new, I_new)

                if prune(n_new):
                    pass

                else:
                    # add edge and node
                    E.append((node, n_new))
                    V.append(n_new)
                    if n_new.get_cost() > B:
                        V_closed.append(n_new)


            # plot_tree(E)
            # plt.plot(x_sample[0], x_sample[1], 'bx')
            # plt.plot(x_feasible[0], x_feasible[1], 'yo')
            # plt.plot(node.get_position()[0], node.get_position()[1], 'k.')
            # plt.plot(x_new[0], x_new[1], 'kx')
            # plt.axis('equal')
            # plt.show()

        print(count)
        count += 1


    return V, E


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

        # plt.plot(x_rand, y_rand, marker)

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


def no_collision(x_n_near, x_new, X_free):
    """
    No collision checking is done at the moment, assuming no obstacles
    :param x_n_near:
    :param x_new:
    :param X_free:
    :return:
    """
    # TODO: actually check for obstacles
    return True


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
        I_new = 0

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

