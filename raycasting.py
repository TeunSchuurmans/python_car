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

    def direction(self, angle):
        down = True if (math.pi / 2) < angle < (math.pi * 3 / 2) else False
        right = True if 0 < angle < math.pi else False
        return down, right

    def ray_pos(self, length, angle):
        return (math.sin(angle) * length, math.cos(angle) * length)
    def ray_collision(self, ray, angle):
        pos = self.ray_pos(ray, angle)
        return False

    def player_decimal(self, coord, bool):
        return coord % TILE_SIZE / TILE_SIZE if bool else TILE_SIZE - coord % TILE_SIZE

    #loop functions
    def cast_rays(self):
        for i, _ in enumerate(self.rays):

            angle = self.ray_angle(i)
            down, right = self.direction(angle)
            tan_a = math.tan(angle)
            start_tb = self.terrain.roads[Tile.current(self.npc.center)].borders

            """
            Horizontal
            """

            h_dx = TILE_SIZE * tan_a
            h_dy = TILE_SIZE
            hor_d = math.sqrt(h_dx ** 2 + h_dy ** 2) if down else -math.sqrt(h_dx ** 2 + h_dy ** 2)
            hor_length = self.player_decimal(self.npc.center[1], down) * hor_d

            """
            Vertical
            """

            v_dx = TILE_SIZE
            v_dy = 1 / tan_a * TILE_SIZE
            ver_d = math.sqrt(v_dx ** 2 + v_dy ** 2) if right else -math.sqrt(v_dx ** 2 + v_dy ** 2)
            ver_length = self.player_decimal(self.npc.center[1], down) * ver_d


            for x in DOF:
                    if hor_length <= ver_length:
                        if hor_length + hor_d > MAX_RAY_LENGTH or self.ray_collision(hor_length, angle):
                            break
                        else:
                            hor_length += hor_d
                    else:
                        if ver_length + ver_d > MAX_RAY_LENGTH or self.ray_collision(ver_length, angle):
                            break
                        else:
                            ver_length += ver_d

            self.rays[i] = min(hor_length, ver_length)

    def draw(self):
        for i, ray in enumerate(self.rays):
            end = (self.npc.center[0] + math.sin(self.ray_angle(i)) * -ray, self.npc.center[1] + math.cos(self.ray_angle(i)) * -ray)
            pg.draw.line(self.game.screen, 'white', self.npc.center, end, 2)
            pg.draw.circle(self.game.screen, 'red', end, 4)
            
    def update(self):
        self.cast_rays()

    

