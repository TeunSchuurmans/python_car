"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=1m
"""

import pygame as pg
import sys
from settings import *
from car import *
from terrain import *
from raycasting import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.terrain = Terrain(self)
        self.car = Player(self, self.terrain)
        for i in range(NPC_AMOUNT):
            self.terrain.cars[i] = Npc(self, self.terrain, i)

    def update(self):
        self.car.update()
        for key, car in list(self.terrain.cars.items()):
            car.update()
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # shows the current fps

    def draw(self):
        self.terrain.draw()
        self.car.draw()
        for key, car in list(self.terrain.cars.items()):
            car.draw()

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
