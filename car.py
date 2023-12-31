"""
Code inspired by : TechWithTim
    Video title: Pygame Car Racing Tutorial #1 - Moving The Car 
    Video link: https://www.youtube.com/watch?v=L3ktUWfAMPg&t=31m4s 
Code inspired by: Dr. Radu Mariescu-Istodor
    Video title: Self-Driving Car with JavaScript Course - Neural Networks and Machine Learning
    Video link: https://www.youtube.com/watch?v=Rs_rAxEsAvI&t=3m44s
"""


import json
from raycasting import *
from terrain import *


class Car:
    def __init__(self, game, terrain, image):
        self.game = game
        self.terrain = terrain
        self.image = image
        self.x, self.y = terrain.start_pos
        self.angle = 1e-10
        self.speed = 0
        self.rotation_speed = 0
        self.tiles_visited = {key: False for key in self.terrain.roads}
        self.driving = False
        self.total_time = 1
        self.lap_time = 1
        self.laps = []
        self.distance = 0

    @property
    def center(self):
        return self.x + (CAR_WIDTH / 2), self.y + (CAR_HEIGHT / 2)

    # loop functions
    def handle_inputs(self, forward, left, right):
        if forward:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
        else:
            self.speed = max(self.speed - FRICTION, 0)
        if left:
            self.angle = (self.angle + self.rotation_speed) % (math.pi * 2)
        if right:
            self.angle = (self.angle - self.rotation_speed) % (math.pi * 2)

        self.distance += self.speed
        
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

    def tick_timer(self):
        self.total_time += 1
        self.lap_time += 1

    def mark_tiles(self):
        self.tiles_visited[self.center] = True

    def check_laps(self):
        if self.terrain.roads[Tile.current(self.center)].type == 'finish' and all(
                value for value in self.tiles_visited.values()):
            self.laps.append(self.lap_time)
            self.lap_time = 0
            self.tiles_visited = {key: False for key in self.tiles_visited}

    def draw(self):

        # rotates the car around its center
        rotated_car = pg.transform.rotate(self.image, math.degrees(self.angle))
        car_rect = rotated_car.get_rect(center=self.center)

        self.game.screen.blit(rotated_car, car_rect.topleft)

    def update(self):
        self.movement()
        self.tick_timer()
        self.mark_tiles()
        self.check_laps()


class Npc(Car):
    def __init__(self, game, terrain, index, weights):
        self.image = CAR_IMAGES['npc']
        self.key = index
        self.raycaster = RayCaster(game, terrain, self)
        self.nnet = NNet(self, weights)
        super().__init__(game, terrain, self.image)

    def delete(self):
        del self.terrain.npc_list[self.key]
        self.terrain.db_data_list.append(self.db_data)

    @property
    def nnet_data(self):
        return {
            'speed': self.speed,
            'angle': self.angle,
            'rotation speed': self.rotation_speed,
            'rays': self.raycaster.rays,
        }

    @property
    def db_data(self):
        avg_speed = round(self.distance / self.total_time, 2)
        time_alive = self.total_time
        hit_wall = False

        return {
            'generation': 0,
            'points': Npc.calc_points(avg_speed, time_alive, hit_wall, len(self.laps)),
            'timeAlive': time_alive,
            'lapTime': sorted(self.laps)[0] if len(self.laps) > 0 else None,
            'avgSpeed': avg_speed,
            'hitWall': hit_wall,
            'weights': json.dumps(self.nnet.weights),
        }

    @staticmethod
    def calc_points(avg_speed, time_alive, hit_wall, laps_completed):
        base_points = 0

        time_alive_bonus = time_alive * 5

        hit_wall = 200 if hit_wall else 0

        lap_bonus = laps_completed * 200

        speed_penalty = max(0, 50 - avg_speed)

        total_points = base_points + lap_bonus + time_alive_bonus - speed_penalty - hit_wall

        return max(0, total_points)

    # loop functions
    def check_inputs(self):
        forward, left, right = self.nnet.predict(self.nnet_data)
        self.handle_inputs(forward, left, right)

    def handle_collision(self, dx, dy):
        hor, ver = self.check_collision(dx, dy)

        if not hor or not ver:
            self.db_data['hitWall'] = True
            self.delete()
        else:
            self.x -= dx
            self.y -= dy

    def check_if_completed_two_laps(self):
        if len(self.laps) >= 2:
            self.delete()

    def check_if_dnf(self):
        if self.total_time >= 10*FPS:
            self.delete()
    
    def draw(self):
        super().draw()
        self.raycaster.draw()

    def update(self):
        super().update()
        self.check_if_completed_two_laps()
        self.check_if_dnf()
        self.raycaster.update()
        self.check_inputs()


class Player(Car):

    def __init__(self, game, terrain, input_type, image):
        super().__init__(game, terrain, image)
        self.player_input = input_type

    def check_inputs(self):
        forward = False
        left = False
        right = False
        player_input = pg.key.get_pressed()

        if player_input[self.player_input['forward']]:
            forward = True
        if player_input[self.player_input['left']]:
            left = True
        if player_input[self.player_input['right']]:
            right = True

        self.handle_inputs(forward, left, right)

    def handle_collision(self, dx, dy):
        hor, ver = self.check_collision(dx, dy)

        if hor:
            self.x -= dx
        if ver:
            self.y -= dy

    def update(self):
        self.check_inputs()
        super().update()

    def draw(self):
        super().draw()


class Player1(Player):
    def __init__(self, game, terrain):
        self.image = CAR_IMAGES['p1']
        self.input_type = {
            'forward': pg.K_w,
            'right': pg.K_d,
            'left': pg.K_a,
        }
        super().__init__(game, terrain, self.input_type, self.image)


class Player2(Player):

    def __init__(self, game, road):
        self.image = CAR_IMAGES['p2']
        self.input_type = {
            'forward': pg.K_UP,
            'right': pg.K_RIGHT,
            'left': pg.K_LEFT,
        }
        super().__init__(game, road, self.input_type, self.image)
    