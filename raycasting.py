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
        return self.npc.angle - HALF_SPREAD + RAY_GAP * index

    def ray_length(self, side1, side2):
        return  math.sqrt(side1**2 + side2 **2) 

    #loop functions
    def cast_rays(self):
        for x, _ in enumerate(self.rays):
            pass

    def draw(self):
        pass
            
    def update(self):
        self.cast_rays()

    

