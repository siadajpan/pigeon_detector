from typing import Tuple, Optional


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.check_correct_data()

    def __eq__(self, other):
        same_width = self.width == other.width
        same_height = self.height == other.height
        same_x = self.x == other.x
        same_y = self.y == other.y

        return same_x and same_y and same_height and same_width

    def __repr__(self):
        return 'x: {}, y: {}, height: {}, width: {}'.\
            format(self.x, self.y, self.height, self.width)

    @property
    def data(self):
        return self.x, self.y, self.width, self.height

    @data.setter
    def data(self, lengths: Optional[Tuple[int, int, int, int]]):
        if not lengths:
            lengths = (0, 0, 0, 0)

        self.x = lengths[0]
        self.y = lengths[1]
        self.width = lengths[2]
        self.height = lengths[3]

    @property
    def x_end(self):
        return self.x + self.width

    @property
    def y_end(self):
        return self.y + self.height

    @property
    def ends(self):
        return self.x_end, self.y_end

    def check_correct_data(self):
        if self.x < 0 or self.y < 0 or self.width < 0 or self.height < 0:
            raise ValueError('Input data incorrect. All values need'
                             'to be positive')
