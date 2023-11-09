import pygame as pg
import math
from settings import *


class RayCaster:
    def __init__(self, game, road, car):
        self.game = game
        self.road = road
        self.car = car
        self.ray_ends = [_ for _ in range(NUM_OF_RAYS)]

    #utility functions
    @property
    def tile_pos(self):
        return (self.car.current_tile[0] * TILE_SIZE, self.car.current_tile[1] * TILE_SIZE)
    
    def current_tile(self, x, y):
        return (x // TILE_SIZE, y // TILE_SIZE)

    def ray_angle(self, index):
        return math.radians(self.car.angle - HALF_SPREAD + RAY_GAP * index)

    def ray_length(self, side1, side2):
        return  math.sqrt(side1**2 + side2 **2) 


    #loop functions
    def cast_rays(self):
        for x, _ in enumerate(self.ray_ends):
            pass

    def check_collision(self, dx, dy):
        end_point = 0,0

        for x in range(10):
            pass
        
        return end_point
            
    def draw(self):
        pass
        """
        for end_point in self.ray_ends:
            pg.draw.line(
                self.game.screen,
                'white',
                self.car.center,
                (end_point[0], end_point[1]),
                3)
            pg.draw.circle(self.game.screen,
                'orange',
                (end_point[0], end_point[1]),
                4)
        """    
            
    def update(self):
        self.cast_rays()
    

