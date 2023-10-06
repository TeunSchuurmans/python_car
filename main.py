import pygame as pg
import sys
from settings import *
from car import *
from road import *


class Game:
    def __init__(self):
        pg.init()   #initializes pygame
        self.screen = pg.display.set_mode(RES)  #sets the screen resolution
        self.clock = pg.time.Clock()    #creates an instance of Clock()
        self.new_game()

    def new_game(self):
        self.car = Car(self)
        self.road = Road(self)

    def update(self):
        self.car.update()
        pg.display.flip()   #updates the screen
        self.clock.tick(FPS)    # adds a delay
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')    #draws the screen black
        #self.road.draw() 
        self.car.draw()
        

    def check_events(self): #listens for events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                pg.quit()   #stops pygame
                sys.exit()  #stops the program


    def run(self): #main game loop
        while True:
            self.check_events()
            self.update()
            self.draw()
        

if __name__ == '__main__':
    game = Game()   #creates an instance of the Game  class
    game.run()  #calls the run function inside of the Game class

        