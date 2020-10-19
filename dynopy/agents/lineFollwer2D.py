# !/usr/bin/env python
# -*- coding: utf-8 -*-

from dynopy.agents.robot2D import Robot2D
from dynopy.data_objects.node import Node


class LineFollower2D(Robot2D):
    def load_waypoints(self, waypoints, steps=None):
        self.waypoints = waypoints
        self.generate_full_path(steps)
        self.generate_trajectory()

    def step(self):
        """
        moves the agent in the commanded direction
        :param
        :return:
        """
        if self.path:
            root = self.path.pop()
            action = self.trajectory.pop()
        else:
            root = self.path_log[-1]
            action = 'stay'

        self.path_log.append(root)
        state = self.state.copy()
        if action == 'north':
            state.set_y_position(self.state.get_y_position() + self.cfg["step_size"])
        elif action == 'east':
            state.set_x_position(self.state.get_x_position() + self.cfg["step_size"])
        elif action == 'south':
            state.set_y_position(self.state.get_y_position() - self.cfg["step_size"])
        elif action == 'west':
            state.set_x_position(self.state.get_x_position() - self.cfg["step_size"])
        elif action == 'stay':
            pass
        else:
            print("ERROR: robot action not understood. Needs to be north, east, south, or west")
            return

        state.set_time(root.get_time())     # TODO: simply takes node time, could update based on current time instead

        self.trajectory_log.append(action)
        self.set_state(state)
        self.state_log.append(self.state)
        self.update_information()

    def generate_full_path(self, steps):
        """
        Creates a list of nodes associated with each time step
        :return:
        """

        path = []         # place holder, value will be removed
        current_step = self.path_log[-1].get_time()

        if not self.waypoints:
            # No waypoints provided, robot will just sit still
            self.waypoints.append(self.state.get_position())
            print(self.name)

        elif self.state.get_position() != self.waypoints[0]:
            # The first state is the first waypoint, don't need it.
            self.waypoints.insert(0, self.state.get_position())
            print(self.name)
            print([x for x in self.waypoints])

        for point in range(0, len(self.waypoints) - 1):
            temp_path = self.generate_straight_line_path(point, current_step)
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
                y += self.cfg["step_size"]
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # East
        elif x < goal[0]:
            while not goal_found:
                x += self.cfg["step_size"]
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # South
        elif y > goal[1]:
            while not goal_found:
                y -= self.cfg["step_size"]
                k += 1
                i = self.get_information_available((x, y))
                path.append(Node.init_without_cost((x, y), i, k))

                if (x, y) == goal:
                    goal_found = True
        # West
        elif x > goal[0]:
            while not goal_found:
                x -= self.cfg["step_size"]
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