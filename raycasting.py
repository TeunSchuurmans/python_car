import pygame as pg

class Raycaster:
    def __init__(self, game, car) -> None:
        self.game = game
        self.car = car
        self.rays = []
        self.num_rays = 5
        self.car_fov = 180

    def draw(self):
        for x in range(self.num_rays):
            pg.draw.line(
                self.game.screen,
                'yellow',
                (self.car.car_center_x, self.car.car_center_y),
                (self.car.car_center_x + 100, self.car.car_center_y + 100),
                3)
            
    def update(self):
        pass
    

