import pygame as pg
import math
from settings import *

class RayCaster:
    def __init__(self, game, road, car):
        self.game = game
        self.road = road
        self.car = car
        self.car_fov = CAR_FOV
        self.half_fov = self.car_fov / 2
        self.ray_gap = self.car_fov / (NUM_OF_RAYS - 1)
        self.ray_ends = [_ for _ in range(NUM_OF_RAYS)]

    #utility functions
    @property
    def start_point(self):
        return (self.car.car_center_x, self.car.car_center_y)

    def ray_angle(self, x):
        return math.radians((self.car.angle - self.half_fov) + self.ray_gap * x) 


    #loop functions
    def cast_rays(self):
        for x, _ in enumerate(self.ray_ends):

            dx = 0
            dy = 0
            x_depth = 0
            y_depth = 0

            for tile in len(self.road.tile_map[0][0]):
                if tile:
                    x_depth += dx
                else:
                    break
                    
            for tile in len(self.road.tile_map[0]):
                if tile:
                    y_depth += dy
                else:
                    break

            self.ray_ends[x] = (self.start_point[0] + math.sin(self.ray_angle(x)) * -100, self.start_point[1] + math.cos(self.ray_angle(x)) * -100)

    def draw(self):
        for end_point in self.ray_ends:
            pg.draw.line(
                self.game.screen,
                'white',
                (self.start_point[0], self.start_point[1]),
                (end_point[0], end_point[1]),
                3)
            pg.draw.circle(self.game.screen,
                'orange',
                (end_point[0], end_point[1]),
                4)
            
    def update(self):
        self.cast_rays()
    

