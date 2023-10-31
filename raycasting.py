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
        return math.radians(self.car.angle - self.half_fov + self.ray_gap * x)

    def ray_length(self, side1, side2):
        return  math.sqrt(side1**2 + side2 **2) 


    #loop functions
    def cast_rays(self):
        for x, _ in enumerate(self.ray_ends):
            
            #variables for horizontal raycasting
            hor_d = (TILE_SIZE,(TILE_SIZE / (math.tan(self.ray_angle(x)) + -1e6)))
            hor_x_end= self.car.current_tile[0] * TILE_SIZE
            hor_y_end = self.car.current_tile[1] * TILE_SIZE

            #variables for vertical raycasting
            ver_d = ((math.tan(self.ray_angle(x)) * TILE_SIZE),TILE_SIZE)
            ver_x_end = self.car.current_tile[0] * TILE_SIZE
            ver_y_end = self.car.current_tile[1] * TILE_SIZE
            
            #horizontal
            for _ in self.road.tile_map[0]:
                if 1 == 2:
                    break
                hor_x_end += hor_d[0]
                hor_y_end += hor_d[1]
                pg.draw.circle(self.game.screen,
                'orange',
                (hor_x_end, hor_y_end),
                4)

            #vertical   
            for _ in self.road.tile_map:
                if 1 == 2:
                        break
                ver_x_end += ver_d[0]
                ver_y_end += ver_d[1]
                pg.draw.circle(self.game.screen,
                'orange',
                (ver_x_end, ver_y_end),
                4)
            
            #collision_point = min(hor_collision, ver_collision)

            #self.ray_ends[x] = collision_point
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
    

