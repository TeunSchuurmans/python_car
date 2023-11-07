import pygame as pg
import math
from settings import *

"""
This class is used for the bot car to receive information about the distance to the wall.
This way, the bot car can make decisions based on this information using the neural network.
First, it calculates the horizontal and vertical depth the ray should move by.
It does this by using the ray's angle and the tile size.
This makes the collision detection for the ray optimal.
Next, it checks each step for a collision with a wall.
It does this by using the the properties from the road class.
If a collision is detected, the cycle will break. Indicating that the sensor has come across a border.
Then, it compares the horizontal and vertical collision point, and picks the closest one.
This coordinate can then be used to calculate the distance from the wall to the car.
It does this for each ray, every frame.
"""


#instead of starting the collision detection at the car, it starts at the point on the grid behind the car


class RayCaster:
    def __init__(self, game, road, car):
        self.game = game
        self.road = road
        self.car = car
        self.half_fov = RAY_SPREAD / 2
        self.ray_gap = RAY_SPREAD / (NUM_OF_RAYS if NUM_OF_RAYS == 1 else NUM_OF_RAYS - 1)
        self.ray_ends = [_ for _ in range(NUM_OF_RAYS)]

    #utility functions

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
            #ver_len = self.check_collision()
            #hor_len = self.check_collision()

            pg.draw.line(self.game.screen, 'green', self.tile_pos, self.car.center, 3)
            self.ray_ends[x] = (self.car.center[0] + math.sin(self.ray_angle(x)) * -100, self.car.center[1] + math.cos(self.ray_angle(x)) * -100)

    def check_collision(self, dx, dy):
        end_point = 0,0

        for x in range(10):
            pass
        
        return end_point
            
    def draw(self):
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
            
    def update(self):
        self.cast_rays()
    

