# !/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import matplotlib.pyplot as plt
from config import config
from dynopy.motion_planning.RIG_tree_R_based import RIG_tree
import dynopy.tools.initialize as init

cfg = config.get_parameters()


def main():
    run("workspace_sandbox.txt", 0.99, 5, 0.1, 1, 1)


def run(file_ws, lamb, budget, t_limit, gamma, n_agents, plot=True, plot_full=False):
    ws = init.load_workspace(file_ws, os.path.dirname(__file__))
    volunteer = init.load_volunteer(config, lamb, budget, t_limit, gamma, plot_full)
    agents_dedicated = init.load_agents(n_agents, config)

    agents_all = agents_dedicated.copy()
    agents_all.append(volunteer)

    for agent in agents_all:
        n = config.get_cfg_number(agent.get_name())
        waypoints = ws.get_default_waypoints(n)
        agent.set_state(waypoints[0])
        agent.start(ws)
        agent.load_waypoints(waypoints, budget)
        ws.add_agent(agent)

    # set additional volunteer parameters
    volunteer.set_c_space()
    volunteer.initialize_channels(ws.get_agents())

    if plot:
        plt.style.use('dark_background')

        for agent in ws.agents:
            if agent.name != "Blinky":
                agent.step()
            else:
                V, E, V_closed = RIG_tree(agent.V, agent.E, agent.V_closed, agent.get_X_free(), agent.get_X_free(),
                                          agent.get_pdf(), agent.get_state(), agent.cfg, agent.sample_dynamics)
                agent.V = V
                agent.E = E
                agent.V_closed = V_closed

                agent.plot_tree(agent.E, 'blue')

        ws.time_step += 1


if __name__ == "__main__":
    main()
