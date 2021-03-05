import math
from time import process_time
import matplotlib.pyplot as plt
import numpy as np
from dynopy.data_objects.node_traj import Node
from dynopy.motion_planning.tree_analysis import plot_tree
from config.config import get_parameters
from tree_analysis import plot_tree

cfg_ws = get_parameters()


def update_information(V, E, epsilon_0, cfg, I_0, fused):
    """

    :param V: list of nodes
    :param E: list of edges
    :param epsilon_0: current pdf
    :param cfg: configuration of agent
    :param I_0: information gained up to this point
    :param fused: dict of information fused so far {channel: information}
    :return: list of nodes with updated information values
    """

    # TODO: could probably save time here by not going through the full tree, just new nodes

    ol = [V[0]]     # open list
    # TODO: create empty branch list node
    bl = []         # branch list for visited nodes
    cl = []         # closed list

    # Lists aligned with the branch element to update pdf as agent travels through it
    epsilon_list = [epsilon_0]          # last element indicates current pdf
    reward_list = [V[0].get_reward()]   # last element indicates current reward
    fused_list = [fused]                # last element indicates current fusion

    time_0 = V[0].get_time              # indicates the time step

    while ol:
        node = ol[-1]

        epsilon = epsilon_list[-1]
        r_0 = reward_list[-1]
        fusion = fused_list[-1]

        if node not in bl:      # first time this node has been visited

            # update information
            if bl:
                I_gained = cfg.get("p_d")*get_information_available(epsilon, node)
                I_parent = bl[-1].get_information()
                node.set_information(I_gained + I_parent)

                # update fusion

        neighbors_all = find_neighbors(E, node)
        neighbors_open = list(set(neighbors_all).difference(cl))

        if neighbors_open:      # there are nodes to expand to
            pass

        elif node in bl:        # just returned to a node that has been fully explored
            ol.pop()
            bl.pop()
            cl.append(node)
            epsilon_list.pop()
            reward_list.pop()
            fused_list.pop()

        else:                           # this is a leaf
            ol.pop()
            cl.append(node)


def RIG_tree(V, E, X_all, X_free, epsilon, x_0, cfg, f_dynamics, channel_list):
    """

    :param V: node list for a prebuilt tree
    :param E: edge list for a prebuilt tree
    :param X_all: workspace
    :param X_free: free space
    :param epsilon: environment
    :param x_0: initial state
    :param cfg: dictionary of necessary values: step size, budget, nearest neighbor radius, input samples, and
    time limit for expansion
    :param f_dynamics: dynamics function
    :param channel_list: starting fusion
    :return: a list of nodes and edges
    """

    t_limit = cfg.get("t_limit")

    if not V:
        V, E = initialize_graph(x_0, epsilon, channel_list)

    t_0 = process_time()
    while process_time() - t_0 < t_limit:
        # Expand the tree while time remains
        pos_sample = sample_position(X_all, cfg)
        n_nearest = find_nearest(pos_sample, V)
        x_feasible, _ = steer(n_nearest.get_state(), pos_sample, f_dynamics, cfg, 'y.')
        n_near = find_nearby(x_feasible, V, cfg)

        r_best = None
        parent_best = None
        child_best = None

        for node in n_near:
            x_new, u_new = steer(node.get_state(), pos_sample, f_dynamics, cfg)

            c_new = evaluate_cost(node, cfg)
            i_new = node.get_information() + get_information_available(epsilon, x_new.get_position())
            k_new = node.get_time() + 1
            f_new = update_fusion(node, x_new, i_new, channel_list, cfg)

            penalty = evaluate_penalty(x_new, c_new, cfg)
            r_new = evaluate_reward(i_new, f_new, k_new, penalty, cfg)

            if not r_best or r_new > r_best:
                parent_best = node
                r_old = parent_best.get_reward()
                child_best = Node(x_new, u_new, c_new, i_new, k_new, r_new + r_old, f_new)
                r_best = r_new

            if cfg_ws.get("plot_full"):
                plot_tree(E)
                plot_expansion(pos_sample, x_feasible.get_position(), node.get_position(), x_new.get_position())

        if parent_best and child_best:
            V.append(child_best)
            E.append((parent_best, child_best))

        # for _, wp in channel_list.items():
        #     x, y = wp[0].get_position()
        #     plt.plot(x, y, 'bx')
        #
        # plot_tree(E)
        # plt.axis("equal")
        # plt.show()

    return V, E


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

    return v, e


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


def evaluate_cost(n_k0, cfg):

    c = n_k0.get_cost() + cfg.get("step_size")
    return c


def evaluate_penalty(x_k1, cost, cfg):
    # TODO: fix this
    x_home = cfg.get("home")
    budget = cfg.get("budget")

    life = budget - cost

    range_now = get_distance(x_k1.get_position(), x_home)
    range_max = life

    if range_max - range_now < cfg.get("step_size"):
        # within a step of being out of range of home
        p = (range_max - range_now)**2
    else:
        p = 0

    return p


def update_fusion(node, x_new, i_new, channel_list, cfg):
    """

    :param node: parent node
    :param x_new: fusion position
    :param i_new: information fused and the fusion position
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


def evaluate_reward(i_new, f_new, k, penalty, cfg):
    lamb = cfg.get("lambda")
    gamma = cfg.get("gamma")

    i_novel = 0
    n = len(f_new)

    for agent, fused in f_new.items():
        i_novel += i_new - fused

    r = gamma**k*(i_new - lamb / n * i_novel)       # fusion reward
    r -= penalty                                    # too far from home penalty

    if r < -1:
        r = -1

    r += 1                                          # movement reward

    return r


def get_information_available(epsilon, pos):
    x = math.trunc(pos[0])
    y = math.trunc(pos[1])

    try:
        i_available = epsilon[y][x]
    except IndexError:
        i_available = 0

    return i_available


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


def plot_expansion(pos_sample, pos_feasible, node_pos, pos_new):
    """
    used to troubleshoot issues with the tree expansion
    :return:
    """
    plt.plot(pos_sample[0], pos_sample[1], 'bx')
    plt.plot(pos_feasible[0], pos_feasible[1], 'yo')
    plt.plot(node_pos[0], node_pos[1], 'rx')
    plt.plot(pos_new[0], pos_new[1], 'r.')
    plt.axis('equal')
    plt.show()



