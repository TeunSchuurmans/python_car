from settings import *
import random

class NNet:
    def __init__(self, raycaster):
        self.raycaster = raycaster

    def __del__(self):
        print('deleted nnet')

    def predict(self, data):
        forward = random.getrandbits(1)
        left = random.getrandbits(1)
        right = random.getrandbits(1)

        return forward, left, right