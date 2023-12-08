"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=2m43s
"""

from settings import *
from database import *


class Terrain:
    def __init__(self, game):
        self.game = game
        self.db = Database()
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.roads = {}
        self.cars = {}
        self.start_pos = WIDTH / 2, HEIGHT / 2
        self.generate_road()

    def clear_tiles(self):
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.roads.clear()

    # terrain generating algorithm. STILL IN PROGRESS!!!
    def generate_road(self):
        self.clear_tiles()

        # temporary tile map
        self.tile_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 3, 3, 4, 0, 0, 0, 0, 5, 3, 3, 3, 3, 4, 0],
            [0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 5, 3, 3, 7, 0],
            [0, 1, 0, 0, 6, 3, 3, 4, 0, 2, 0, 2, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 6, 3, 3, 4, 0],
            [0, 6, 3, 3, 4, 0, 0, 2, 0, 6, 3, 3, 4, 0, 2, 0],
            [0, 0, 0, 0, 2, 0, 0, 6, 3, 3, 3, 3, 7, 0, 2, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 0],
        ]

        self.init_tiles()

    def init_tiles(self):
        for row_i, row in enumerate(self.tile_map):
            for col_i, tile in enumerate(row):
                key = (col_i, row_i)
                pos = (col_i * TILE_SIZE, row_i * TILE_SIZE)
                if tile:
                    self.roads[key] = Tile(self, pos, tile)
                else:
                    Tile(self, pos, tile)
                if SHOW_GRID:
                    Tile(self, pos, 'grid')

    def draw(self):
        self.game.screen.blit(self.surface, (0, 0))

    def check_car_status(self):

        """

        if all npc cars are either dead, or have finished 2 laps:


        """

    def update(self):
        self.check_car_status()


class Tile:

    # init functions
    def __init__(self, terrain, pos, key):
        self.terrain = terrain
        self.key = key
        self.pos = self.x, self.y = pos
        self.type = ''
        self.collision_borders = self.init_border_type()
        self.image = TILE_IMAGES[self.type]
        self.draw_on_surface()

    def draw_on_surface(self):
        self.terrain.surface.blit(self.image, self.pos)

    # utility functions
    @property
    def borders(self):
        return {
            'left': self.x,
            'down': self.y + TILE_SIZE,
            'right': self.x + TILE_SIZE,
            'up': self.y,
        }

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

    def init_border_type(self):
        match self.key:
            case 1:
                self.terrain.start_pos = self.x + TILE_CENTER - (CAR_WIDTH / 2), self.y + TILE_CENTER - (CAR_HEIGHT / 2)
                self.type = 'finish'
                return (self.borders['left'], self.borders['right']), (None, None)
            case 2:
                self.type = 'ver'
                return (self.borders['left'], self.borders['right']), (None, None)
            case 3:
                self.type = 'hor'
                return (None, None), (self.borders['up'], self.borders['down'])
            case 4:
                self.type = 'ld'
                return (None, self.borders['right']), (self.borders['up'], None)
            case 5:
                self.type = 'dr'
                return (self.borders['left'], None), (self.borders['up'], None)
            case 6:
                self.type = 'ru'
                return (self.borders['left'], None), (None, self.borders['down'])
            case 7:
                self.type = 'ul'
                return (None, self.borders['right']), (None, self.borders['down'])
            case 0:
                self.type = 'grass'
                return (self.borders['left'], self.borders['right']), (self.borders['up'], self.borders['down'])
            case 'grid':
                self.type = 'grid'
                return (None, None), (None, None)

    def check_collision(self, pos):
        hor = False
        ver = False
        if Tile.in_range(self.collision_borders[0], pos[0]):
            hor = True
        if Tile.in_range(self.collision_borders[1], pos[1]):
            ver = True

        return hor, ver
