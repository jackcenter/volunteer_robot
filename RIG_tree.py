

def RIG_tree(d,  B, X_all, X_free, epsilon, x_0, R):
    """

    :param d: single dynamic step
    :param B: budget
    :param X_all: workspace
    :param X_free: free space
    :param epsilon: environment
    :param x_0: initial state
    :param R: nearest neighbor radius
    :return: tree, a list of
    """

    # node is [position, Cost?, Information]
    # Initialize cost C, information I, starting node x_0, node list V, edge list E, and tree T

    # Sample configuration space of vehicle and find nearest node
    pass


def initial_information(x_0, epsilon):
    """

    :param x_0: initial state
    :param epsilon: environment
    :return: initial information
    """
    pass


def nearest(x_s, V_open):
    """

    :param x_s: sampled position
    :param V_open: set of nodes that are still open
    :return:
    """
    pass


def steer(x_n_nearest, x_s, d):
    """

    :param x_n_nearest: position of the nearest node
    :param x_s: sampled position
    :param d: step size of the agent
    :return: x_feasible - a feasible position
    """
    pass


def near(x_feasible, V_open, R):
    """

    :param x_feasible: feasible position found
    :param V_open: set of nodes that are still open
    :param R: nearest neighbor radius parameter
    :return: set of nodes near x_feasible
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
