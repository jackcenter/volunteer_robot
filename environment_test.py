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
# TODO: set seed for samples and try to get side by side of pure RIG vs Fusion aware RIG


def main():
    boundary = [
        (0, 0),
        (20, 0),
        (20, 20),
        (0, 20)
    ]

    ws = Workspace(boundary, config.get_workspace_parameters())
    ws.generate_initial_distribution(multi=False)

    cfg_volunteer = config.load_agent_parameters("Blinky")
    # ROBOT 1 =====================================================
    wp1 = [
        # (7.5, 19.5)

        (7.5, 12.5),
        (5.5, 12.5),
        (5.5, 7.5)
    ]

    # robot1 = LineFollower2D("Inky", State_2D(wp1[0][0], wp1[0][1]))
    robot1 = LineFollower2D("Inky", State_2D(7.5, 7.5))
    # robot1 = LineFollower2D("Inky", State_2D(10.5, 2.5))
    robot1.start(ws)
    robot1.load_waypoints(wp1, cfg.get("budget"))
    ws.add_agent(robot1)

    # ROBOT 2 =====================================================
    wp2 = [
        # (13.5, 19.5)

        (13.5, 12.5),
        (15.5, 12.5),
        (15.5, 7.5)
    ]
    # robot2 = LineFollower2D("Clyde", State_2D(wp2[0][0], wp2[0][1]))
    robot2 = LineFollower2D("Clyde", State_2D(13.5, 7.5))
    robot2.start(ws)
    robot2.load_waypoints(wp2, cfg.get("budget"))
    ws.add_agent(robot2)

    # ROBOT 3 =====================================================
    # wp3 = [
    #     # (10.5, 19.5)
    #     # (13.5, 12.5),
    #     # (15.5, 12.5),
    #     # (15.5, 7.5)
    # ]
    # robot3 = LineFollower2D("Pinky", State_2D(17.5, 17.5))
    # robot3.start(ws)
    # robot3.load_waypoints(wp3, cfg.get("budget"))
    # ws.add_agent(robot3)

    # VOLUNTEER ===================================================
    volunteer = Volunteer2D("Blinky", State_2D(10.5, 10.5), True)
    volunteer.start(ws)
    ws.add_agent(volunteer)
    volunteer.set_c_space()
    volunteer.initialize_channels(ws.get_agents())

    plt.style.use('dark_background')
    for i in range(config.load_agent_parameters("Blinky").get("budget")):
        cycle(ws)
        if volunteer.plot_full:
            print("Cost: {}\n".format(volunteer.path[0].get_cost()))
            volunteer.plot_pdf()
            ws.plot()
            # print_nodes_with_reward(volunteer.get_tree()[0])
            circle = volunteer.get_budget_radius_object()
            axes = plt.gca()
            axes.add_artist(circle)
            plt.show()

    volunteer.plot_pdf()
    ws.plot()
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
