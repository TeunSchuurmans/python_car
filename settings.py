import pygame as pg
import math

# game settings
RES = WIDTH, HEIGHT = 1600, 900
FPS = 144

# terrain settings
ROWS = 9
COLUMNS = 16
TILE_SIZE = 100
TILE_CENTER = TILE_SIZE / 2
TILE_IMAGES = {
    'grid': pg.transform.scale(pg.image.load('images/grid.png'), (TILE_SIZE, TILE_SIZE)),
    'grass': pg.transform.scale(pg.image.load('images/grass.png'), (TILE_SIZE, TILE_SIZE)),
    'finish': pg.transform.scale(pg.image.load('images/finish.png'), (TILE_SIZE, TILE_SIZE)),
    'ver': pg.transform.scale(pg.image.load('images/straight.png'), (TILE_SIZE, TILE_SIZE)),
    'hor': pg.transform.rotate(pg.transform.scale(pg.image.load('images/straight.png'), (TILE_SIZE, TILE_SIZE)), 90),
    'ld': pg.transform.rotate(pg.transform.scale(pg.image.load('images/straight_corner.png'), (TILE_SIZE, TILE_SIZE)), 270),
    'dr': pg.transform.scale(pg.image.load('images/straight_corner.png'), (TILE_SIZE, TILE_SIZE)),
    'ru': pg.transform.rotate(pg.transform.scale(pg.image.load('images/straight_corner.png'), (TILE_SIZE, TILE_SIZE)), 90),
    'ul': pg.transform.rotate(pg.transform.scale(pg.image.load('images/straight_corner.png'), (TILE_SIZE, TILE_SIZE)), 180),
}
SHOW_GRID = False

# car settings
CAR_WIDTH = TILE_SIZE / 6
CAR_HEIGHT = CAR_WIDTH * 2
P1 = True
P2 = False
P1_IMAGE = pg.transform.rotate(pg.transform.scale(pg.image.load('images/player_1.png'), (CAR_HEIGHT, CAR_WIDTH)), 90)
P2_IMAGE = pg.transform.rotate(pg.transform.scale(pg.image.load('images/player_2.png'), (CAR_HEIGHT, CAR_WIDTH)), 90)
NPC_IMAGE = pg.transform.rotate(pg.transform.scale(pg.image.load('images/npc.png'), (CAR_HEIGHT, CAR_WIDTH)), 90)
MAX_SPEED = 2
ACCELERATION = MAX_SPEED / 150
ROTATION_SPEED = 0.05
CORNERING_SPEED = ROTATION_SPEED * 15
FRICTION = MAX_SPEED / 150
BRAKE_SPEED = 1.01

# raycaster  settings
NUM_OF_RAYS = 5
MAX_RAY_LENGTH = 1000
RAY_SPREAD = math.pi
HALF_SPREAD = RAY_SPREAD / 2
RAY_GAP = RAY_SPREAD / (NUM_OF_RAYS - 1)
DOF = range(10)

# nnet settings
NPC_AMOUNT = 1
