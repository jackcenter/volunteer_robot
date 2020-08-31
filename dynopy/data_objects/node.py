class Node:
    def __init__(self, position, cost, information, time_step):
        """
        Data object that holds information for nodes used in motion planning.
        :param position: tuple with x and y locations
        :param cost: cost of node along path
        :param information: probability the target can be seen from the node position
        :param time_step: int for node time_step
        """
        self.pos = position
        self.c = cost
        self.i = information
        self.k = time_step

    def get_position(self):
        return self.pos

    def set_position(self, pos):
        self.pos = pos

    def get_cost(self):
        return self.c

    def set_cost(self, cost):
        self.c = cost

    def get_information(self):
        return self.i

    def set_information(self, i):
        self.i = i

    def get_time_step(self):
        return self.k

    def set_time_step(self, k):
        self.k = k
