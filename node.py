
""" Module containing a node of the Ising model (single spin) """

from random import random
from math import pi

class Node(object):
    def __init__(self):
        self.value = random() * 2 * pi
        self._model = None

    def kick(self):
        """ Randomize spin """
        self.value = random() * 2 * pi
