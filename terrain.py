"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=2m43s
"""

import pygame as pg
from settings import *


class Terrain:
    def __init__(self, game):
        self.game = game
        self.road_surface = pg.Surface((WIDTH, HEIGHT))
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.roads = {}
        self.start_pos = WIDTH / 2, HEIGHT / 2
        self.cars = {}
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
        self.game.screen.blit(self.road_surface, (0, 0))


class Tile:
    def __init__(self, road, key, row, col):
        self.road = road
        self.key = key
        self.row = row
        self.column = col
        self.blit()

    def blit(self):
        self.road.road_surface.blit(TILE_IMAGES[self.key], (self.column * TILE_SIZE, self.row * TILE_SIZE))


class Tile2:
    def __int__(self, road, pos, type, image):
        self.road = road
        self.pos = self.x, self.y = pos
        self.type = type
        self.image = image
