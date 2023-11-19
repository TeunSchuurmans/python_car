"""
Code inspired by : TechWithTim
    Video title: Pygame Car Racing Tutorial #1 - Moving The Car 
    Video link: https://www.youtube.com/watch?v=L3ktUWfAMPg&t=31m4s 
Code inspired by: Dr. Radu Mariescu-Istodor
    Video title: Self-Driving Car with JavaScript Course - Neural Networks and Machine Learning
    Video link: https://www.youtube.com/watch?v=Rs_rAxEsAvI&t=3m44s
"""


from raycasting import *
from utils import *


class Car:
    def __init__(self, game, terrain):
        self.game = game
        self.terrain = terrain
        self.image = CAR_IMAGE
        self.x, self.y = terrain.start_pos
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0

    @property
    def center(self):
        return self.x + (CAR_WIDTH / 2), self.y + (CAR_HEIGHT / 2)

    # loop functions
    def movement(self):
        if self.speed <= FRICTION:
            self.rotation_speed = 0
        else:
            self.rotation_speed = ROTATION_SPEED / (1 + (self.speed / CORNERING_SPEED))

        dx = math.sin(self.angle) * self.speed
        dy = math.cos(self.angle) * self.speed

        self.check_collision(dx, dy)

    def check_status(self):
        pass

    def draw(self):

        # rotates the car around its center
        rotated_car = pg.transform.rotate(self.image, math.degrees(self.angle))
        car_rect = rotated_car.get_rect(center=self.center)

        self.game.screen.blit(rotated_car, car_rect.topleft)

    def update(self):
        self.movement()


class Npc(Car):
    def __init__(self, game, road, index):
        super().__init__(game, road)
        self.key = index
        self.raycaster = RayCaster(self.game, self.terrain, self)
        self.nnet = self.raycaster.nnet
        self.points = 0

    @property
    def input_data(self):
        return {
            'speed': self.speed,
            'angle': self.angle,
            'rotation speed': self.rotation_speed,
            'rays': self.raycaster.rays,
        }

    def delete(self):
        del self.terrain.cars[self.key]

    def listen_inputs(self):
        forward, left, right = self.nnet.predict(self.input_data)

        if forward:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        else:
            self.speed = max(self.speed - FRICTION, 0)

        if left:
            self.angle += self.rotation_speed

        if right:
            self.angle -= self.rotation_speed

    def check_collision(self, dx, dy):
        if Utils.Tile.current(self.center) in self.terrain.roads:
            delete = False
            match self.terrain.roads[Utils.Tile.current(self.center)]:
                # finish
                case 1:
                    if not Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        delete = True
                    else:
                        self.x -= dx
                    self.y -= dy
                # vertical
                case 2:
                    if not Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        delete = True
                    else:
                        self.x -= dx
                    self.y -= dy
                # horizontal
                case 3:
                    if not Utils.in_range(
                            Utils.Tile.up_border(self.center),
                            Utils.Tile.down_border(self.center),
                            self.center[1] - dy):
                        delete = True
                    else:
                        self.y -= dy
                    self.x -= dx
                # left->down
                case 4:
                    if not Utils.in_range(
                            Utils.Tile.up_border(self.center),
                            None,
                            self.center[1] - dy):
                        delete = True
                    else:
                        self.y -= dy
                    if not Utils.in_range(
                            None,
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        delete = True
                    else:
                        self.x -= dx
                # down->right
                case 5:
                    if not Utils.in_range(
                            Utils.Tile.up_border(self.center),
                            None,
                            self.center[1] - dy):
                        delete = True
                    else:
                        self.y -= dy
                    if not Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            None,
                            self.center[0] - dx):
                        delete = True
                    else:
                        self.x -= dx
                # right->up
                case 6:
                    if not Utils.in_range(
                            None,
                            Utils.Tile.down_border(self.center),
                            self.center[1] - dy):
                        delete = True
                    else:
                        self.y -= dy
                    if not Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            None,
                            self.center[0] - dx):
                        delete = True
                    else:
                        self.x -= dx
                # up->left
                case 7:
                    print('case 7')
                    if not Utils.in_range(
                            None,
                            Utils.Tile.down_border(self.center),
                            self.center[1] - dy):
                        delete = True
                    else:
                        self.y -= dy
                    if not Utils.in_range(
                            None,
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        delete = True
                    else:
                        self.x -= dx

        # player is on grass or no tile
        else:
            self.x -= dx
            self.y -= dy
        if delete:
            self.delete()

    def movement(self):
        super().movement()

    def draw(self):
        super().draw()
        self.raycaster.draw()

    def update(self):
        self.raycaster.update()
        self.listen_inputs()
        self.movement()


class Player(Car):
    def listen_inputs(self):
        player_input = pg.key.get_pressed()

        if player_input[pg.K_w]:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        else:
            self.speed = max(self.speed - FRICTION, 0)

        if player_input[pg.K_a]:
            self.angle += self.rotation_speed

        if player_input[pg.K_d]:
            self.angle -= self.rotation_speed

    def check_collision(self, dx, dy):
        if Utils.Tile.current(self.center) in self.terrain.roads:
            match self.terrain.roads[Utils.Tile.current(self.center)]:
                # finish
                case 1:
                    if Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        self.x -= dx
                    self.y -= dy
                # vertical
                case 2:
                    if Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        self.x -= dx
                    self.y -= dy
                # horizontal
                case 3:
                    if Utils.in_range(
                            Utils.Tile.up_border(self.center),
                            Utils.Tile.down_border(self.center),
                            self.center[1] - dy):
                        self.y -= dy
                    self.x -= dx
                # left->down
                case 4:
                    if Utils.in_range(
                            Utils.Tile.up_border(self.center),
                            None,
                            self.center[1] - dy):
                        self.y -= dy
                    if Utils.in_range(
                            None,
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        self.x -= dx
                # down->right
                case 5:
                    if Utils.in_range(
                            Utils.Tile.up_border(self.center),
                            None,
                            self.center[1] - dy):
                        self.y -= dy
                    if Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            None,
                            self.center[0] - dx):
                        self.x -= dx
                # right->up
                case 6:
                    if Utils.in_range(
                            None,
                            Utils.Tile.down_border(self.center),
                            self.center[1] - dy):
                        self.y -= dy
                    if Utils.in_range(
                            Utils.Tile.left_border(self.center),
                            None,
                            self.center[0] - dx):
                        self.x -= dx
                # up->left
                case 7:
                    if Utils.in_range(
                            None,
                            Utils.Tile.down_border(self.center),
                            self.center[1] - dy):
                        self.y -= dy
                    if Utils.in_range(
                            None,
                            Utils.Tile.right_border(self.center),
                            self.center[0] - dx):
                        self.x -= dx

        # player is on grass or no tile
        else:
            self.x -= dx
            self.y -= dy

    def update(self):
        self.listen_inputs()
        super().update()

