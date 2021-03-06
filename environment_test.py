# !/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from config import config
from dynopy.workspace.workspace import Workspace
from dynopy.agents.lineFollwer2D import LineFollower2D
from dynopy.agents.volunteer2D import Volunteer2D
from dynopy.data_objects.state import State_2D
from dynopy.motion_planning.tree_analysis import print_nodes_with_reward, print_leafs_with_reward

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
    ws.generate_initial_distribution()
    cfg_volunteer = config.load_agent_parameters("Blinky")


    # ROBOT 1 =====================================================
    wp1 = [
        # (7.5, 19.5)

        # (7.5, 12.5),
        # (5.5, 12.5),
        # (5.5, 7.5)
    ]


    robot1 = LineFollower2D("Inky", State_2D(2.5, 2.5))
    robot1.start(ws)
    robot1.load_waypoints(wp1, cfg_volunteer.get("budget"))
    ws.add_agent(robot1)

    # ROBOT 2 =====================================================
    wp2 = [
        # (13.5, 19.5)

        # (13.5, 12.5),
        # (15.5, 12.5),
        # (15.5, 7.5)
    ]
    robot2 = LineFollower2D("Clyde", State_2D(2.5, 17.5))
    robot2.start(ws)
    robot2.load_waypoints(wp2, cfg_volunteer.get("budget"))
    ws.add_agent(robot2)

    # ROBOT 3 =====================================================
    wp3 = [
        # (10.5, 7.5)

        # (13.5, 12.5),
        # (15.5, 12.5),
        # (15.5, 7.5)
    ]
    robot3 = LineFollower2D("Pinky", State_2D(10.5, 2.5))
    robot3.start(ws)
    robot3.load_waypoints(wp3, cfg_volunteer.get("budget"))
    # ws.add_agent(robot3)

    # VOLUNTEER ===================================================
    volunteer = Volunteer2D("Blinky", cfg_volunteer, State_2D(10.5, 10.5), False)
    volunteer.start(ws)
    ws.add_agent(volunteer)
    volunteer.set_c_space()
    volunteer.initialize_channels(ws.get_agents())

    # Simulation ===================================================
    plt.style.use('dark_background')
    for i in range(config.load_agent_parameters("Blinky").get("budget")):
        ws.step()
        if volunteer.plot_full:
            print(len(volunteer.path))
            # print("Cost: {}\n".format(volunteer.path[0].get_cost()))
            volunteer.plot_pdf()
            ws.plot()
            # print_nodes_with_reward(volunteer.get_tree()[0])
            print_leafs_with_reward(volunteer.get_nodes(), volunteer.get_edges())
            circle = volunteer.get_budget_radius_object()
            axes = plt.gca()
            axes.add_artist(circle)
            plt.show()

    volunteer.plot_pdf()
    ws.plot()
    plt.show()


if __name__ == "__main__":
    main()
