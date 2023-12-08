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
        if P1:
            self.player_1 = Player1(self, self.terrain)
        if P2:
            self.player_2 = Player2(self, self.terrain)
        for i in NPC_AMOUNT:
            self.terrain.cars[i] = Npc(self, self.terrain, i)

    def update(self):
        self.terrain.update()
        if P1:
            self.player_1.update()
        if P2:
            self.player_2.update()
        for _, car in list(self.terrain.cars.items()):
            car.update()
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # shows the current fps

    def draw(self):
        self.terrain.draw()
        if P1:
            self.player_1.draw()
        if P2:
            self.player_2.draw()
        for key, car in list(self.terrain.cars.items()):
            car.draw()

    @staticmethod
    def check_events():
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
