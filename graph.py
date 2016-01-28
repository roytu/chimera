
""" Module containing the graph, which maintains the state of all nodes and
    their connections.

    In particular, a graph is fully defined by:
        - A set of nodes
        - A set of (Node, Node, Spin) that determines connections
"""

class Graph(object):
    def __init__(self):
        self._connections = dict()
        """ Node -> [Node] mapping """

        self._spins = dict()
        """ (Node, Node) -> Spin mapping
            Invariants:
                - No keys matching: (A, A)
                - Given (A, B) is a key, (B, A) is not a key
        """
        self._ids = dict()
        """ Node -> Int """

    def add(self, node):
        """ Adds a node to the graph.

        Args:
            node: Node object
        """
        self._connections[node] = []
        self._ids[node] = len(self._ids)

    def connect(self, node_a, node_b, spin):
        """ Connects this node with another node, where the edge has some
        interaction strength (-1 or 1).

        Args:
            node_a: Node object
            node_b: other Node object
            spin: interaction strength (-1 or 1)
        """
        assert node_a is not node_b, "No keys matching (A, A) allowed"
        assert (node_a, node_b) not in self._spins or \
               (node_b, node_a) not in self._spins, "Edge already exists"

        self._connections[node_a].append(node_b)
        self._connections[node_b].append(node_a)
        self._spins[(node_a, node_b)] = spin
    def get_spin(self, node_a, node_b):
        """ Gets the spin correlation between two nodes.  If they are not
        connected, return None.

        Args:
            node_a: Node object
            node_b: Node object

        Returns:
            spin value (-1 or 1)
        """
        if (node_a, node_b) in self._spins:
            return self._spins[(node_a, node_b)]
        if (node_b, node_a) in self._spins:
            return self._spins[(node_b, node_a)]
        return None

    def all_nodes(self):
        """ Return a list of all nodes in the graph, in the order in which
        they were added.

        Returns:
            list of Node objects
        """
        return self._connections.keys()

    def all_edges(self):
        """ Return a list of edges (Node, Node)

        Returns:
            list of (Node, Node) tuples
        """
        return self._spins.keys()

    def all_nodes_connected_to_node(self, node):
        """ Returns a list of nodes connected to some node.

        Args:
            node: Node object

        Returns:
            list of Node objects
        """
        return self._connections[node]
    def get_id(self, node):
        """ Get the ID of some node in the graph.

        Args:
            node: Node object

        Returns:
            integer
        """
        return self._ids[node]
