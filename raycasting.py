"""
Code inspired by : javidx9
    Video title: Super Fast Ray Casting in Tiled Worlds using DDA
    Video link: https://www.youtube.com/watch?v=NbSee-XM7WA
    also: https://lodev.org/cgtutor/raycasting.html
"""

import math
import pygame as pg
from settings import *
from nnet import *

class RayCaster:
    def __init__(self, game, road, car):
        self.game = game
        self.road = road
        self.car = car
        self.nnet = NNet(self)
        self.ray_ends = [_ for _ in range(NUM_OF_RAYS)]

    #utility functions
    @property
    def tile_pos(self):
        return (self.car.current_tile[0] * TILE_SIZE, self.car.current_tile[1] * TILE_SIZE)
    
    def current_tile(self, x, y):
        return (x // TILE_SIZE, y // TILE_SIZE)

    def ray_angle(self, index):
        return self.car.angle - HALF_SPREAD + RAY_GAP * index

    def ray_length(self, side1, side2):
        return  math.sqrt(side1**2 + side2 **2) 


    #loop functions
    def cast_rays(self):
        for x, _ in enumerate(self.ray_ends):
            pass
            self.ray_ends[x] = (self.car.center[0] + math.sin(self.ray_angle(x)) * -100, self.car.center[1] + math.cos(self.ray_angle(x)) * -100)
            #self.car.rays[x] = self.ray_length(side1, side2)
            
            
    def draw(self):
        for end in self.ray_ends:
            pg.draw.line(
                self.game.screen,
                'white',
                self.car.center,
                (end[0], end[1]),
                3)
            pg.draw.circle(self.game.screen,
                'orange',
                (end[0], end[1]),
                4)    
            
    def update(self):
        self.cast_rays()

    

