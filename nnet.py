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
        for x in self.weights['input_to_hidden']:
            print(x)
        print('test')

    def get_node_average(self, index, input_layer, weights):
        return sum(node[index] * weights[i][index] for i, node in enumerate(input_layer)) / len(input_layer)

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
        hidden_layer = [self.get_node_average(index, input_layer, self.weights['input_to_hidden']) for index, _ in enumerate(HIDDEN_LAYER_NEURONS)]

        return forward, left, right
