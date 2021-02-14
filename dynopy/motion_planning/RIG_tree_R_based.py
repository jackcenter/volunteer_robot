import math
from time import process_time
import matplotlib.pyplot as plt
import numpy as np
from dynopy.data_objects.node_traj import Node
from dynopy.motion_planning.tree_analysis import plot_tree
from config.config import get_parameters
from tree_analysis import plot_tree

cfg_ws = get_parameters()


def RIG_tree(V,  E, V_closed, X_all, X_free, epsilon, x_0, cfg, f_dynamics):
    """

    :param V: node list for a prebuilt tree
    :param E: edge list for a prebuilt tree
    :param V_closed: list of nodes that can't be expanded
    :param X_all: workspace
    :param X_free: free space
    :param epsilon: environment
    :param x_0: initial state
    :param cfg: dictionary of necessary values: step size, budget, nearest neighbor radius, input samples, and
    time limit for expansion
    :param f_dynamics: dynamics function
    :return: a list of nodes and edges
    """

    d = cfg["step_size"]
    B = cfg["budget"]
    R = cfg["radius"]
    input_samples = cfg["samples"]
    t_limit = cfg["t_limit"]

    if not V:
        V, E, V_closed = initialize_graph(x_0, epsilon)

    t_0 = process_time()

    # while process_time() - t_0 < t_limit:

    while 1:
        # Expand the tree while time remains
        V_open = list(set(V).difference(V_closed))
        pos_sample = sample_position(X_all, cfg)
        n_nearest = find_nearest(pos_sample, V_open)
        x_feasible, _ = steer(n_nearest.get_state(), pos_sample, f_dynamics, cfg, 'y.')
        print(x_feasible.get_position())
        n_near = find_nearby(x_feasible, V_open, cfg)

        R_best = 0
        node_best = None
        n_best = None

        for node in n_near:
            print(node.get_position())

            x_new, u_new = steer(node.get_state(), pos_sample, f_dynamics, cfg)
            print(x_new.get_position())

            # TODO: compute cost
            c_new = 0
            # TODO: compute reward
            i_new = 0
            r_new = 0

            k_new = node.get_time() + 1
            node_new = Node(x_new, u_new, c_new, i_new, k_new, r_new)

        V.append(node_new)
        E.append((node, node_new))

        plot_tree(E)
        plt.axis("equal")
        plt.show()

        # if node.get_time() >= cfg.get("budget"):
        #     # TODO: don't throw out, add to cost
        #     continue

        # extend towards new point
        # x_new = steer(node.get_position(), x_feasible, d, input_samples)
        #
        # if cfg["plot_full"]:
        #     plot_tree(E)
        #     plot_expansion(x_sample, x_feasible, node.get_position(), x_new)
        #
        # # TODO: add in too far from home cost
        # C_x_new = evaluate_cost(node.get_position(), x_new)
        # C_new = node.get_cost() + C_x_new
        #
        # # TODO: find expected reward on static pdf and pick node based on that


def initialize_graph(x_0, epsilon):
    """
    creates the initial graph if none has been previously computed.
    :param x_0: initial state
    :param epsilon: initial distribution
    :return:
    """
    i_init = initial_information(x_0.get_position(), epsilon)  # Initial node information
    c_init = 0                                  # Initial node cost
    n_0 = Node(x_0, None, c_init, i_init, 0)          # Initial node
    v = [n_0]                                   # Node list
    e = []
    v_closed = []
    return v, e, v_closed


def initial_information(x_0, epsilon):
    """
    takes initial position and determines information gained from being there for one time step.
    :param x_0: initial state
    :param epsilon: environment pdf
    :return: initial information
    """
    x, y = math.trunc(x_0[0]), math.trunc(x_0[1])
    return epsilon[x][y]


def sample_position(x_all, parameters):
    """
    samples the configuration space for a random node position
    :param x_all:
    :param parameters:
    :return:
    """
    v_sample = np.random.rand()
    if v_sample < 0.05:
        x_sample = parameters.get("home")

    else:
        x_min, x_max = x_all.get_x_position()
        y_min, y_max = x_all.get_y_position()

        x = random_sample(x_min, x_max)
        y = random_sample(y_min, y_max)
        x_sample = (x, y)

    return x_sample


def random_sample(a, b):
    """

    :param a: lower bound
    :param b: upper bound
    :return: random value between a and b
    """
    r = np.random.rand()
    return a + r*(b - a)


def find_nearest(x_s, v_open):
    """
    finds the node in the tree closest to the sampled position
    :param x_s: sampled position tuple
    :param v_open: set of nodes that are still open
    :return: the node with a position closest to the sampled position
    """

    node_nearest = v_open[0]
    min_dist = get_distance(x_s, node_nearest.get_position())

    for node in v_open:
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
    return math.sqrt((x2[0] - x1[0])**2 + (x2[1] - x1[1])**2)


def steer(x_0, pos_sample, f, cfg, marker='g.'):
    """
    steers a current node at a sample node
    :param x_0: state of the near node
    :param pos_sample: sampled position tuple
    :param f: dynamics function
    :param cfg: configuration data
    :param marker: color for plotting
    :return: x_feasible: a feasible position
    """

    x_nearest = x_0
    u_nearest = None
    d_nearest = -1

    for i in range(0, cfg.get("samples")):
        x_new, u_new = f(x_0)                          # return a state
        d_new = get_distance(x_new.get_position(), pos_sample)   # state vs a position

        if cfg_ws["plot_full"]:
            plt.plot(x_new.get_x_position(), x_new.get_y_position(), marker)

        if d_new < d_nearest or d_nearest < 0:
            x_nearest = x_new
            u_nearest = u_new
            d_nearest = d_new

    return x_nearest, u_nearest


def find_nearby(x, v, cfg):
    """

    :param x: state object
    :param v: list of tree nodes
    :param cfg: configuration data
    :return: list of nodes within the specified radius
    """

    pos_x = x.get_position()
    r = cfg.get("radius")
    nodes_near = []

    for node in v:
        pos_node = node.get_position()
        distance = get_distance(pos_x, pos_node)

        if distance < r:
            nodes_near.append(node)

    return nodes_near


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
