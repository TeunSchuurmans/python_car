import pygame as pg
from settings import * 



class Road:
    rows = HEIGHT // 100
    columns = WIDTH // 100
    grass = pg.transform.scale(pg.image.load(GRASS_IMAGE), (100,100))
    finish = ''
    road_ver = ''
    road_hor = ''
    road_L_D = ''
    road_D_R = ''
    road_R_U = ''
    road_U_L = ''

    def __init__(self, game):
        self.game = game
        self.road_map = [[1 for i in range(Road.columns)] for x in range(Road.rows)]
        self.generate_map()

    def generate_map(self):
        pass

    def draw(self):
        for x in range(19):
            for i in range(9):
                self.game.screen.blit(Road.grass, (x * 100, i * 100))
                        
                        
                    
