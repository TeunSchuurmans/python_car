"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=2m43s
"""

import pygame as pg
from settings import *


class Road:
    tile = TILE_SIZE
    tile_center = TILE_CENTER
    rows = HEIGHT // tile
    columns = WIDTH // tile

    def __init__(self, game):
        self.game = game
        self.tile_map = [[0 for _ in range(Road.columns)] for _ in range(Road.rows)]
        self.road_dict = {}
        self.road_surface = pg.Surface((WIDTH, HEIGHT))
        self.start_pos = WIDTH / 2, HEIGHT / 2
        self.cars = []
        self.generate_road()

    # road generating algorithm. STILL IN PROGRESS!!!
    def generate_road(self):

        # clears the map so it can be regenerated
        self.tile_map = [[0 for _ in range(Road.columns)] for _ in range(Road.rows)]

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
                    self.road_dict[(col_index, row_index)] = tile

    # initializes tiles from tile_map onto the road surface
    def init_road_surface(self):
        for row_index, row in enumerate(self.tile_map):
            for col_index, tile in enumerate(row):
                match tile:
                    case 1:
                        Tile(self, 'finish', row_index, col_index)
                        self.start_pos = ((col_index * Road.tile) + Road.tile_center - (CAR_WIDTH / 2),
                                          (row_index * Road.tile) + Road.tile_center - (CAR_HEIGHT / 2))
                    case 2:
                        Tile(self, 'ver', row_index, col_index)
                    case 3:
                        Tile(self, 'hor', row_index, col_index)
                    case 4:
                        Tile(self, 'grass', row_index, col_index)
                        Tile(self, 'ld', row_index, col_index)
                    case 5:
                        Tile(self, 'grass', row_index, col_index)
                        Tile(self, 'dr', row_index, col_index)
                    case 6:
                        Tile(self, 'grass', row_index, col_index)
                        Tile(self, 'ru', row_index, col_index)
                    case 7:
                        Tile(self, 'grass', row_index, col_index)
                        Tile(self, 'ul', row_index, col_index)
                    case _:
                        Tile(self, 'grass', row_index, col_index)

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
