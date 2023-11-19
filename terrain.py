"""
Code inspired by : Coder Space
    Video title: Creating a DOOM (Wolfenstein) - style 3D Game in Python
    Video link: https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=2m43s
"""

from utils import *


class Terrain:
    def __init__(self, game):
        self.game = game
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.roads = {}
        self.cars = {}
        self.start_pos = WIDTH / 2, HEIGHT / 2
        self.generate_road()

    def clear_tiles(self):
        self.tile_map = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.roads.clear()

    # terrain generating algorithm. STILL IN PROGRESS!!!
    def generate_road(self):
        self.clear_tiles()

        # temporary tile map
        self.tile_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 3, 3, 4, 0, 0, 0, 0, 5, 3, 3, 3, 3, 4, 0],
            [0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 5, 3, 3, 7, 0],
            [0, 1, 0, 0, 6, 3, 3, 4, 0, 2, 0, 2, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 6, 3, 3, 4, 0],
            [0, 6, 3, 3, 4, 0, 0, 2, 0, 6, 3, 3, 4, 0, 2, 0],
            [0, 0, 0, 0, 2, 0, 0, 6, 3, 3, 3, 3, 7, 0, 2, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 0],
        ]

        self.init_road_surface()

    # initializes tiles from tile_map onto the terrain surface
    def init_road_surface(self):
        for row_i, row in enumerate(self.tile_map):
            for col_i, tile in enumerate(row):
                key = (col_i, row_i)
                pos = (col_i * TILE_SIZE, row_i * TILE_SIZE)
                if tile:
                    self.roads[key] = Tile(self, pos, tile)
                else:
                    Tile(self, pos, tile)

    def draw(self):
        self.game.screen.blit(self.surface, (0, 0))


class Tile:
    def __init__(self, terrain, pos, key):
        self.terrain = terrain
        self.key = key
        self.pos = self.x, self.y = pos
        self.type = ''
        self.borders = self.borders()
        self.image = TILE_IMAGES[self.type]
        self.draw_on_surface()

    @property
    def border(self):
        return {
            'left': self.x,
            'down': self.y + TILE_SIZE,
            'right': self.x + TILE_SIZE,
            'up': self.y,
        }

    def borders(self):
        match self.key:
            case 1:
                self.terrain.start_pos = self.x + TILE_CENTER - (CAR_WIDTH / 2), self.y + TILE_CENTER - (CAR_HEIGHT / 2)
                self.type = 'finish'
                return (self.border['left'], self.border['right']), (None, None)
            case 2:
                self.type = 'ver'
                return (self.border['left'], self.border['right']), (None, None)
            case 3:
                self.type = 'hor'
                return (None, None), (self.border['up'], self.border['down'])
            case 4:
                self.type = 'ld'
                return (None, self.border['right']), (self.border['up'], None)
            case 5:
                self.type = 'dr'
                return (self.border['left'], None), (self.border['up'], None)
            case 6:
                self.type = 'ru'
                return (self.border['left'], None), (None, self.border['down'])
            case 7:
                self.type = 'ul'
                return (None, self.border['right']), (None, self.border['down'])
            case 0:
                self.type = 'grass'
                return (None, None), (None, None)

    def check_collision(self, pos):
        hor = False
        ver = False
        if Utils.in_range(self.borders[0], pos[0]):
            hor = True
        if Utils.in_range(self.borders[1], pos[1]):
            ver = True

        return hor, ver

    def draw_on_surface(self):
        self.terrain.surface.blit(self.image, self.pos)


