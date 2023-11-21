"""
Code inspired by : TechWithTim
    Video title: Pygame Car Racing Tutorial #1 - Moving The Car 
    Video link: https://www.youtube.com/watch?v=L3ktUWfAMPg&t=31m4s 
Code inspired by: Dr. Radu Mariescu-Istodor
    Video title: Self-Driving Car with JavaScript Course - Neural Networks and Machine Learning
    Video link: https://www.youtube.com/watch?v=Rs_rAxEsAvI&t=3m44s
"""

from raycasting import *
from terrain import *


class Car:
    def __init__(self, game, terrain, image):
        self.game = game
        self.terrain = terrain
        self.image = image
        self.pos = self.x, self.y = terrain.start_pos
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

        self.handle_collision(dx, dy)

    def check_collision(self, dx, dy):
        tile = Tile.current(self.center)
        future_pos = (self.center[0] - dx, self.center[1] - dy)
        if tile in self.terrain.roads:
            return self.terrain.roads[tile].check_collision(future_pos)
        else:
            return True, True

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
    def __init__(self, game, terrain, index):
        self.image = NPC_IMAGE
        self.key = index
        self.raycaster = RayCaster(game, terrain, self)
        self.nnet = self.raycaster.nnet
        self.points = 0
        super().__init__(game, terrain, self.image)

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

    def handle_collision(self, dx, dy):
        hor, ver = self.check_collision(dx, dy)

        if not hor or not ver:
            self.delete()
        else:
            self.x -= dx
            self.y -= dy

    def draw(self):
        super().draw()
        self.raycaster.draw()

    def update(self):
        self.raycaster.update()
        self.listen_inputs()
        super().movement()


class Player(Car):

    def __init__(self, game, terrain, input_type, image):
        super().__init__(game, terrain, image)
        self.player_input = input_type

    def listen_inputs(self):
        player_input = pg.key.get_pressed()

        if player_input[self.player_input['forward']]:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        else:
            self.speed = max(self.speed - FRICTION, 0)
        if player_input[self.player_input['left']]:
            self.angle += self.rotation_speed
        if player_input[self.player_input['right']]:
            self.angle -= self.rotation_speed

    def handle_collision(self, dx, dy):
        hor, ver = self.check_collision(dx, dy)

        if hor:
            self.x -= dx
        if ver:
            self.y -= dy

    def update(self):
        self.listen_inputs()
        super().update()


class Player1(Player):
    def __init__(self, game, terrain):
        self.image = P1_IMAGE
        self.input_type = {
            'forward': pg.K_w,
            'right': pg.K_d,
            'left': pg.K_a,
        }
        super().__init__(game, terrain, self.input_type, self.image)


class Player2(Player):

    def __init__(self, game, road):
        self.image = P2_IMAGE
        self.input_type = {
            'forward': pg.K_UP,
            'right': pg.K_RIGHT,
            'left': pg.K_LEFT,
        }
        self.image = P2_IMAGE
        super().__init__(game, road, self.input_type, self.image)
