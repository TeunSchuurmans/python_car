from settings import *

class NNet:
    def __init__(self, raycaster):
        self.raycaster = raycaster

    def predict(self, data):
        forward = False
        left = False
        right = False

        return forward, left, right