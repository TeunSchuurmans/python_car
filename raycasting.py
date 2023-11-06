import pygame as pg
import math
from settings import *

class RayCaster:
    def __init__(self, game, road, car):
        self.game = game
        self.road = road
        self.car = car
        self.half_fov = RAY_SPREAD / 2
        self.ray_gap = RAY_SPREAD / (NUM_OF_RAYS - 1)
        self.ray_ends = [_ for _ in range(NUM_OF_RAYS)]
        print(self.ray_gap, RAY_SPREAD, math.pi)

    #utility functions
    @property
    def start_point(self):
        return (self.car.car_center_x, self.car.car_center_y)

    @property
    def tile_pos(self):
        return (self.car.current_tile[0] * TILE_SIZE, self.car.current_tile[1] * TILE_SIZE)
    
    def current_tile(self, x, y):
        return (x // TILE_SIZE, y // TILE_SIZE)

    def ray_angle(self, x):
        return math.radians(self.car.angle - self.half_fov + self.ray_gap * x)

    def ray_length(self, side1, side2):
        return  math.sqrt(side1**2 + side2 **2) 


    #loop functions
    def cast_rays(self):
        for x, _ in enumerate(self.ray_ends):            
            
            #horizontal raycasting
            hor_dx = math.tan(self.ray_angle(x)) * TILE_SIZE
            hor_dy = TILE_SIZE
            hor_x_end= self.tile_pos[0]
            hor_y_end = self.tile_pos[1]

            for _ in self.road.tile_map[0]:
                hor_x_end += hor_dx
                hor_y_end += hor_dy
                pg.draw.circle(self.game.screen,
                'white',
                (hor_x_end, hor_y_end),
                5)


            #vertical raycasting
            ver_dx = TILE_SIZE
            ver_dy = TILE_SIZE / (math.tan(self.ray_angle(x)) + 1e-10)
            ver_x_end = self.tile_pos[0]
            ver_y_end = self.tile_pos[1]

            for _ in self.road.tile_map:
                ver_x_end += ver_dx
                ver_y_end += ver_dy
                pg.draw.circle(self.game.screen,
                'white',
                (ver_x_end, ver_y_end),
                5)
    
    
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
    

