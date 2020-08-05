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
    robot1 = Robot("Inky", "cyan", [1, 0])
    wp1 = [
        (1, 0),
        (1, 9)
    ]
    robot1.waypoints = wp1
    robot1.generate_straight_line_path(0)

    robot1.generate_trajectory()

    robot2 = Robot("Clyde", "orange", [4, 9])
    wp2 = [
        (6, 9),
        (4, 9),
        (4, 0)
    ]
    robot2.waypoints = wp2
    robot2.generate_straight_line_path(0)
    robot2.generate_trajectory()

    print(robot1.path)
    print(robot1.trajectory)
    print(robot2.path)
    print(robot2.trajectory)

    volunteer = Robot("Blinky", "red", [0, 5], True)

    ws.add_agent(robot1)
    ws.add_agent(robot2)
    ws.add_agent(volunteer)

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 10))
    ws.plot()
    plt.show()

    for i in range(2):
        cycle(ws)
        ws.plot()
        plt.show()


def cycle(ws):
    for robot in ws.agents:
        if not robot.get_volunteer_status():
            robot.step()
            print(robot.path_log)


if __name__ == "__main__":
    main()
