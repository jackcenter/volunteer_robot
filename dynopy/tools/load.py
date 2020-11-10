# !/usr/bin/env python
# -*- coding: utf-8 -*-

from dynopy.workspace.workspace import Workspace
from dynopy.agents.lineFollwer2D import LineFollower2D
from dynopy.agents.volunteer2D import Volunteer2D


def workspace(file):
    bound, params_e = read_workspace_file(file)
    ws = Workspace(bound, params_e)
    ws.generate_initial_distribution()
    # distribution
    # obstacles - not implemented yet
    return ws


def read_workspace_file(file):
    # returns the boundary and a distribution
    return 0, 0


def volunteer(cfg, home, lamb=0.99, budget=60, t_limit=0.1, gamma=1, name="Blinky"):
    """

    :param cfg: file with dictionary of default parameters
    :param home: tuple of x, y position for the volunteers starting position.
    :param lamb: float [0,1) for fusion preference
    :param budget: int for maximum steps volunteer can take
    :param t_limit: float greater than or equal to 0.1 for time taken to expand tree
    :param gamma: float [0, 1] for discount on future rewards
    :param name: default parameters to use
    :return:
    """

    if lamb < 0:
        lamb = 0
        print("Warning: lambda set out of range [0.0, 0.99), setting to 0")
    elif lamb >= 1:
        lamb = 0.99
        print("Warning: lambda set out of range [0.0, 0.99), setting to 0.99")

    if t_limit < 0.1:
        t_limit = 0.1
        print("Warning: t_limit set to less than 0.1, setting to 0.1")

    if gamma < 0:
        gamma = 0.0
        print("Warning: gamma set out of range [0.0, 1.0], setting to 0")
    elif gamma > 1:
        gamma = 1.0
        print("Warning: gamma set out of range [0.0, 1.0], setting to 1.0")

    cfg_volunteer = cfg.load_agent_parameters(name)

    cfg_volunteer.update({"home": home})
    cfg_volunteer.update({"lambda": lamb})
    cfg_volunteer.update({"budget": budget})
    cfg_volunteer.update({"t_limit": t_limit})
    cfg_volunteer.update({"k_discount": gamma})

    robot = Volunteer2D(name, home, cfg, False)

    return robot


def agents(file, budget):
    # loads dedicated agents with named configurations with paths
    pass
