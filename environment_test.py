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
    robot1 = Robot("Inky", "cyan", [1, 0, 1.57])
    wp1 = [
        (9, 9),
        (1, 9)
    ]
    robot1.waypoints = wp1
    path = robot1.generate_path(0)
    print(path)

    robot2 = Robot("Clyde", "orange", [4, 9, -1.57])
    wp2 = [
        (4, 9),
        (4, 0)
    ]

    volunteer = Robot("Blinky", "red", [0, 5, 0], True)

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
        # plt.show()


def cycle(ws):
    for robot in ws.agents:
        if not robot.get_volunteer_status():
            robot.step('forward')


if __name__ == "__main__":
    main()
