# !/usr/bin/env python
# -*- coding: utf-8 -*-


def get_parameters():
    cfg = {
        "budget": 20,           # distance volunteer can travel
        "step_size": 1,         # distance traveled each time step
        "radius": 1.2,          # radius to search for node expansion in
        "cycles": 20,           # number of times to run expansion
        "samples": 16,          # number of control inputs to sample
        "plot_full": False,     # plot troubleshooting information
        "gamma": 0.85           # chance of detection if target is in cell
    }

    return cfg
