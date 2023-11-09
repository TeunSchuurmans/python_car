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
        self.delta_time = 1
        self.init_objects()

    def init_objects(self):
        self.road = Road(self)
        self.car = Npc(self, self.road)
    
    def update(self):
        self.car.update()
        pg.display.flip()  
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  #shows the current fps

    def draw(self):
        self.road.draw() 
        self.car.draw()

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
