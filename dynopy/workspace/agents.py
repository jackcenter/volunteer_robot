import matplotlib.pyplot as plt
import numpy as np

from dynopy.data_objects.node import Node
from dynopy.data_objects.state import State_2D


class Robot:
    def __init__(self, name: str, color: str, state, volunteer=False):
        """

        :param name:
        :param color:
        :param state: [x position, y_position]
        """
        self.name = name
        self.color = color
        self.state = state
        self.configuration_space = None
        self.volunteer = volunteer

        self.waypoints = []         # list of points the agent needs to reach
        self.path = []              # list of 2D positions
        self.path_log = []
        self.trajectory = []        # last element, [-1], is the next action to take
        self.trajectory_log = []    # stores actions taken in order, ie [0] is the first action

        self.pD = 0.85              # probability of detection
        self._pD = 1 - self.pD      # probability of no detection

        self.workspace = None       # current workspace
        # self.map = None             # list of coordinates corresponding to the map
        self.pdf = None             # current probability distribution
        self.i_gained = []          # information gained along path

    def start(self, workspace):
        """
        Set initial conditions for the robot in a specified workspace
        :param workspace: Workspace object that describes the environment the agent is working in
        :return:
        """
        self.set_workspace(workspace)
        # self.set_map()
        self.set_initial_pdf()
        self.update_pdf()

        current_step = self.workspace.get_time_step()
        i = self.get_information_available(self.state)
        start_node = Node.init_without_cost(self.state.get_position(), i, current_step)
        self.path_log.append(start_node)

    def load_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.generate_full_path()
        self.generate_trajectory()

    def plot(self):

        if self.volunteer:
            x = self.state.get_x_position()
            y = self.state.get_y_position()
            plt.plot(x, y, 'x', color=self.color)

        else:
            x = self.state.get_x_position() + 0.5
            y = self.state.get_y_position() + 0.5
            plt.plot(x, y, 'x', color=self.color)

    def plot_visited_cells(self):
        for node in self.path_log:
            pos = node.get_position()
            x = pos[0] + 0.5
            y = pos[1] + 0.5
            plt.plot(x, y, 'o', color=self.color, mfc='none')

    def plot_path(self):
        for node in self.path:
            pos = node.get_position()
            x = pos[0] + 0.5
            y = pos[1] + 0.5
            plt.plot(x, y, '.', color=self.color)

    def get_volunteer_status(self):
        return self.volunteer

    def set_workspace(self, ws):
        self.workspace = ws

    # def set_map(self):
    #     self.map = self.workspace.map

    def set_initial_pdf(self):
        self.pdf = self.workspace.pdf.copy()

    def get_pdf(self):
        return self.pdf

    def set_configuration_space(self):
        c1 = self.workspace.get_x_bounds()
        c2 = self.workspace.get_y_bounds()

        self.configuration_space = State_2D(c1, c2)

    def get_X_free(self):
        return self.configuration_space

    def get_position(self):
        return self.state.get_position()

    def generate_full_path(self):
        """
        Creates a list of nodes associated with each time step
        :return:
        """

        path = []         # place holder, value will be removed
        current_step = self.path_log[-1].get_time()

        for i in range(0, len(self.waypoints) - 1):
            temp_path = self.generate_straight_line_path(i, current_step)
            temp_path.reverse()
            temp_path.pop()
            temp_path.extend(path)

            path = temp_path
            current_step = path[0].get_time()

        # temp_path.reverse()
        # self.path_log.append(temp_path.pop())
        self.path = path

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
        path = [Node.init_without_cost(start, i, k)]

        x = start[0]
        y = start[1]

        goal_found = False

        # North
        if y < goal[1]:
            while not goal_found:
                y += 1
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # East
        elif x < goal[0]:
            while not goal_found:
                x += 1
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # South
        elif y > goal[1]:
            while not goal_found:
                y -= 1
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # West
        elif x > goal[0]:
            while not goal_found:
                x -= 1
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # Error
        else:
            print("ERROR: Something's wrong with the start or goal position for {}".format(self.name))

        return path

    def generate_trajectory(self):

        traj = []
        path = self.path.copy()
        w_1 = self.path_log[-1]

        while path:
            w_0 = w_1
            w_1 = path.pop()
            traj.append(self.checkCellDirection(w_0.get_position(), w_1.get_position()))

        traj.reverse()
        self.trajectory = traj

    def get_information_available(self, pos):
        """

        :return: information available in the specified grid cell.
        """
        if isinstance(pos, tuple):
            x = pos[0]
            y = pos[1]

        elif isinstance(pos, State_2D):
            x = pos.get_x_position()
            y = pos.get_y_position()

        else:
            print("Error: data type unknown for get_information_available")
            print(type(pos))
            return [[]]

        return self.pdf[x][y]

    def update_pdf(self):
        """
        updated probability target is in current grid cell for the time step
        :return:
        """
        x = self.state.get_x_position()
        y = self.state.get_y_position()

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
            # self.state[1] += 1
            self.state.set_y_position(self.state.get_y_position() + 1)
        elif action == 'east':
            # self.state[0] += 1
            self.state.set_x_position(self.state.get_x_position() + 1)
        elif action == 'south':
            # self.state[1] -= 1
            self.state.set_y_position(self.state.get_y_position() - 1)
        elif action == 'west':
            # self.state[0] -= 1
            self.state.set_x_position(self.state.get_x_position() - 1)
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
