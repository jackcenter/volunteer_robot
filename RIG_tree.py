import numpy as np
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
    I_init = initial_information(x_0, epsilon)      # Initial node information
    C_init = 0                                      # Initial node cost
    n_0 = Node(x_0, C_init, I_init)                 # Initial node
    V = [n_0]                                       # Node list
    V_closed = []                                   # Closed node list
    E = []                                          # Edge list

    # Sample configuration space of vehicle and find nearest node
    running = True
    while running:
        x_sample = sample(X_all)
        n_nearest = nearest(x_sample, list(set(V).difference(V_closed)))
        x_feasible = steer(n_nearest.get_position(), x_sample, d)

        # find near points to be extended
        n_near = near(x_feasible, list(set(V).difference(V_closed)), R)

        for n in n_near:
            # extend towards new point
            x_new = steer(n_near.get_position(), x_feasible, d)
            if no_collision(n_near.get_position(), x_new, X_free):
                # calculate new information and cost
                # TODO: how does information change with time and how do I account for it?
                I_new = information(n_near.get_information(), x_new, epsilon)
                # TODO: clean up this cost stuff below
                C_x_new = evaluate_cost(n_near.get_position(), x_new)
                C_new = n_near.get_cost() + C_x_new
                n_new = Node(x_new, C_new, I_new)

                if prune(n_new):
                    pass

                else:
                    # add edge and node
                    E.append((n_near, n_new))
                    V.append(n_new)
                    if C_new > B:
                        V_closed.append(n_new)

    return V, E


def initial_information(x_0, epsilon):
    """
    takes initial position and determines information gained from being there for one time step.
    :param x_0: initial state
    :param epsilon: environment pdf
    :return: initial information
    """
    x, y = x_0.get_position()
    return epsilon[x][y]


def sample(X_all):
    """

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

    :param x_s: sampled position
    :param V_open: set of nodes that are still open
    :return:
    """
    pass


def steer(x_n_nearest, x_sample, d):
    """

    :param x_n_nearest: position of the nearest node
    :param x_sample: sampled position
    :param d: step size of the agent
    :return: x_feasible - a feasible position
    """
    pass


def near(x_feasible, V_open, R):
    """

    :param x_feasible: feasible position found
    :param V_open: set of nodes that are still open
    :param R: nearest neighbor radius parameter
    :return: list of nodes near x_feasible
    """
    pass


def no_collision(x_n_near, x_new, X_free):
    """

    :param x_n_near:
    :param x_new:
    :param X_free:
    :return:
    """
    pass


def information(I_n_near, x_new, epsilon):
    """

    :param I_n_near: information in the near node
    :param x_new: new node position
    :param epsilon: environment
    :return: new information
    """
    pass


def evaluate_cost(x_n_near, x_new):
    """

    :param x_n_near: position of nearest node
    :param x_new: position of new node
    :return:
    """
    pass


def prune(n_new):
    """
    check if the new node should be pruned and delete if needed
    :param n_new:
    :return:
    """
    pass
