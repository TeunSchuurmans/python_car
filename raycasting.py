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
from terrain import *

class RayCaster:
    def __init__(self, game, terrain, npc):
        self.game = game
        self.terrain = terrain
        self.npc = npc
        self.nnet = NNet(self)
        self.rays = [0 for _ in range(NUM_OF_RAYS)]

    #utility functions
    def ray_angle(self, index):
        return (self.npc.angle - HALF_SPREAD + RAY_GAP * index)  % (math.pi * 2)

    def ray_length(self, x, y):
        side1 = x - self.npc.center[0]
        side2 = y - self.npc.center[1]
        return  math.sqrt(side1**2 + side2 **2)

    #loop functions
    def cast_rays(self):
        for i, _ in enumerate(self.rays):

            angle = self.ray_angle(i) + 1e-10
            tan_a = math.tan(angle)
            start_tb = self.terrain.roads[Tile.current(self.npc.center)].borders

            """
            Horizontal
            """

            h_x_end, h_y_end = self.npc.center
            h_dx = TILE_SIZE * tan_a
            h_dy = TILE_SIZE

            # down
            if (math.pi / 2) < angle < (math.pi * 3 / 2):
                h_y_end = start_tb['down']
                h_x_end += tan_a * (h_y_end - self.npc.center[1])
            # up
            else:
                h_y_end = start_tb['up']
                h_x_end -= tan_a * (self.npc.center[1] - h_y_end)
                h_dx = -h_dx
                h_dy = -h_dy

            for _ in DOF:
                if self.ray_length(h_x_end, h_y_end) >= MAX_RAY_LENGTH:
                    break
                pg.draw.circle(self.game.screen, 'blue', (h_x_end, h_y_end), 4)
                h_x_end += h_dx
                h_y_end += h_dy

            """
            Vertical
            """

            v_x_end, v_y_end = self.npc.center
            v_dx = TILE_SIZE
            v_dy = 1 / tan_a * TILE_SIZE

            # left
            if 0 < angle < math.pi:
                v_x_end = start_tb['left']
                v_y_end -= 1 / tan_a * (self.npc.center[0] - v_x_end)
                v_dx = -v_dx
                v_dy = -v_dy
            # right
            else:
                v_x_end = start_tb['right']
                v_y_end += 1 / tan_a * (v_x_end - self.npc.center[0])


            for _ in DOF:
                if self.ray_length(v_x_end, v_y_end) >= MAX_RAY_LENGTH:
                    break
                pg.draw.circle(self.game.screen, 'green', (v_x_end, v_y_end), 4)
                v_x_end += v_dx
                v_y_end += v_dy

            ray_length = min(self.ray_length(h_x_end, h_y_end), self.ray_length(v_x_end, v_y_end))
            self.rays[i] = ray_length


    def draw(self):
        for i, ray in enumerate(self.rays):
            end = (self.npc.center[0] + math.sin(self.ray_angle(i)) * -ray, self.npc.center[1] + math.cos(self.ray_angle(i)) * -ray)
            pg.draw.line(self.game.screen, 'white', self.npc.center, end, 2)
            pg.draw.circle(self.game.screen, 'red', end, 4)
            
    def update(self):
        self.cast_rays()

    

