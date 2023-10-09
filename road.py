import pygame as pg
from settings import * 




class Road:
    rows = HEIGHT // 100
    columns = WIDTH // 100
    images = {
        'grass' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'finish' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'ver' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'hor' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'L_D' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'D_R' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'R_U' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
        'U_L' : pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100)),
    }

    def __init__(self, game):
        self.game = game
        self.road_map = [[0 for _ in range(Road.columns)] for _ in range(Road.rows)]
        self.road_map =[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
                        Tile(self, 'finish', row_index, col_index)
                    case 3:
                        Tile(self, 'finish', row_index, col_index)
                    case 4:
                        Tile(self, 'finish', row_index, col_index)
                    case 6:
                        Tile(self, 'finish', row_index, col_index)
                    case 6:
                        Tile(self, 'finish', row_index, col_index)
                    case 7:
                        Tile(self, 'finish', row_index, col_index)
                    case _:
                        Tile(self, 'finish', row_index, col_index)

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
        self.road.road_surface.blit(Road.images[self.key], (self.column * 100, self.row * 100))
