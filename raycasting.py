import pygame as pg

class Raycaster:
    def __init__(self, game, car) -> None:
        self.game = game
        self.car = car
        self.rays = []
        self.num_rays = 5
        self.car_fov = 180
        self.init_rays()

    def init_rays(self):
        for x in range(self.num_rays):       
            self.rays.append(pg.draw.line(self.game.screen,'yellow',(self.car.x, self.car.y),(self.car.x + 100, self.car.y + 100),1))
