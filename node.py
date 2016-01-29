
""" Module containing a node of the Ising model (single spin) """

from random import random
from math import pi

import visual as v

class Node(object):
    def __init__(self):
        self._value = random() * 2 * pi
        self._model = v.frame()

        W = 0.1
        v.box(frame=self._model, pos=(+W / 2, 0, 0), size=(W, W, W), color=v.color.red)
        v.box(frame=self._model, pos=(-W / 2, 0, 0), size=(W, W, W),
            color=v.color.white)

        self._model.rotate(angle=self._value, axis=(0, 0, 1))

    def set(self, value):
        """ Sets the value and updates the model.

        Args:
            value: new value (float)
        """
        prev_value = self._value
        self._value = value

        self._model.rotate(angle=value - prev_value, axis=(0, 0, 1))

    def get(self):
        """ Gets the value and updates the model.

        Returns:
            float
        """
        return self._value

    def model(self):
        return self._model
