import pygame as pg
import math
from settings import *
from raycasting import *

class Car:
    def __init__(self, game, road):
        self.game = game
        self.road = road
        self.raycaster = RayCaster(self.game, self.road, self)
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(CAR_IMAGE), (CAR_HEIGHT, CAR_WIDTH)), 90)
        self.x, self.y = road.start_pos
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0

    #utility functions
    def in_range(self, min, max, pos):
        if max is None:
            return (min < pos)
        if min is None:
            return (max > pos)
        else:
            return (min < pos) and (max > pos)
    
    #collision detection properties
    @property
    def current_tile(self):
        return (self.center[0] // TILE_SIZE, self.center[1] // TILE_SIZE)

    @property
    def center(self):
        return (self.x + (CAR_WIDTH / 2), self.y + (CAR_HEIGHT / 2))

    @property
    def left_tile_border(self):
        return self.current_tile[0] * TILE_SIZE

    @property
    def down_tile_border(self):
        return self.current_tile[1] * TILE_SIZE + TILE_SIZE

    @property
    def right_tile_border(self):
        return self.current_tile[0] * TILE_SIZE + TILE_SIZE

    @property
    def up_tile_border(self):
        return self.current_tile[1] * TILE_SIZE

    #loop functions
    def listen_inputs(self):

        input = pg.key.get_pressed()

        #go forward
        if input[pg.K_w]:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        else:
            self.speed = max(self.speed - FRICTION, 0)

        #rotate left
        if input[pg.K_a]:
            self.angle += self.rotation_speed

        #rotate right
        if input[pg.K_d]:
            self.angle -= self.rotation_speed

    def movement(self):
        #print(self.game.delta_time)
        #self.speed *= self.game.delta_time

        if self.speed <= FRICTION:
            self.rotation_speed = 0
        else:
            self.rotation_speed = ROTATION_SPEED / (1+ (self.speed / CORNERING_SPEED))

        radian = math.radians(self.angle)
        dx = math.sin(radian) * self.speed
        dy = math.cos(radian) * self.speed

        self.check_collision(dx, dy)

    def check_collision(self, dx, dy):

        if self.current_tile in self.road.road_dict:
            match self.road.road_dict[self.current_tile[0], self.current_tile[1]]:
                #finish
                case 1:
                    if self.in_range(self.left_tile_border, self.right_tile_border , self.center[0] - dx):
                        self.x -= dx
                    self.y -= dy
                #vertical
                case 2:
                    if self.in_range(self.left_tile_border, self.right_tile_border , self.center[0] - dx):
                        self.x -= dx
                    self.y -= dy
                #horizontal
                case 3:
                    if self.in_range(self.up_tile_border, self.down_tile_border , self.center[1] - dy):
                        self.y -= dy
                    self.x -= dx
                #left->down
                case 4:
                    if self.in_range(self.up_tile_border, None, self.center[1] - dy):
                        self.y -= dy
                    if self.in_range(None, self.right_tile_border, self.center[0] - dx):
                        self.x -= dx
                #down->right
                case 5:
                    if self.in_range(self.up_tile_border, None, self.center[1] - dy):
                        self.y -= dy
                    if self.in_range(self.left_tile_border, None, self.center[0] - dx):
                        self.x -= dx
                #right->up
                case 6:
                    if self.in_range(None, self.down_tile_border, self.center[1] - dy):
                        self.y -= dy
                    if self.in_range(self.left_tile_border, None, self.center[0] - dx):
                        self.x -= dx
                #up->left
                case 7:
                    if self.in_range(None, self.down_tile_border, self.center[1] - dy):
                        self.y -= dy
                    if self.in_range(None, self.right_tile_border, self.center[0] - dx):
                      self.x -= dx

        #if a player is on grass, there is no collision to check
        else:
            self.x -= dx
            self.y -=dy

    def draw(self):

        #makes sure the car rotates around its center
        rotated_car = pg.transform.rotate(self.image, self.angle)
        car_rect = rotated_car.get_rect(center=(self.center))

        self.game.screen.blit(rotated_car, car_rect.topleft)

        self.raycaster.draw()

    def update(self):
        self.listen_inputs()
        self.movement()
        self.raycaster.update()