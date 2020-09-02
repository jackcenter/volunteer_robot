class State_2D:
    def __init__(self, x_pos, y_pos):
        self.x1 = x_pos
        self.x2 = y_pos

    def get_position(self):
        return self.x1, self.x2

    def set_position(self, x, y):
        self.x1 = x
        self.x2 = y

    def get_x_position(self):
        return self.x1

    def set_x_position(self, x):
        self.x1 = x

    def get_y_position(self):
        return self.x2

    def set_y_position(self, y):
        self.x2 = y
