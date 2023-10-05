import pygame as pg
import math
from settings import * 



class Car:
    max_speed = MAX_SPEED   #defining the class constants
    acceleration = ACCELERATION 
    friction = FRICTION
    car_width = 25
    car_height = 50
    car_image = pg.transform.rotate(pg.transform.scale(pg.image.load(CAR_IMAGE), (car_height, car_width)), 90)


    def __init__(self, game):
        
        self.game = game
        self.x, self.y = CAR_POSITION
        self.angle = 0
        self.speed = 0
        self.rotation_speed = ROTATION_SPEED

    def movement(self):

        dx, dy = 0, 0   #delta x and delta y

        self.rotation_speed = (self.speed/13)/self.friction

        input = pg.key.get_pressed()

        if input[pg.K_w]:   #if the W key is pressed, the speed will increment by the acceleration
            self.speed = min(self.speed + Car.acceleration, Car.max_speed)
        else:               #if the W key is not pressed, the speed will decrement by the friction
            self.speed = max(self.speed - Car.friction, 0)

        if input[pg.K_s]:   #brakes
            self.speed /= 1.01
        
        if input[pg.K_a]:
            self.angle += self.rotation_speed    #rotates the car to the left
            
        if input[pg.K_d]:
            self.angle -= self.rotation_speed    #rotates the car to the right
            

        radian = math.radians(self.angle)                  #converts the angle into a radiant

        dx = math.sin(radian) * self.speed
        dy = math.cos(radian) * self.speed

        if self.x >= WIDTH + Car.car_width:
            self.x = 0

        if self.x <= 0 - Car.car_width:
            self.x = WIDTH

        if self.y >= HEIGHT + Car.car_height:
            self.y = 0

        if self.y <= 0 - Car.car_height:
            self.y = HEIGHT

        self.x -= dx    #adds the X increment to the car's X position                       
        self.y -= dy    #adds the Y increment to the car's Y position

    def draw(self): 
        center_X = self.x + (Car.car_width / 2)
        center_Y = self.y + (Car.car_height / 2)

        rotated_image = pg.transform.rotate(Car.car_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(center_X, center_Y))

        self.game.screen.blit(rotated_image, rotated_rect.topleft)
        
    def update(self):
        self.movement()