import pygame as pg
import math
from settings import * 



class Car:
    max_speed = MAX_SPEED                       #defining the class constants
    acceleration = ACCELERATION 
    friction = FRICTION
    rotation_speed = ROTATION_SPEED

    def __init__(self):
        self.x, self.y = CAR_POSITION
        self.angle = 0
        self.speed = 0

    def movement(self):

        dx, dy = 0, 0                           #delta x and delta y

        input = pg.key.get_pressed()

        if input[pg.K_w]:                       #if the W key is pressed, the speed will increment by the acceleration
            if self.speed < Car.max_speed:      #makes sure the speed can't be higher than the max speed
                self.speed += Car.acceleration
        else:                                   #if the W key is not pressed, the speed will decrement by the acceleration
            if self.speed > 0:                  #makes sure the car's speed is higher than 0
                self.speed -= Car.acceleration
        
        if input[pg.K_a]:
            self.angle -= Car.rotation_speed    #rotates the car to the left
        if input[pg.K_d]:
            self.angle += Car.rotation_speed    #rotates the car to the right

        self.x += dx                            #adds the X increment to the car's X position                       
        self.y += dy                            #adds the Y increment to the car's Y position
        
    def update(self):
        self.movement()