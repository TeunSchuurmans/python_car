from settings import *
import random

class NNet:
    def __init__(self, raycaster):
        self.raycaster = raycaster

    def predict(self, data):
        forward = True
        left = random.getrandbits(1)
        right = random.getrandbits(1)

        return forward, left, right