
""" Module containing a Problem class, storing the state of a current
    graph and information about the running process.
"""

from math import exp

class Problem(object):

    TIMESTEP = 0.01
    """ Amount of time to progress per iteration """

    def __init__(self, graph, temp):
        """ Initializes a Problem with a graph.

        Args:
            graph: Graph object
            temp: Temperature (in Kelvin)

        Returns:
            Problem object
        """
        self._graph = graph
        self._time = 0
        self._temp = temp

    def kinetic_factor(self):
        """ Return A(t), the kinetic coefficient, based on the current time.

        Returns:
            float
        """
        # TODO
        pass

    def interaction_factor(self):
        """ Return B(t), the interaction coefficient, based on the current time.

        Returns:
            float
        """
        # TODO
        pass

    def hamiltonian(self):
        """ Returns the current energy.  The Hamiltonian is split into:

            - a kinetic term from the coupling between individual spins and
                an external magnetic field
            - an interaction term from the coupling between linked spins
                of the graph

            H(t) = -A(t) \sum_i sin i    -    B(t) \sum_{i<j} J_{ij} (cos i) (cos j)

            where A(t) and B(t) are coefficients determined by the annealing
            schedule.
        Returns:
            float
        """
        all_nodes = self._graph.all_nodes()
        all_edges = self._graph.all_edges()

        kinetic = 0
        for node in all_nodes:
            kinetic += sin(node.value)
        kinetic *= -self.kinetic_factor()

        interaction = 0
        for node_a, node_b in all_edges:
            coupling = self._graph.get_spin(node_a, node_b)
            interaction += coupling * cos(node_a.value) * cos(node_b.value)
        interaction *= -self.interaction_factor()

        return kinetic + interaction

    def solve(self):
        while self._time < 1:
            self.iterate()

    def kick_probability(self, node):
        """ Determine the probability that a node should be kicked.

        Args:
            node: Node object

        Returns:
            probability between 0 and 1
        """
        theta = node.value
        theta_prime = random() * 2 * pi

        kinetic = sin(theta_prime) - sin(theta)
        kinetic *= -self.kinetic_factor()

        interaction = 0
        other_nodes = self._graph.all_nodes_connected_to_node(node)
        for other_node in other_nodes:
            coupling = self._graph.get_spin(node, other_node)
            other_theta = other_node.value
            interaction += coupling * cos(other_theta)
        interaction *= cos(theta_prime) - cos(theta)
        interaction *= -self.interaction_factor()

        energy_delta = kinetic + interaction
        prob = exp(-energy_delta / self._temp)
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

        for node in all_nodes:
            prob = self.kick_probability(node)
            kicks.append(random() < prob)

        # Then kick them
        for i, node in enumerate(all_nodes):
            if kicks[i]:
                node.kick()

        self._time += Problem.TIMESTEP
