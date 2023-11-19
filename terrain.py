"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=2m43s
"""

from utils import *


class Terrain:
    def __init__(self, game):
        self.game = game
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.roads = {}
        self.cars = {}
        self.start_pos = WIDTH / 2, HEIGHT / 2
        self.generate_road()

    def clear_tile_map(self):
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

    # terrain generating algorithm. STILL IN PROGRESS!!!
    def generate_road(self):
        self.clear_tile_map()

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

        self.store_road_tiles()
        self.init_road_surface()

    # will be incorporated into generate_map()
    def store_road_tiles(self):
        for row_index, row in enumerate(self.tile_map):
            for col_index, tile in enumerate(row):
                if tile:
                    self.roads[(col_index, row_index)] = tile

    # initializes tiles from tile_map onto the terrain surface
    def init_road_surface(self):
        for row_i, row in enumerate(self.tile_map):
            for col_i, tile in enumerate(row):
                match tile:
                    case 1:
                        Tile(self, 'finish', row_i, col_i)
                        self.start_pos = ((col_i * TILE_SIZE) + TILE_CENTER - (CAR_WIDTH / 2),
                                          (row_i * TILE_SIZE) + TILE_CENTER - (CAR_HEIGHT / 2))
                    case 2:
                        Tile(self, 'ver', row_i, col_i)
                    case 3:
                        Tile(self, 'hor', row_i, col_i)
                    case 4:
                        Tile(self, 'grass', row_i, col_i)
                        Tile(self, 'ld', row_i, col_i)
                    case 5:
                        Tile(self, 'grass', row_i, col_i)
                        Tile(self, 'dr', row_i, col_i)
                    case 6:
                        Tile(self, 'grass', row_i, col_i)
                        Tile(self, 'ru', row_i, col_i)
                    case 7:
                        Tile(self, 'grass', row_i, col_i)
                        Tile(self, 'ul', row_i, col_i)
                    case _:
                        Tile(self, 'grass', row_i, col_i)

    def draw(self):
        self.game.screen.blit(self.surface, (0, 0))


class Tile:
    def __init__(self, road, key, row, col):
        self.road = road
        self.key = key
        self.row = row
        self.column = col
        self.blit()

    def blit(self):
        self.road.surface.blit(TILE_IMAGES[self.key], (self.column * TILE_SIZE, self.row * TILE_SIZE))


class Tile2:
    def __int__(self, terrain, pos, type):
        self.terrain = terrain
        self.type = type
        self.pos = self.x, self.y = pos
        self.borders = self.borders()
        self.image = TILE_IMAGES[type]
        self.draw_on_surface()

    @property
    def left_border(self):
        return self.x

    @property
    def down_border(self):
        return self.y

    @property
    def right_border(self):
        return self.x + TILE_SIZE

    @property
    def up_border(self):
        return self.y + TILE_SIZE

    def borders(self):
        match self.type:
            case 'finish':
                self.terrain.start_pos = self.x + TILE_CENTER - (CAR_WIDTH / 2), self.y + TILE_CENTER - (CAR_HEIGHT / 2)
                return (self.left_border, self.right_border), (None, None)
            case 'ver':
                return (self.left_border, self.right_border), (None, None)
            case 'hor':
                return (None, None), (self.up_border, self.down_border)
            case 'ld':
                return (None, self.right_border), (self.up_border, None)
            case 'dr':
                return (self.left_border, None), (self.up_border, None)
            case 'ru':
                return (self.left_border, None), (None, self.down_border)
            case 'ul':
                return (None, self.right_border), (None, self.down_border)
            case 'grass':
                return (None, None), (None, None)

    def draw_on_surface(self):
        self.terrain.surface.blit(self.image, self.pos)

    def check_collision(self, pos):
        hor = False
        ver = False
        if Utils.in_range(self.borders[0], pos[0]):
            hor = True
        if Utils.in_range(self.borders[1], pos[1]):
            ver = True

        return hor, ver

