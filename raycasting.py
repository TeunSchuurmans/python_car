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
            angle = self.ray_angle(i) + 1e-100
            #horizontal
            h_dx, h_dy = 0, TILE_SIZE
            h_x_end, h_y_end = self.npc.center
            #down
            if (math.pi / 2) < angle < (math.pi * 3 / 2):
                h_y_end = self.terrain.roads[Tile.current(self.npc.center)].borders['down']
                h_x_end += math.tan(angle) * (h_y_end - self.npc.center[1])
            #up
            else:
                h_y_end = self.terrain.roads[Tile.current(self.npc.center)].borders['up']
                h_x_end -= math.tan(angle) * (self.npc.center[1] - h_y_end)

            for x in DOF:
                if False:
                    break
                else:
                    #h_x_end += h_dx
                    #h_y_end += h_dy
                    pass

            #vertical
            v_dx, v_dy = TILE_SIZE, 0
            v_x_end, v_y_end = self.npc.center

            #left
            if 0 < angle < math.pi:
                v_x_end = self.terrain.roads[Tile.current(self.npc.center)].borders['left']
                v_y_end -= 1 / math.tan(angle) * (self.npc.center[0] - v_x_end)
            #right
            else:
                v_x_end = self.terrain.roads[Tile.current(self.npc.center)].borders['right']
                v_y_end += 1 / math.tan(angle) * (v_x_end - self.npc.center[0])

            for x in DOF:
                if False:
                    break
                else:
                    #v_x_end += v_dx
                    #v_y_end += v_dy
                    pass

            ray_length = min(min(self.ray_length(h_x_end, h_y_end), self.ray_length(v_x_end, v_y_end)), MAX_RAY_LENGTH)
            self.rays[i] = ray_length

    def draw(self):
        for i, ray in enumerate(self.rays):
            end = (self.npc.center[0] + math.sin(self.ray_angle(i)) * -ray, self.npc.center[1] + math.cos(self.ray_angle(i)) * -ray)
            pg.draw.line(self.game.screen, 'white', self.npc.center, end, 2)
            pg.draw.circle(self.game.screen, 'blue', end, 4)
            
    def update(self):
        self.cast_rays()

    

