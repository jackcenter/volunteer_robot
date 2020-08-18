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
        self.path_log = [((self.state[0], self.state[1]), 0)]
        self.trajectory = []        # last element, [-1], is the next action to take
        self.trajectory_log = []    # stores actions taken in order, ie [0] is the first action

        self.pD = 0.85              # probability of detection
        self._pD = 1 - self.pD      # probability of no detection

        self.workspace = None       # current workspace
        self.map = None             # list of coordinates corresponding to the map
        self.pdf = None             # current probability distribution
        self.i_gained = []          # information gained along path

    def plot(self):
        x = self.state[0] + 0.5
        y = self.state[1] + 0.5
        plt.plot(x, y, 'x', color=self.color)

    def plot_visited_cells(self):
        for node in self.path_log:
            pos = node[0]
            x = pos[0] + 0.5
            y = pos[1] + 0.5
            plt.plot(x, y, 'o', color=self.color, mfc='none')

    def plot_path(self):
        for node in self.path:
            pos = node[0]
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

        temp_path = [self.waypoints[0]]
        current_step = self.workspace.get_time_step()

        for i in range(0, len(self.waypoints) - 1):
            path = self.generate_straight_line_path(i, current_step)
            temp_path.pop()
            temp_path.extend(path)
            current_step = temp_path[-1][1]

        temp_path.reverse()
        temp_path.pop()
        self.path = temp_path

    def generate_straight_line_path(self, w_0, k=0):
        """
        Could use any type of path planner here. This is just a straight line style implementation
        Assume waypoint 1 is the starting location
        :return:
        """

        start = self.waypoints[w_0]
        goal = self.waypoints[w_0 + 1]

        # --- Straight line assumption ---

        i = self.get_information_available(start)
        path = [[start, k, i]]

        x = start[0]
        y = start[1]

        goal_found = False

        # North
        if start[1] < goal[1]:
            while not goal_found:
                y += 1
                k += 1
                i = self.get_information_available((x, y))
                path.append([(x, y), k, i])

                if (x, y) == goal:
                    goal_found = True
        # East
        elif start[0] < goal[0]:
            while not goal_found:
                x += 1
                k += 1
                i = self.get_information_available((x, y))
                path.append([(x, y), k, i])

                if (x, y) == goal:
                    goal_found = True
        # South
        elif start[1] > goal[1]:
            while not goal_found:
                y -= 1
                k += 1
                i = self.get_information_available((x, y))
                path.append([(x, y), k, i])

                if (x, y) == goal:
                    goal_found = True
        # West
        elif start[0] > goal[0]:
            while not goal_found:
                x -= 1
                k += 1
                i = self.get_information_available((x, y))
                path.append([(x, y), k, i])

                if (x, y) == goal:
                    goal_found = True
        # Error
        else:
            print("ERROR: Something's wrong with the start or goal position for {}".format(self.name))

        return path

    def generate_trajectory(self):
        traj = []
        path = self.path.copy()
        w_1 = self.path_log[0]

        while path:
            w_0 = w_1
            w_1 = path.pop()
            traj.append(self.checkCellDirection(w_0[0], w_1[0]))

        traj.reverse()
        self.trajectory = traj

    def get_information_available(self, pos):
        """

        :return:
        """
        x = pos[0]
        y = pos[1]

        return self.pdf[x][y]

    def update_pdf(self):
        """
        updated probability target is in current grid cell for the time step
        :return:
        """
        x = self.state[0]
        y = self.state[1]

        i_available = self.pdf[x][y]
        i_remaining = i_available * self._pD
        i_gained = i_available - i_remaining

        self.pdf[x][y] = i_remaining
        self.pdf = self.pdf/np.sum(self.pdf)      # normalize

        return i_gained

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
        i_gained = self.update_pdf()
        self.i_gained.append(i_gained)
        self.path_log.append(self.path.pop())

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
