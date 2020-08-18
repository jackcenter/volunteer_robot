import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


class Workspace:
    def __init__(self, boundary_coordinates):
        """

        :param boundary_coordinates: list of tuples
        """
        self.boundary_coordinates = boundary_coordinates
        self.agents = []
        self.time_step = 0

        self.x_ordinates = [i[0] for i in self.boundary_coordinates]
        self.y_ordinates = [i[1] for i in self.boundary_coordinates]

        self.x_bounds = (min(self.x_ordinates), max(self.x_ordinates))
        self.y_bounds = (min(self.y_ordinates), max(self.y_ordinates))

        self.map = None         # list of map coordinates
        self.pXY = None

        self.agents = []

    def plot(self):
        """
        Plots the environment boundaries as a black dashed line, the polygon obstacles, and the robot starting position
        and goal.
        :return: none
        """
        x_ords = self.x_ordinates.copy()
        x_ords.append(self.boundary_coordinates[0][0])

        y_ords = self.y_ordinates.copy()
        y_ords.append(self.boundary_coordinates[0][1])

        plt.plot(x_ords, y_ords, 'b-')

        x_min = self.x_bounds[0]
        x_max = self.x_bounds[1] + 1
        y_min = self.y_bounds[0]
        y_max = self.y_bounds[1] + 1

        plt.axis('equal')
        plt.grid(b=None, which='major', axis='both')
        plt.xticks(range(x_min, x_max, 1))
        plt.yticks(range(y_min, y_max, 1))
        plt.xlabel(r"Easting, $\xi$ [inches]")
        plt.ylabel(r"Northing, $\eta$ [inches]")

        for robot in self.agents:
            robot.plot()
            robot.plot_visited_cells()
            robot.plot_path()

    def get_time_step(self):
        return self.time_step

    def step(self):
        self.time_step += 1

    def add_agent(self, agent):
        self.agents.append(agent)

    def generate_grid(self):
        x_range = np.arange(self.x_bounds[0], self.x_bounds[1])
        y_range = np.arange(self.y_bounds[0], self.y_bounds[1])

        coordinates = []
        for x in x_range:
            row = []
            for y in y_range:
                row.append((x, y))

            coordinates.append(row)

        self.map = coordinates

    def generate_initial_distribution(self, dx=1, dy=1):
        x_range = np.arange(self.x_bounds[0], self.x_bounds[1], dx)
        y_range = np.arange(self.y_bounds[0], self.y_bounds[1], dy)
        X, Y = np.meshgrid(x_range, y_range)

        # Initial probability - uniform across the grid
        x_uniform = stats.uniform(loc=self.x_bounds[0], scale=self.x_bounds[1] - self.x_bounds[0])
        y_uniform = stats.uniform(loc=self.y_bounds[0], scale=self.y_bounds[1] - self.y_bounds[0])

        pX = x_uniform.pdf(X)
        pY = y_uniform.pdf(Y)
        self.pXY = pX*pY

        print(self.pXY)
        print()