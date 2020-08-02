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
    robot2 = Robot("Clyde", "orange", [4, 9, -1.57])
    volunteer = Robot("Blinky", "red", [0, 5, 0], True)

    ws.add_agent(robot1)
    ws.add_agent(robot2)
    ws.add_agent(volunteer)

    ws.plot()
    plt.show()

    for i in range(9):
        cycle(ws)
        ws.plot()
        plt.show()


def cycle(ws):
    for robot in ws.agents:
        if not robot.get_volunteer_status():
            robot.step('forward')


if __name__ == "__main__":
    main()
