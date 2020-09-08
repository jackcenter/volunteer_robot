from math import sqrt, cos, sin, trunc
import numpy as np
import scipy.stats as stats
from config import config
from dynopy.data_objects.node import Node


def RIG_tree(d,  B, X_all, X_free, epsilon, x_0, R):
    """

    :param d: single dynamic step
    :param B: budget
    :param X_all: workspace
    :param X_free: free space
    :param epsilon: environment
    :param x_0: initial state
    :param R: nearest neighbor radius
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
    while count < 10:
        x_sample = sample(X_all)
        n_nearest = nearest(x_sample, list(set(V).difference(V_closed)))
        x_feasible = steer(n_nearest.get_position(), x_sample, d, input_samples)

        # find near points to be extended
        n_near = near(x_feasible, list(set(V).difference(V_closed)), R)

        for node in n_near:
            # extend towards new point
            x_new = steer(node.get_position(), x_feasible, d, input_samples)
            if no_collision(node.get_position(), x_new, X_free):
                # calculate new information and cost
                # TODO: how does information change with time and how do I account for it?
                I_new = information(node.get_information(), x_new, epsilon)
                # TODO: clean up this cost stuff below
                C_x_new = evaluate_cost(node.get_position(), x_new)
                C_new = node.get_cost() + C_x_new
                n_new = Node(x_new, C_new, I_new)

                if prune(n_new):
                    pass

                else:
                    # add edge and node
                    E.append((n_near, n_new))
                    V.append(n_new)
                    if n_new.get_cost() > B:
                        V_closed.append(n_new)

        count += 1
        print(count)

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

        if min_dist > test_dist:
            node_nearest = node

    return node_nearest


def get_distance(x1, x2):
    """

    :param x1: first x, y position
    :param x2: second x, y position
    :return: euclidean distance apart
    """
    return sqrt((x2[0] - x1[0])**2 + (x2[1] - x2[1])**2)


def steer(x_0, x_sample, d, samples):
    """

    :param x_0: position of the nearest node
    :param x_sample: sampled position
    :param d: step size of the agent
    :param samples: number of inputs to sample
    :return: x_feasible, a feasible position
    """
    # sample dynamics starting at x_nearest state
    x_nearest = x_0
    d_nearest = get_distance(x_0, x_sample)

    # sample between -1 and 1 for x and y then normalize to 0
    uniform = stats.uniform(loc=0, scale=3.1415)

    for i in range(0, samples):
        theta_rand = uniform.rvs()
        x_rand = x_0[0] + d*cos(theta_rand)
        y_rand = x_0[1] + d*sin(theta_rand)
        rand_pos = (x_rand, y_rand)
        d_rand = get_distance(rand_pos, x_sample)

        if d_rand < d_nearest:
            x_nearest = rand_pos

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
    I_new = epsilon[x][y]
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
