# !/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from config import config
from dynopy.workspace.workspace import Workspace
from dynopy.agents.lineFollwer2D import LineFollower2D
from dynopy.agents.volunteer2D import Volunteer2D
from dynopy.data_objects.state import State_2D
from dynopy.motion_planning.tree_analysis import print_nodes_with_reward

cfg = config.get_parameters()

# TODO: check that the path_log and state_log are updating correctly
# TODO: use a more interesting pdf
# TODO: look at volunteer start up
# TODO: check out those negative rewards, not sure why that would happen
# TODO: agent is jumping path locations, need to figure out why
# TODO: set seed for samples and try to get side by side of pure RIG vs Fusion aware RIG


def main():
    boundary = [
        (0, 0),
        (20, 0),
        (20, 20),
        (0, 20)
    ]

    ws = Workspace(boundary)
    ws.generate_initial_distribution()

    # ROBOT 1 =====================================================
    robot1 = LineFollower2D("Inky", State_2D(5.5, 0.5))
    robot1.start(ws)

    wp1 = [
        (5.5, 0.5),
        (5.5, 19.5),
        (7.5, 19.5),
        (7.5, 0.5)
    ]

    robot1.load_waypoints(wp1)
    ws.add_agent(robot1)

    # ROBOT 2 =====================================================
    robot2 = LineFollower2D("Clyde", State_2D(10.5, 19.5))
    robot2.start(ws)
    wp2 = [
        (10.5, 19.5),
        (10.5, 0.5),
        (12.5, 0.5),
        (12.5, 19.5)
    ]
    robot2.load_waypoints(wp2)
    ws.add_agent(robot2)

    # VOLUNTEER ===================================================
    volunteer = Volunteer2D("Blinky", State_2D(0.5, 5.5))
    volunteer.start(ws)
    ws.add_agent(volunteer)
    volunteer.set_c_space()
    volunteer.initialize_channels(ws.get_agents())
    print(volunteer.channel_list)
    print(volunteer.pdf)

    plt.style.use('dark_background')
    for i in range(config.load_agent_parameters("Blinky")["budget"]):
        cycle(ws)
        volunteer.plot_pdf()
        ws.plot()

        print_nodes_with_reward(volunteer.get_tree()[0])
        plt.show()


def cycle(ws):
    """
    Cycles forward one time step
    :param ws:
    :return:
    """
    ws.step()

    for robot in ws.agents:
        robot.step()
        # print([x.get_position() for x in robot.path_log])
        # print(robot.i_gained)


if __name__ == "__main__":
    main()
