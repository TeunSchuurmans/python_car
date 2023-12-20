from settings import *
import random
import json


class NNet:
    def __init__(self, npc, best_data):
        self.npc = npc
        self.best_weights = [x for x in best_data['weights']]
        self.weights = {}
        self.init_weights()

    def init_weights(self):
        if len(self.best_weights) == 1:
            print('got weights from database')
            self.weights['input_to_hidden'] = [[((self.best_weights[0]['input_to_hidden'][i][j] + self.best_weights[1]['input_to_hidden'][i][j]) / 2) + round(random.uniform(-0.1, 0.1), 11) for j in range(HIDDEN_LAYER_NEURONS)] for i in range(INPUT_NEURONS)]
            self.weights['hidden_to_output'] = [[((self.best_weights[0]['hidden_to_output'][i][j] + self.best_weights[1]['hidden_to_output'][i][j]) / 2) + round(random.uniform(-0.1, 0.1), 11) for j in range(OUTPUT_NEURONS)] for i in range(HIDDEN_LAYER_NEURONS)]
        else:
            self.weights['input_to_hidden'] = [[round(random.uniform(0.5, 1.7), 9) for _ in range(HIDDEN_LAYER_NEURONS)] for _ in range(INPUT_NEURONS)]
            self.weights['hidden_to_output'] = [[round(random.uniform(0.5, 1.7), 9) for _ in range(OUTPUT_NEURONS)] for _ in range(HIDDEN_LAYER_NEURONS)]

    @staticmethod
    def get_node_average(list_to_sum, weights):
        return sum(num * weights[i] for i, num in enumerate(list_to_sum)) / len(list_to_sum)

    def predict(self, data):

        input_layer = [
            data['speed'] / MAX_SPEED,
            data['angle'] / (math.pi * 2),
            data['rotation speed'] / ROTATION_SPEED,
        ] + [ray / MAX_RAY_LENGTH for ray in data['rays']]

        hidden_layer = [self.get_node_average(input_layer, [weight[index] for weight in self.weights['input_to_hidden']]) for index in range(HIDDEN_LAYER_NEURONS)]

        output_layer = [self.get_node_average(hidden_layer, [weight[index] for weight in self.weights['hidden_to_output']]) for index, _ in enumerate(range(OUTPUT_NEURONS))]

        return [value > 0.5 for value in output_layer]



