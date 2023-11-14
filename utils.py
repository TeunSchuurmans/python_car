from settings import *


class Utils:
    class Tile:
        @staticmethod
        def current(pos):
            return pos[0] // TILE_SIZE, pos[1] // TILE_SIZE

        @staticmethod
        def left_border(pos):
            return Utils.Tile.current(pos)[0] * TILE_SIZE

        @staticmethod
        def down_border(pos):
            return Utils.Tile.current(pos)[1] * TILE_SIZE + TILE_SIZE

        @staticmethod
        def right_border(pos):
            return Utils.Tile.current(pos)[0] * TILE_SIZE + TILE_SIZE

        @staticmethod
        def up_border(pos):
            return Utils.Tile.current(pos)[1] * TILE_SIZE

    @staticmethod
    def in_range(minimum, maximum, value):
        if maximum is None:
            return minimum < value
        if minimum is None:
            return maximum > value
        else:
            return (minimum < value) and (maximum > value)
