import matplotlib.pyplot as plt
from dynopy.workspace.workspace import Workspace
from dynopy.workspace.agents import Robot


def main():
    boundary = [
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10)
    ]

    ws = Workspace(boundary)
    ws.generate_grid()
    ws.generate_initial_distribution()

    # ROBOT 1 =====================================================
    robot1 = Robot("Inky", "cyan", [1, 0])
    robot1.start(ws)
    # robot1.set_workspace(ws)
    # robot1.set_map()
    # robot1.set_initial_pdf()
    # robot1.update_pdf()

    wp1 = [
        (1, 0),
        (1, 9),
        (2, 9),

    ]

    robot1.load_waypoints(wp1)

    # robot1.waypoints = wp1
    # robot1.generate_full_path()
    # robot1.generate_trajectory()

    ws.add_agent(robot1)

    # ROBOT 2 =====================================================
    robot2 = Robot("Clyde", "orange", [6, 9])
    # robot2.set_workspace(ws)
    # robot2.set_map()
    # robot2.set_initial_pdf()
    # robot2.update_pdf()
    robot2.start(ws)
    wp2 = [
        (6, 9),
        (4, 9),
        (4, 0)
    ]
    robot2.load_waypoints(wp2)
    # robot2.waypoints = wp2
    # robot2.generate_full_path()
    # robot2.generate_trajectory()

    ws.add_agent(robot2)

    # VOLUNTEER ===================================================
    volunteer = Robot("Blinky", "red", [0, 5], True)
    volunteer.set_workspace(ws)
    volunteer.set_initial_pdf()

    ws.add_agent(volunteer)

    print(robot1.path)
    print(robot1.trajectory)
    print(robot2.path)
    print(robot2.trajectory)

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 10))
    ws.plot()
    plt.show()

    for i in range(4):
        cycle(ws)
        ws.plot()
        plt.show()


def cycle(ws):
    ws.step()

    for robot in ws.agents:
        if not robot.get_volunteer_status():
            # print(robot.pdf)
            # print()

            robot.step()
            print(robot.path_log)
            print(robot.i_gained)


if __name__ == "__main__":
    main()
