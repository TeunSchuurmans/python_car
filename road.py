import pygame as pg
from settings import * 


class Road:
    rows = HEIGHT // 100
    columns = WIDTH // 100

    def __init__(self, game):
        self.game = game
        self.road_map = [[0 for _ in range(Road.columns)] for _ in range(Road.rows)]
        self.road_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 3, 3, 4, 0, 0, 0, 0, 5, 3, 3, 3, 3, 4, 0],
        [0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
        [0, 1, 0, 0, 6, 3, 3, 4, 0, 2, 0, 0, 0, 0, 2, 0],
        [0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0],
        [0, 6, 3, 3, 4, 0, 0, 2, 0, 6, 3, 3, 4, 0, 2, 0],
        [0, 0, 0, 0, 2, 0, 0, 6, 3, 3, 3, 3, 7, 0, 2, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 0],
        ]

        self.road_surface = pg.Surface((WIDTH, HEIGHT))
        self.generate_map()

    def generate_map(self):
        for row_index, row in enumerate(self.road_map):
            for col_index, item in enumerate(row):
                match item:
                    case 1:
                        Tile(self, 'finish', row_index, col_index)
                    case 2:
                        Tile(self, 'ver', row_index, col_index)
                    case 3:
                        Tile(self, 'hor', row_index, col_index)
                    case 4:
                        Tile(self, 'L_D', row_index, col_index)
                    case 5:
                        Tile(self, 'D_R', row_index, col_index)
                    case 6:
                        Tile(self, 'R_U', row_index, col_index)
                    case 7:
                        Tile(self, 'U_L', row_index, col_index)
                    case _:
                        Tile(self, 'grass', row_index, col_index)

    def draw(self):
        self.game.screen.blit(self.road_surface, (0, 0))
                        

class Tile:
    corner_image = pg.transform.scale(pg.image.load(CORNER_IMAGE), (100, 100))

    images = {
        'grass' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'finish' : pg.transform.scale(pg.image.load(FINISH_IMAGE), (100,100)),
        'ver' : pg.transform.scale(pg.image.load(STRAIGHT_IMAGE), (100,100)),
        'hor' : pg.transform.rotate(pg.transform.scale(pg.image.load(STRAIGHT_IMAGE), (100, 100)),90),
        'L_D' : pg.transform.rotate(corner_image, 270),
        'D_R' : corner_image,
        'R_U' : pg.transform.rotate(corner_image, 90),
        'U_L' : pg.transform.rotate(corner_image, 180),
    }

    def __init__(self, road, key, row, col):
        self.road = road
        self.key = key
        self.row = row
        self.column = col
        self.blit()   
    
    def blit(self):
        self.road.road_surface.blit(Tile.images[self.key], (self.column * 100, self.row * 100))
