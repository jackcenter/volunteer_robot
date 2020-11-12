# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from config import config
import dynopy.tools.initialize as init


def main():
    """


    :return:
    """
    # run("test.txt", 0.99, 5, 0.1, 1)


def run(file_ws, lamb, budget, t_limit, gamma, n_agents, plot=True, plot_full=False):
    """

    :param file_ws: string for the workspace parameters filename
    :param lamb: float [0, 1) for fusion preference - 0 is none, 0.99 is heavy fusion preference
    :param budget: int > 0 for number of steps the volunteer can take
    :param t_limit: float > 0.1 for volunteers planning time between steps
    :param gamma: float [0, 1] for time discount on rewards
    :param n_agents: int [1, 3] for number of dedicated agents in the simulation
    :param plot: boolean for whether or not to show the plot at the end
    :param plot_full: boolean for whether or not to show each step
    :return: dictionary of final results
    """
    ws = init.load_workspace(file_ws, os.path.dirname(__file__))
    volunteer = init.load_volunteer(config, lamb, budget, t_limit, gamma, plot_full)
    agents_dedicated = init.load_agents(n_agents, config)

    agents_all = agents_dedicated.copy()
    agents_all.append(volunteer)

    # load waypoints for all agents based on defaults set in the workspace
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

    # step the workspace

    if plot:
        plt.style.use('dark_background')

    for _ in range(0, budget):
        ws.step()

        if plot and not plot_full:
            print(" Current time step: {}\tof {}".format(ws.get_time_step(), budget), end='\r')
        #     print(" Current time step: {}\tof {}\n".format(ws.get_time_step(), budget))
        # else:

        if plot and plot_full:
            volunteer.plot_pdf()
            ws.plot()
            plt.show()

    if plot and not plot_full:      # keeps simulation from overwriting benchmarking output
        print()

    volunteer.plot_pdf()
    ws.plot()

    # TODO: could put this in volunteer and keep track of every step
    I_Data = {"I_Gained": volunteer.get_information_gained()}
    fused_total = 0
    for channel, novel in volunteer.information_novel.items():
        I_Data.update({channel + "_Novel": novel})
        fused = I_Data.get("I_Gained") - novel
        I_Data.update({channel + "_Fused": fused})

        fused_total += fused

    I_Data.update({"I_Fused": fused_total})

    return I_Data


if __name__ == "__main__":
    main()
