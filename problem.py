
""" Module containing a Problem class, storing the state of a current
    graph and information about the running process.
"""

from random import random, choice
from math import exp, pi, sin, cos

import numpy as np

class Problem(object):

    TIMESTEP = 1.0 / 150000
    """ Amount of time to progress per iteration """

    def __init__(self, graph, temp):
        """ Initializes a Problem with a graph.

        Args:
            graph: Graph object
            temp: Temperature (in Hz)

        Returns:
            Problem object
        """
        self._graph = graph
        self._time = 0
        self._temp = temp

    def kinetic_factor(self, t=None):
        """ Return A(t), the kinetic coefficient, based on the current time.

        Args:
            t: float (optional time value between 0 and 1)

        Returns:
            float (Hz)
        """
        if not t:
            t = self._time
        return 3 * exp(-t * 7)

    def interaction_factor(self, t=None):
        """ Return B(t), the interaction coefficient, based on the current time.

        Args:
            t: float (optional time value between 0 and 1)

        Returns:
            float (Hz)
        """
        if not t:
            t = self._time
        return 0.1 * exp(t * 4)

    def hamiltonian(self):
        """ Returns the current energy.  The Hamiltonian is split into:

            - a kinetic term from the coupling between individual spins and
                an external magnetic field
            - an interaction term from the coupling between linked spins
                of the graph

            H(t) = -A(1) \sum_i sin i    -    B(1) \sum_{i<j} J_{ij} (cos i) (cos j)

            where A(1) and B(1) are coefficients determined by the annealing
            schedule.
        Returns:
            float (Frequency)
        """
        all_nodes = self._graph.all_nodes()
        all_edges = self._graph.all_edges()

        kinetic = 0
        for node in all_nodes:
            kinetic += sin(node.get())
        kinetic *= -self.kinetic_factor(1)

        interaction = 0
        for node_a, node_b in all_edges:
            coupling = self._graph.get_spin(node_a, node_b)
            interaction += coupling * cos(node_a.get()) * cos(node_b.get())
        interaction *= -self.interaction_factor(1)

        return kinetic + interaction

    def kick_probability(self, node, new_angle):
        """ Determine the probability that a node should be kicked.

        Args:
            node: Node object
            new_angle: angle

        Returns:
            probability between 0 and 1
        """

        theta = node.get()
        theta_prime = new_angle

        kinetic = sin(theta_prime) - sin(theta)
        kinetic *= -self.kinetic_factor()

        interaction = 0
        other_nodes = self._graph.all_nodes_connected_to_node(node)
        for other_node in other_nodes:
            coupling = self._graph.get_spin(node, other_node)
            other_theta = other_node.get()
            interaction += coupling * cos(other_theta)
        interaction *= cos(theta_prime) - cos(theta)
        interaction *= -self.interaction_factor()

        energy_delta = kinetic + interaction
        prob = np.exp(-energy_delta / self._temp)
        if prob < 0:
            return 0
        elif prob > 1:
            return 1
        else:
            return prob

    def iterate(self):
        # First determine which nodes should be kicked
        all_nodes = self._graph.all_nodes()
        kicks = []
        new_angles = []

        for node in all_nodes:
            new_angle = random() * 2 * pi
            prob = self.kick_probability(node, new_angle)
            kicks.append(random() < prob)
            new_angles.append(new_angle)

        # Then kick them
        for i, node in enumerate(all_nodes):
            if kicks[i]:
                node.set(new_angles[i])

        self._time += Problem.TIMESTEP

    def is_finished(self):
        """ Return whether problem is finished or not, based on time. """
        return self._time >= 1
