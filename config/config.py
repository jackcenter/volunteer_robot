# !/usr/bin/env python
# -*- coding: utf-8 -*-


def get_parameters():
    cfg = {
        "plot_full": False,     # plot troubleshooting information
    }

    return cfg


def get_workspace_parameters():
    cfg = {
        "x_mean": 10,
        "x_var": 4,
        "y_mean": 13,
        "y_var": 4
    }

    return cfg


def load_agent_parameters(name):
    if name == "Blinky":
        cfg = {
            "color": "red",
            "budget": 5,  # distance volunteer can travel
            "step_size": 1,  # distance traveled each time step
            "radius": 1.2,  # radius to search for node expansion in
            "t_limit": .1,  # expansion time limit
            "samples": 16,  # number of control inputs to sample
            "gamma": 0.85,  # chance of detection if target is in cell
            "lambda": 0.99,        # reward preference coefficient (how important is fusion)
            "home": (10.5, 10.5),  # charging station position
            "fusion_range": 2   # max distance agent can communicate
        }

    elif name == "Pinky":
        cfg = {
            "color": "lightcoral",
            "budget": 30,  # distance volunteer can travel
            "step_size": 1,  # distance traveled each time step
            "radius": 1.2,  # radius to search for node expansion in
            "t_limit": .5,  # expansion time limit
            "samples": 16,  # number of control inputs to sample
            "gamma": 0.85,  # chance of detection if target is in cell
            "lambda": 0,  # reward preference coefficient (how important is fusion)
            "home": (10.5, 10.5),  # charging station position
            "fusion_range": 3   # max distance agent can communicate
        }

    elif name == "Inky":
        cfg = {
            "color": "cyan",
            "step_size": .25,  # distance traveled each time step
            "gamma": 0.85,  # chance of detection if target is in cell
            "fusion_range": 3  # max distance agent can communicate
        }

    elif name == "Clyde":
        cfg = {
            "color": "orange",
            "step_size": .25,  # distance traveled each time step
            "gamma": 0.85,  # chance of detection if target is in cell
            "fusion_range": 3  # max distance agent can communicate
        }

    else:
        cfg = {
            "color": "k",
            "budget": 20,  # distance volunteer can travel
            "step_size": 1,  # distance traveled each time step
            "radius": 1.2,  # radius to search for node expansion in
            "t_limit": 0.1,  # expansion time limit
            "samples": 16,  # number of control inputs to sample
            "gamma": 0.85,  # chance of detection if target is in cell
            "fusion_range": 2  # max distance agent can communicate
        }

    return cfg
