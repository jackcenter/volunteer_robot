# !/usr/bin/env python
# -*- coding: utf-8 -*-

configurations = {
    "Blinky": 0,
    "Inky": 1,
    "Clyde": 2,
    "Pinky": 3
}


def get_parameters():
    cfg = {
        "plot_full": False,     # plot troubleshooting information
    }

    return cfg


def get_workspace_parameters():
    cfg = [
        {"x_mean": 15, "x_var": 4, "y_mean": 10, "y_var": 4},
        {"x_mean": 5, "x_var": 2, "y_mean": 5, "y_var": 2},
        {"x_mean": 5, "x_var": 2, "y_mean": 15, "y_var": 2}
    ]

    return cfg


def load_agent_parameters(name):
    if name == "Blinky":
        cfg = {
            "color": "red",
            "budget": 50,           # distance volunteer can travel
            "step_size": 1,         # distance traveled each time step
            "radius": 1.9,          # radius to search for node expansion in
            "t_limit": .1,           # expansion time limit
            "gamma": 1,        # reward discount factor
            "samples": 16,          # number of control inputs to sample
            "p_d": 0.80,          # chance of detection if target is in cell
            "lambda": 0.99,         # reward preference coefficient (how important is fusion)
            "home": (10.5, 10.5),   # charging station position
            "fusion_range": 2,       # max distance agent can communicate
            "dynamics_range": ([-1, 1], [1, 1],),
            "epsilon": .25            # min distance between children
        }

    elif name == "Pinky":
        cfg = {
            "color": "pink",
            "step_size": .25,  # distance traveled each time step
            "p_d": 0.8,  # chance of detection if target is in cell
            "fusion_range": 100  # max distance agent can communicate
        }

    elif name == "Inky":
        cfg = {
            "color": "cyan",
            "step_size": .25,  # distance traveled each time step
            "p_d": 0.8,  # chance of detection if target is in cell
            "fusion_range": 100  # max distance agent can communicate
        }

    elif name == "Clyde":
        cfg = {
            "color": "orange",
            "step_size": .25,  # distance traveled each time step
            "p_d": 0.85,  # chance of detection if target is in cell
            "fusion_range": 100  # max distance agent can communicate
        }

    else:
        cfg = {
            "color": "k",
            "budget": 20,  # distance volunteer can travel
            "step_size": 1,  # distance traveled each time step
            "radius": 1.2,  # radius to search for node expansion in
            "t_limit": 0.1,  # expansion time limit
            "samples": 16,  # number of control inputs to sample
            "p_d": 0.85,  # chance of detection if target is in cell
            "fusion_range": 100  # max distance agent can communicate
        }

    return cfg


def get_cfg_names(volunteer=True):
    """
    Returns a list of possible configuration names in the file
    :param volunteer: boolean to determine whether volunteer configurations should be returned
    :return: list of configuration names
    """

    names = list(configurations.keys())
            # ["Blinky", "Inky", "Clyde", "Pinky"]
    if not volunteer:
        names = [x for x in names if x != "Blinky"]

    return names


def get_cfg_number(name):
    return configurations.get(name)
