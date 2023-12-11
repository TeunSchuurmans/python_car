import math

from settings import *
import random


class NNet:
    def __init__(self, npc, weights):
        self.npc = npc
        self.weights = {}
        self.bias = round(random.uniform(0.0, 0.1), 9)
        self.init_weights()

    def init_weights(self):
        self.weights['input_to_hidden'] = [[round(random.uniform(0.0, 1.7), 9) for _ in range(HIDDEN_LAYER_NEURONS)] for _ in range(INPUT_NEURONS)]
        self.weights['hidden_to_output'] = [[round(random.uniform(0.0, 1.7), 9) for _ in range(OUTPUT_NEURONS)] for _ in range(HIDDEN_LAYER_NEURONS)]

    def get_node_average(self, list_to_sum, weights):
        return sum(num * weights[i] for i, num in enumerate(list_to_sum)) / len(list_to_sum) + self.bias

    def predict(self, data):

        input_layer = [
            data['speed'] / MAX_SPEED,
            data['angle'] / (math.pi * 2),
            data['rotation speed'] / ROTATION_SPEED,
        ] + [ray / MAX_RAY_LENGTH for ray in data['rays']]

        hidden_layer = [self.get_node_average(input_layer, [weight[index] for weight in self.weights['input_to_hidden']]) for index in range(HIDDEN_LAYER_NEURONS)]

        output_layer = [self.get_node_average(hidden_layer, [weight[index] for weight in self.weights['hidden_to_output']]) for index, _ in enumerate(range(OUTPUT_NEURONS))]

        # print(output_layer)

        return [value > 0.5 for value in output_layer]


