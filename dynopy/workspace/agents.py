import matplotlib.pyplot as plt
import numpy as np


class Robot:
    def __init__(self, name: str, color: str, state: list, volunteer=False):
        """

        :param name:
        :param color:
        :param state: [x position, y_position]
        """
        self.name = name
        self.color = color
        self.state = state
        self.volunteer = volunteer

        self.waypoints = []         # list of points the agent needs to reach
        self.path = []              # list of 2D positions
        self.path_log = []
        self.trajectory = []        # last element, [-1], is the next action to take
        self.trajectory_log = []    # stores actions taken in order, ie [0] is the first action

        self.pD = 0.85              # probability of detection
        self._pD = 1 - self.pD      # probability of no detection

        self.workspace = None       # current workspace
        self.map = None             # list of coordinates corresponding to the map
        self.pdf = None             # current probability distribution

    def plot(self):
        x = self.state[0] + 0.5
        y = self.state[1] + 0.5
        plt.plot(x, y, 'x', color=self.color)

    def plot_visited_cells(self):
        for pos in self.path_log:
            x = pos[0] + 0.5
            y = pos[1] + 0.5
            plt.plot(x, y, 'o', color=self.color, mfc='none')

    def plot_path(self):
        for pos in self.path:
            x = pos[0] + 0.5
            y = pos[1] + 0.5
            plt.plot(x, y, '.', color=self.color)

    def get_volunteer_status(self):
        return self.volunteer

    def set_workspace(self, ws):
        self.workspace = ws

    def set_map(self):
        self.map = self.workspace.map

    def set_initial_pdf(self):
        self.pdf = self.workspace.pXY.copy()

    def generate_full_path(self):
        pass

    def generate_straight_line_path(self, w_0):
        """
        Could use any type of path planner here. This is just a straight line style implementation
        Assume waypoint 1 is the starting location
        :return:
        """

        # TODO: Need to fix this to be more generic so the full path can be generated
        start = self.waypoints[w_0]
        goal = self.waypoints[w_0 + 1]
        path = [start]

        # --- Straight line assumption ---
        x = start[0]
        y = start[1]
        goal_found = False

        # North
        if start[1] < goal[1]:
            while not goal_found:
                y += 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # East
        elif start[0] < goal[0]:
            while not goal_found:
                x += 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # South
        elif start[1] > goal[1]:
            while not goal_found:
                y -= 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # West
        elif start[0] > goal[0]:
            while not goal_found:
                x -= 1
                path.append((x, y))

                if (x, y) == goal:
                    goal_found = True
        # Error
        else:
            print("ERROR: Something's wrong with the start or goal position for {}".format(self.name))

        path.reverse()
        self.path = path
        self.path_log.append(self.path.pop())    # agent is already at first point in the path

    def generate_trajectory(self):
        traj = []
        path = self.path.copy()
        w_1 = path.pop()

        while path:
            w_0 = w_1
            w_1 = path.pop()
            traj.append(self.checkCellDirection(w_0, w_1))

        traj.reverse()
        self.trajectory = traj

    def update_pdf(self):
        """
        updated probability target is in current grid cell for the time step
        :return:
        """
        x = self.state[0]
        y = self.state[1]

        self.pdf[x][y] *= self._pD
        self.pdf = self.pdf/np.sum(self.pdf)      # normalize

    def step(self):
        """
        moves the agent in the commanded direction
        :param
        :return:
        """
        action = self.trajectory.pop()

        if action == 'north':
            self.state[1] += 1
        elif action == 'east':
            self.state[0] += 1
        elif action == 'south':
            self.state[1] -= 1
        elif action == 'west':
            self.state[0] -= 1
        else:
            print("ERROR: robot action not understood. Needs to be north, east, south, or west")
            return

        self.trajectory_log.append(action)
        self.path_log.append(self.path.pop())
        self.update_pdf()

    @staticmethod
    def checkCellDirection(a, b):
        if a[0] == b[0] and a[1] < b[1]:
            return "north"
        elif a[0] < b[0] and a[1] == b[1]:
            return "east"
        elif a[0] == b[0] and a[1] > b[1]:
            return "south"
        elif a[0] > b[0] and a[1] == b[1]:
            return "west"
        else:
            print("ERROR: couldn't determine the orientation of these two cells: {}, {}".format(a, b))
