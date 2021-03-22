import math
from time import process_time
import matplotlib.pyplot as plt
import numpy as np
from dynopy.data_objects.node_traj import Node
from config.config import get_parameters

cfg_ws = get_parameters()


def IRRT_tree(V, E, V_closed, X_all, X_free, epsilon, x_0, x_g, cfg, f_dynamics, channel_list, b):

    t_limit = cfg.get("t_limit")

    if not V:
        V, E, V_closed = initialize_graph(x_0, epsilon, channel_list)

    t_0 = process_time()
    # j = 100
    # for _ in range(0, j):
    while process_time() - t_0 < t_limit:

        if not set(V).difference(V_closed):
            # no open nodes
            break

        # Expand the tree while time remains
        pos_sample = sample_position(X_all, x_g)
        n_nearest = find_nearest(pos_sample, list(set(V).difference(V_closed)))
        x_new, u_new = steer(n_nearest.get_state(), pos_sample, f_dynamics, cfg, 'y.')
        # TODO: add in multi step

        n_root = n_nearest
        c_new = n_root.get_cost() + cfg.get("step_size")
        i_new = n_root.get_information() + get_information_available(epsilon, x_new.get_position())
        k_new = n_root.get_time() + 1
        f_new = set_fusion(n_root, x_new, i_new, channel_list, cfg)
        n_new = Node(x_new, u_new, c_new, i_new, k_new, i_new, f_new)

        if get_distance(n_new.get_position(), x_g) < cfg.get("fusion_range"):
            V_closed.append(n_new)
            n_new.set_goal_status(True)

        elif c_new > b:
            V_closed.append(n_new)

        if n_root and n_new and not twin_node(E, n_root, n_new, cfg):
            V.append(n_new)
            E.append((n_root, n_new))

    return V, E, V_closed


def initialize_graph(x_0, epsilon, channel_list):
    """
    creates the initial graph if none has been previously computed.

    :param x_0: initial state
    :param epsilon: initial distribution
    :param channel_list:
    :return:
    """
    i_init = initial_information(x_0.get_position(), epsilon)  # Initial node information
    c_init = 0                                  # Initial node cost
    r_init = 0
    k_init = 0
    f_init = {}

    for agent in channel_list.keys():
        f_init.update({agent: 0})

    n_0 = Node(x_0, None, c_init, i_init, k_init, r_init, f_init)
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


def sample_position(x_all, x_goal):
    """
    samples the configuration space for a random node position
    :param x_all:
    :param x_goal
    :return:
    """
    v_sample = np.random.rand()
    if v_sample < 0.05:
        x_sample = x_goal

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


def get_information_available(epsilon, pos):
    x = math.trunc(pos[0])
    y = math.trunc(pos[1])

    try:
        i_available = epsilon[y][x]
    except IndexError:
        i_available = 0

    return i_available


def set_fusion(node, x_new, i_new, channel_list, cfg):
    """
    copies the previous node's fusion list, checks if there has been any new fusion, and update the appropriate channels

    :param node: parent node
    :param x_new: fusion position
    :param i_new: information gained to this point
    :param channel_list:
    :param cfg:
    :return:
    """

    f_new = node.get_fusion().copy()
    fusion_list = check_for_fusion(x_new, channel_list, cfg)

    for agent in fusion_list:
        f_new.update({agent: i_new})

    return f_new


def check_for_fusion(state, channel_list, cfg):

    fusion_range = cfg.get("fusion_range")
    fusion_list = []

    for agent, path in channel_list.items():
        for node in path:
            if node.compare_time(state) and node.get_distance_from(state) < fusion_range:
                fusion_list.append(agent)
                break

    return fusion_list


def pick_irrt_path(v, e):
    """
    picks a path simply based on the highest information in a path. Defaults to paths that reached the goal state
    :param v: list of nodes
    :param e: list of directed node tuples
    :return: list of nodes that represent a path
    """

    goal_nodes = []
    goal_node = False

    for n in v:
        # check for any nodes that reached the goal
        if n.get_goal_status():
            goal_nodes.append(n)
            goal_node = True
            # print("Pos: {}\nInf: {}\n".format(n.get_position(), n.get_information()))

    if goal_node:

        max_node = None

        for n in goal_nodes:
            if not max_node or max_node.get_information() < n.get_information():
                max_node = n

    else:
        max_node = max(v, key=lambda x: x.i) # finds node with most information

    path = [max_node]

    searching = True

    while searching:
        searching = False
        for root, leaf in e:
            if leaf == path[-1]:
                path.append(root)
                searching = True
                break

    return path


def twin_node(E, n0, n1, cfg):

    twin = False

    for parent, child in E:

        if n0 == parent:
            dist = get_distance(child.get_position(), n1.get_position())

            if dist < cfg.get("epsilon"):
                twin = True
                break

    return twin
