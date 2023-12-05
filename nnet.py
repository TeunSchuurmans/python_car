import math

from settings import *
import random


class NNet:
    def __init__(self, npc):
        self.npc = npc
        self.weights = {
            'input_to_hidden': [[round(random.uniform(0.0, 1.0), 9) for _ in HIDDEN_LAYER_NEURONS]for _ in range(INPUT_NEURONS)],
            'hidden_to_output': [[round(random.uniform(0.0, 1.0), 9) for _ in OUTPUT_NEURONS] for _ in HIDDEN_LAYERS],
        }


    def get_average(self, index, value, node_amount):
        value = 0
        for i, x in range(node_amount):
            value += 0
        value /= node_amount
        return value

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

        forward = random.getrandbits(1)
        left = random.getrandbits(1)
        right = random.getrandbits(1)

        input_layer = [
            data['speed'] / MAX_SPEED,
            data['angle'] / (math.pi * 2),
            data['rotation speed'] / ROTATION_SPEED,
        ] + [ray / MAX_RAY_LENGTH for ray in data['rays']]
        hidden_layer = [self.get_average(index, value, INPUT_NEURONS) for index, value in enumerate(input_layer)]

        print(self.weights)

        return forward, left, right
