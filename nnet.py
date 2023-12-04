import math

from settings import *
import random


class NNet:
    def __init__(self, npc):
        self.npc = npc
        self.weights = []

    def predict(self, data):

        """
        data input looks like this:

        {
            'speed': self.speed,
            'angle': self.angle,
            'rotation speed': self.rotation_speed,
            'rays': self.raycaster.rays,
        }

        """

        forward = False
        left = False
        right = False
        print(data['angle'] / (math.pi * 2))
        input_layer = [
            data['speed'] / MAX_SPEED,
            data['angle'] / (math.pi * 2),
            data['rotation speed'] / ROTATION_SPEED,
        ] + [ray / MAX_RAY_LENGTH for ray in data['rays']]

        return forward, left, right
