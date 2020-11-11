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


def run(file_ws, lamb, budget, t_limit, gamma, plot=True, plot_full=False):
    ws = init.load_workspace(file_ws, os.path.dirname(__file__))
    volunteer = init.load_volunteer(config, lamb, budget, t_limit, gamma, plot_full)
    agents_dedicated = init.load_agents(3, config)

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

        if not plot_full:
            print(" Current time step: {}\tof {}".format(ws.get_time_step(), budget), end='\r')
        #     print(" Current time step: {}\tof {}\n".format(ws.get_time_step(), budget))
        # else:


        if plot and plot_full:
            volunteer.plot_pdf()
            ws.plot()
            plt.show()

    print('\n')

    volunteer.plot_pdf()
    ws.plot()

    # TODO: could put this in volunteer and keep track of every step
    I_Data = {"I_Gained": volunteer.get_information_gained()}
    novel_total = 0
    for channel, novel in volunteer.information_novel.items():
        novel_total += novel

        I_Data.update({channel + "_Novel": novel})

        fused = I_Data.get("I_Gained") - novel
        I_Data.update({channel + "_Fused": fused})

    return I_Data


if __name__ == "__main__":
    main()
