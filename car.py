import pygame as pg
import math
from settings import * 



class Car:
    max_speed = MAX_SPEED   #defining the class constants
    acceleration = ACCELERATION 
    friction = FRICTION
    rotation_speed = ROTATION_SPEED
    cornering_speed = 11
    car_width = CAR_WIDTH
    car_height = CAR_HEIGHT


    def __init__(self, game, start_pos):
        
        self.game = game
        self.car = pg.transform.rotate(pg.transform.scale(pg.image.load(CAR_IMAGE), (Car.car_height, Car.car_width)), 90)
        self.x, self.y = start_pos
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0
        

    def listen_inputs(self):

        input = pg.key.get_pressed()

        if input[pg.K_w]:   #if the W key is pressed, the speed will increment by the acceleration
            self.speed = min(self.speed + Car.acceleration, Car.max_speed)
        else:               #if the W key is not pressed, the speed will decrement by the friction
            self.speed = max(self.speed - Car.friction, 0)

        if input[pg.K_s]:   #brakes
            self.speed /= BRAKE_SPEED

        if input[pg.K_a]:
            self.angle += self.rotation_speed    #rotates the car to the left
            
        if input[pg.K_d]:
            self.angle -= self.rotation_speed    #rotates the car to the right

    def movement(self):

        #print(self.game.delta_time)
        #self.speed *= self.game.delta_time
        dx, dy = 0, 0   #delta x and delta y  

        if self.speed <= FRICTION:
            self.rotation_speed = 0
        else:
            self.rotation_speed = Car.rotation_speed / (1+ (self.speed / Car.cornering_speed))

        radian = math.radians(self.angle)   #converts the angle into a radiant

        dx = math.sin(radian) * self.speed
        dy = math.cos(radian) * self.speed

        self.x -= dx    #adds the X increment to the car's X position                       
        self.y -= dy    #adds the Y increment to the car's Y position

        self.check_collision(dx, dy)

    def check_collision(self, dx, dy):
        return True not in self.game.road.road_dict
        

    def draw(self): 
        center_X = self.x + (Car.car_width / 2) #gets the center coordinate of the car
        center_Y = self.y + (Car.car_height / 2)

        rotated_car = pg.transform.rotate(self.car, self.angle) #rotates the car by the angle
        car_rect = rotated_car.get_rect(center=(center_X, center_Y)) #gets the center coordinate of the rotated car

        self.game.screen.blit(rotated_car, car_rect.topleft)
        
    def update(self):
        self.listen_inputs()
        self.movement()