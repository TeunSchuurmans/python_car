import pygame as pg
import math
from settings import * 



class Car:
    max_speed = MAX_SPEED
    acceleration = ACCELERATION 
    friction = FRICTION
    rotation_speed = ROTATION_SPEED
    cornering_speed = CORNERING_SPEED
    car_width = CAR_WIDTH
    car_height = CAR_HEIGHT


    def __init__(self, game, road):
        
        self.game = game
        self.road = road
        self.car = pg.transform.rotate(pg.transform.scale(pg.image.load(CAR_IMAGE), (Car.car_height, Car.car_width)), 90)
        self.x, self.y = road.start_pos
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0 

    @property
    def radians(self):
        return math.radians(self.angle)     

    #returns the current tile the car is on
    #for collision detection
    @property
    def car_center_x(self):
        return self.x + (Car.car_width / 2)

    @property
    def car_center_y(self):
        return self.y + (Car.car_height / 2)
       
    @property
    def current_tile(self):
        return (self.car_center_x // TILE_SIZE, self.car_center_y // TILE_SIZE)
    
    @property
    def left_tile_border(self):
        return self.current_tile[0] * 100

    @property
    def down_tile_border(self):
        return self.current_tile[1] * 100 + 100

    @property
    def right_tile_border(self):
        return self.current_tile[0] * 100 + 100

    @property
    def up_tile_border(self):
        return self.current_tile[1] * 100

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

        #self.speed *= self.game.delta_time
        dx, dy = 0, 0     

        if self.speed <= FRICTION:
            self.rotation_speed = 0
        else:
            self.rotation_speed = Car.rotation_speed / (1+ (self.speed / Car.cornering_speed))

        dx = math.sin(self.radians) * self.speed
        dy = math.cos(self.radians) * self.speed

        self.check_collision(dx, dy)    

    #for now the collision detection will only be for the center of the car
    #in the future, collision will "destroy" the car
    def check_collision(self, dx, dy):

        if self.current_tile in self.road.road_dict:
            match self.road.road_dict[self.current_tile[0], self.current_tile[1]]:
                #finish
                case 1:
                    if self.in_range(self.left_tile_border, self.right_tile_border , self.car_center_x - dx):
                        self.x -= dx
                    self.y -= dy
                #vertical
                case 2:
                    if self.in_range(self.left_tile_border, self.right_tile_border , self.car_center_x - dx):
                        self.x -= dx
                    self.y -= dy
                #horizontal
                case 3: 
                    if self.in_range(self.up_tile_border, self.down_tile_border , self.car_center_y - dy):
                        self.y -= dy
                    self.x -= dx
                #left->down
                case 4:
                    if self.in_range(self.up_tile_border, None, self.car_center_y - dy):
                        self.y -= dy
                    if self.in_range(None, self.right_tile_border, self.car_center_x - dx):
                        self.x -= dx
                #down->right
                case 5:
                    if self.in_range(self.up_tile_border, None, self.car_center_y - dy):
                        self.y -= dy
                    if self.in_range(self.left_tile_border, None, self.car_center_x - dx):
                        self.x -= dx
                #right->up
                case 6:
                    if self.in_range(None, self.down_tile_border, self.car_center_y - dy):
                        self.y -= dy
                    if self.in_range(self.left_tile_border, None, self.car_center_x - dx):
                        self.x -= dx
                #up->left
                case 7:
                    if self.in_range(None, self.down_tile_border, self.car_center_y - dy):
                        self.y -= dy
                    if self.in_range(None, self.right_tile_border, self.car_center_x - dx):
                      self.x -= dx

        #if a player is on grass, there is no collision               
        else:
            self.x -= dx
            self.y -=dy

    #checks if the car is between the 2 borders
    def in_range(self, min, max, pos):
        if max is None:
            return (min < pos)
        if min is None:
            return (max > pos)
        else:
            return (min < pos) and (max > pos)

    def draw(self): 
        
        #this makes sure the car rotates around its center
        rotated_car = pg.transform.rotate(self.car, self.angle)
        car_rect = rotated_car.get_rect(center=(self.car_center_x, self.car_center_y))

        self.game.screen.blit(rotated_car, car_rect.topleft)

    def update(self):
        self.listen_inputs()
        self.movement()