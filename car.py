import pygame as pg
import math
from settings import * 



class Car:
    max_speed = MAX_SPEED
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
        

    #returns the current tile the car is on
    #for collision detection    
    @property
    def current_tile(self):
        return ((self.x + (CAR_WIDTH / 2)) // TILE_SIZE, (self.y + (CAR_HEIGHT / 2)) // TILE_SIZE)
    
    def listen_inputs(self):

        input = pg.key.get_pressed()

        if input[pg.K_w]:   
            self.speed = min(self.speed + Car.acceleration, Car.max_speed)
        else:               
            self.speed = max(self.speed - Car.friction, 0)

        if input[pg.K_s]:   #brake
            self.speed /= BRAKE_SPEED

        if input[pg.K_a]:
            self.angle += self.rotation_speed    #rotates the car to the left
            
        if input[pg.K_d]:
            self.angle -= self.rotation_speed    #rotates the car to the right

    def movement(self):

        #print(self.game.delta_time)
        #self.speed *= self.game.delta_time
        dx, dy = 0, 0     

        if self.speed <= FRICTION:
            self.rotation_speed = 0
        else:
            self.rotation_speed = Car.rotation_speed / (1+ (self.speed / Car.cornering_speed))

        radian = math.radians(self.angle)

        dx = math.sin(radian) * self.speed
        dy = math.cos(radian) * self.speed

        
        self.x -= dx                    
        self.y -= dy    

    #for now the collision detection will only be for the center of the car
    #in the future, collision will "destroy" the car
    def check_collision(self):
        pass

    def draw(self): 
        center_X = self.x + (Car.car_width / 2)
        center_Y = self.y + (Car.car_height / 2)

        #this makes sure the car rotates around its center
        rotated_car = pg.transform.rotate(self.car, self.angle)
        car_rect = rotated_car.get_rect(center=(center_X, center_Y))

        self.game.screen.blit(rotated_car, car_rect.topleft)
        pg.draw.circle(self.game.screen, 'white', (center_X, center_Y), 3)

    def update(self):
        self.listen_inputs()
        self.movement()
        print(self.current_tile) 