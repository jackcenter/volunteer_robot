# !/usr/bin/env python
# -*- coding: utf-8 -*-


def get_parameters():
    cfg = {
        "plot_full": False,     # plot troubleshooting information
        "lambda": .5            # reward preference coefficient (how important is fusion)
    }

    return cfg


def load_agent_parameters(name):
    if name == "Blinky":
        cfg = {
            "color": "red",
            "budget": 30,  # distance volunteer can travel
            "step_size": 1,  # distance traveled each time step
            "radius": 1.2,  # radius to search for node expansion in
            "t_limit": .3,  # expansion time limit
            "samples": 16,  # number of control inputs to sample
            "gamma": 0.85,  # chance of detection if target is in cell
            "home": (0.5, 5.5)  # charging station position
        }

    elif name == "Inky":
        cfg = {
            "color": "cyan",
            "step_size": 1,  # distance traveled each time step
            "gamma": 0.85  # chance of detection if target is in cell
        }

    elif name == "Clyde":
        cfg = {
            "color": "orange",
            "step_size": 1,  # distance traveled each time step
            "gamma": 0.85  # chance of detection if target is in cell
        }

    else:
        cfg = {
            "color": "k",
            "budget": 20,  # distance volunteer can travel
            "step_size": 1,  # distance traveled each time step
            "radius": 1.2,  # radius to search for node expansion in
            "t_limit": 0.1,  # expansion time limit
            "samples": 16,  # number of control inputs to sample
            "gamma": 0.85  # chance of detection if target is in cell
        }

    return cfg
