class Node:
    def __init__(self, position, time_step, information):
        """
        Data object that holds information for nodes used in motion planning.
        :param position: tuple with x and y locations
        :param time_step: int for node time_step
        :param information: probability the target can be seen from the node position
        """
        self.pos = position
        self.k = time_step
        self.i = information

    def get_position(self):
        return self.pos

    def set_position(self, pos):
        self.pos = pos

    def get_time_step(self):
        return self.k

    def set_time_step(self, k):
        self.k = k

    def get_information(self):
        return self.i

    def set_information(self, i):
        self.i = i
