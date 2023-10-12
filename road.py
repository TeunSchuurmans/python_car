import pygame as pg
from settings import * 


class Road:
    tile = TILE_SIZE
    tile_center = TILE_CENTER
    rows = HEIGHT // tile
    columns = WIDTH // tile

    def __init__(self, game):
        self.game = game
        self.road_map = [[False for _ in range(Road.columns)] for _ in range(Road.rows)]
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
        self.start_pos = WIDTH/2, HEIGHT/2
        self.generate_map()

    def generate_map(self):
        for row_index, row in enumerate(self.road_map):
            for col_index, item in enumerate(row):
                match item:
                    case 1:
                        Tile(self, 'finish', row_index, col_index)
                        
                        #sets the car's starting position to the center of the finish
                        self.start_pos = (col_index * Road.tile) + Road.tile_center - (CAR_WIDTH / 2), (row_index * Road.tile) + Road.tile_center  - (CAR_HEIGHT / 2)
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
    dimensions = (TILE_SIZE, TILE_SIZE)
    corner_image = pg.transform.scale(pg.image.load(CORNER_IMAGE), dimensions)

    images = {
        'grass' : pg.transform.scale(pg.image.load(GRASS_IMAGE), dimensions),
        'finish' : pg.transform.scale(pg.image.load(FINISH_IMAGE), dimensions),
        'ver' : pg.transform.scale(pg.image.load(STRAIGHT_IMAGE), dimensions),
        'hor' : pg.transform.rotate(pg.transform.scale(pg.image.load(STRAIGHT_IMAGE), dimensions),90),
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
        self.road.road_surface.blit(Tile.images[self.key], (self.column * TILE_SIZE, self.row * TILE_SIZE))
