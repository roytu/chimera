
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
    left_grid = [[[] for _ in range(n)] for _ in range(n)]
    right_grid = [[[] for _ in range(n)] for _ in range(n)]

    # Spawn nodes
    for i in range(n):
        for j in range(n):
            for g in [left_grid, right_grid]:
                for _ in range(4):
                    # Four nodes in each supernode
                    node = Node()
                    graph.add(node)
                    g[i][j].append(node)

    # Vertical connections
    for j in range(n):
        for i in range(n-1):
            for k in range(4):
                node = left_grid[i][j][k]
                next_node = left_grid[i+1][j][k]
                graph.connect(node, next_node, choice([1, -1]))

    # Horizontal connections
    for i in range(n):
        for j in range(n-1):
            for k in range(4):
                node = right_grid[i][j][k]
                next_node = right_grid[i][j+1][k]
                graph.connect(node, next_node, choice([1, -1]))

    # Same node connections
    for i in range(n):
        for j in range(n):
            for k1 in range(8):
                for k2 in range(k1 + 1, 8):
                    left_node = (left_grid if k1 < 4 else right_grid)[i][j][k1 % 4]
                    right_node = (left_grid if k2 < 4 else right_grid)[i][j][k2 % 4]
                    graph.connect(left_node, right_node, choice([1, -1]))

    return graph
