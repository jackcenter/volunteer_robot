# !/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from config import config
from dynopy.workspace.workspace import Workspace
from dynopy.agents.lineFollwer2D import LineFollower2D
from dynopy.agents.volunteer2D import Volunteer2D
from dynopy.data_objects.state import State_2D
from tree_analysis import plot_tree

cfg = config.get_parameters()


def main():
    boundary = [
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10)
    ]

    ws = Workspace(boundary)
    # ws.generate_grid()
    ws.generate_initial_distribution()

    # ROBOT 1 =====================================================
    robot1 = LineFollower2D("Inky", State_2D(1.5, 0.5))
    robot1.start(ws)

    wp1 = [
        (1.5, 0.5),
        (1.5, 9.5),
        (2.5, 9.5),

    ]

    robot1.load_waypoints(wp1)
    ws.add_agent(robot1)

    # ROBOT 2 =====================================================
    robot2 = LineFollower2D("Clyde", State_2D(6.5, 9.5))
    robot2.start(ws)
    wp2 = [
        (6.5, 9.5),
        (4.5, 9.5),
        (4.5, 0.5)
    ]
    robot2.load_waypoints(wp2)
    ws.add_agent(robot2)

    # VOLUNTEER ===================================================
    volunteer = Volunteer2D("Blinky", State_2D(0.5, 5.5))
    volunteer.start(ws)
    volunteer.set_c_space()

    ws.add_agent(volunteer)
    print(volunteer.pdf)

    plt.style.use('dark_background')
    V, E = volunteer.execute_planning_cycle()
    # update_information(V, E, volunteer.pdf)
    # identify_fusion_nodes(V, robot1.get_path(), robot1.name, 2)
    # identify_fusion_nodes(V, robot2.get_path(), robot2.name, 2)
    # volunteer.path = pick_path(V, E)    #

    # plot_tree(E, 'blue')
    # V, E = prune_step(V, E, volunteer.get_path())

    #   Prune passed nodes
    for i in range(1):
        plot_tree(E, 'lightcoral')
        cycle(ws)
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
