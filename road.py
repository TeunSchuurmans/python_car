import pygame as pg
import random
from settings import * 


class Road:
    tile = TILE_SIZE
    tile_center = TILE_CENTER
    rows = HEIGHT // tile
    columns = WIDTH // tile

    def __init__(self, game):
        self.game = game
        self.road_dict = {}
        self.map_surface = pg.Surface((WIDTH, HEIGHT))
        self.start_pos = WIDTH/2, HEIGHT/2
        self.generate_map()


    #road generating algorithm, STILL IN PROGRESS!!!
    def generate_map(self):
        self.tile_map = [[False for _ in range(Road.columns)] for _ in range(Road.rows)] #clears the map so it can be regenerated

        #curr_row = random.randint(1, len(self.tile_map) -2)
        #curr_col = random.randint(1, len(self.tile_map[0]) - 2)
        #self.tile_map[curr_row][curr_col] = 1

        
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
        
        self.init_road_borders()
        self.blit_tiles()

    # adds all road pieces to a dictionary with the according coordinates for collision detection, WORK IN PROGRESS
    def init_road_borders(self):    
        for row_index, row in enumerate(self.tile_map):
            for col_index, tile in enumerate(row):
                if tile:
                    self.road_dict[(col_index, row_index)] = tile
        print(self.road_dict)


    #takes the tile map and draws the according tiles onto a surface
    def blit_tiles(self):    
        for row_index, row in enumerate(self.tile_map):
            for col_index, tile in enumerate(row):
                match tile:
                    case 1:
                        Tile(self, 'finish', row_index, col_index)
                        
                        #sets the car's starting position to the center of the finish, might be moved to generate_map()
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


    #takes the tile map and draws the according tiles onto a surface
    def draw(self):         
        self.game.screen.blit(self.map_surface, (0, 0))
                        

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
        self.road.map_surface.blit(Tile.images[self.key], (self.column * TILE_SIZE, self.row * TILE_SIZE))
