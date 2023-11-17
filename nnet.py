from settings import *
import random

class NNet:
    def __init__(self, wheights):
        pass

    def predict(self, data):
        input_1 = data['speed'] / MAX_SPEED
        input_2 = data['angle'] % 360 / 360
        input_3 = data['rotation speed'] / ROTATION_SPEED
        forward = True
        left = random.getrandbits(1)
        right = random.getrandbits(1)

        return forward, left, right
