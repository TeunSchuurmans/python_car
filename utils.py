from settings import *


class Utils:

    class Tile:
        @staticmethod
        def current(pos):
            return pos[0] // TILE_SIZE, pos[1] // TILE_SIZE

    @staticmethod
    def in_range(bounds, value):
        minimum, maximum = bounds

        if minimum is None and maximum is None:
            return True
        if maximum is None:
            return minimum < value
        if minimum is None:
            return maximum > value
        else:
            return minimum < value < maximum
