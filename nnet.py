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

    def get_node_average(self, list_to_sum, weights):
        return sum(num * weights[i] for i, num in enumerate(list_to_sum)) / len(list_to_sum)

    def predict(self, data):

        forward = random.getrandbits(1)
        left = random.getrandbits(1)
        right = random.getrandbits(1)

        input_layer = [
            data['speed'] / MAX_SPEED,
            data['angle'] / (math.pi * 2),
            data['rotation speed'] / ROTATION_SPEED,
        ] + [ray / MAX_RAY_LENGTH for ray in data['rays']]

        hidden_layer = [self.get_node_average([1], [1]) for index, _ in enumerate(HIDDEN_LAYER_NEURONS)]

        return forward, left, right
