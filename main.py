"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=1m
"""

import pygame as pg
import sys
from settings import *
from car import *
from road import *
from raycasting import *

class Game:
    def __init__(self):
        pg.init()   
        self.screen = pg.display.set_mode(RES)  
        self.clock = pg.time.Clock()
        self.init_objects()

    def init_objects(self):
        self.road = Road(self)
        self.car = Player(self, self.road)
        for _ in range(NPC_AMOUNT):
            self.road.cars.append(Npc(self, self.road))

    def update(self):
        self.car.update()
        for x in self.road.cars:
            x.update()
        pg.display.flip()  
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  #shows the current fps

    def draw(self):
        self.road.draw() 
        self.car.draw()
        for x in self.road.cars:
            x.draw()

    def check_events(self): 
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                pg.quit()   
                sys.exit()  

    def main_loop(self): 
        while True:
            self.check_events()
            self.update()
            self.draw()
        
if __name__ == '__main__':
    game = Game()
    game.main_loop() 
