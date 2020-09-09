import matplotlib.pyplot as plt
from RIG_tree import RIG_tree, plot_tree
from dynopy.workspace.workspace import Workspace
from dynopy.workspace.agents import Robot
from dynopy.data_objects.state import State_2D


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
    robot1 = Robot("Inky", "cyan", State_2D(1, 0))
    robot1.start(ws)

    wp1 = [
        (1, 0),
        (1, 9),
        (2, 9),

    ]

    robot1.load_waypoints(wp1)
    ws.add_agent(robot1)

    # ROBOT 2 =====================================================
    robot2 = Robot("Clyde", "orange", State_2D(6, 9))
    robot2.start(ws)
    wp2 = [
        (6, 9),
        (4, 9),
        (4, 0)
    ]
    robot2.load_waypoints(wp2)
    ws.add_agent(robot2)

    # VOLUNTEER ===================================================
    volunteer = Robot("Blinky", "red", State_2D(0.5, 5.5), True)
    volunteer.set_workspace(ws)
    volunteer.set_configuration_space()
    volunteer.set_initial_pdf()

    ws.add_agent(volunteer)
    print(volunteer.pdf)

    V, E = RIG_tree(1, 10, volunteer.get_X_free(), volunteer.get_X_free(), volunteer.get_pdf(), volunteer.get_position()
                    , 1.2)

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 10))
    # ws.plot()
    # plt.show()

    for i in range(2):
        cycle(ws)
        ws.plot()
        plot_tree(E)
        plt.show()


def cycle(ws):
    """
    Cycles forward one time step
    :param ws:
    :return:
    """
    ws.step()

    for robot in ws.agents:
        if not robot.get_volunteer_status():
            # print(robot.pdf)
            # print()

            robot.step()
            print([x.get_position() for x in robot.path_log])
            print(robot.i_gained)


if __name__ == "__main__":
    main()
