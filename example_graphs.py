
""" Module that has functions for the construction of well-known graphs
    SUCH AS THE CHIMERA GRAPH.
"""

from random import choice

from graph import Graph
from node import Node

def make_chimera_graph(n):
    """ Generates an NxN Chimera graph with random spins.

    Returns:
        Graph object
    """

    graph = Graph()

    # Left grid connects vertically, right grid connects horizontally
    left_grid = [[None for _ in range(n)] for _ in range(n)]
    right_grid = [[None for _ in range(n)] for _ in range(n)]

    # Spawn nodes
    for i in range(n):
        for j in range(n):
            for g in [left_grid, right_grid]:
                node = Node()
                graph.add(node)
                g[i][j] = node

    # Vertical connections
    for j in range(n):
        for i in range(n-1):
            node = left_grid[i][j]
            next_node = left_grid[i+1][j]
            graph.connect(node, next_node, choice([1, -1]))

    # Horizontal connections
    for i in range(n):
        for j in range(n-1):
            node = right_grid[i][j]
            next_node = right_grid[i][j+1]
            graph.connect(node, next_node, choice([1, -1]))

    # Same node connections
    for i in range(n):
        for j in range(n):
            left_node = left_grid[i][j]
            right_node = right_grid[i][j]
            graph.connect(left_node, right_node, choice([1, -1]))

    return graph
