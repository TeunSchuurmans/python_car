import pygame as pg
import math
from settings import *

class RayCaster:
    def __init__(self, game, car):
        self.game = game
        self.car = car
        self.num_rays = NUM_OF_RAYS
        self.car_fov = CAR_FOV
        self.half_fov = self.car_fov / 2
        self.ray_gap = self.car_fov / self.num_rays
        self.ray_ends = [_ for _ in range(self.num_rays)]

    #utility functions
    def ray_angle(self, x):
        return math.radians((self.car.angle - self.half_fov) + self.ray_gap * x) 


    #loop functions
    def cast_rays(self):
        for x in range(self.num_rays):
            self.ray_ends[x] = (self.car.car_center_x + math.sin(self.ray_angle(x)) * -100, self.car.car_center_y + math.cos(self.ray_angle(x)) * -100)

    def draw(self):
        for x in self.ray_ends:
            pg.draw.line(
                self.game.screen,
                'yellow',
                (self.car.car_center_x, self.car.car_center_y),
                (x[0], x[1]),
                3)
            
    def update(self):
        self.cast_rays()
    

