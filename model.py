
""" Module containing functions that primarily take in a graph and draw
    a model for it.
"""

from example_graphs import make_chimera_graph
import visual as v

def draw_chimera_graph(graph, n):
    """ Draws a chimera graph to a window and displays it.

    Args:
        graph: Graph object
        n: dimension of Chimera graph

    Returns:
        frame
    """
    # Draw nodes
    all_nodes = graph.all_nodes()
    all_edges = graph.all_edges()

    global_frame = v.frame()

    for i, node in enumerate(all_nodes):
        """ The Chimera graph is ID'd as follows:

            e.g. n = 4,

            x -->

        y   00 01    02 03    04 05    06 07
        |   08 09    10 11    12 13    14 15
        v   16 17    18 19    20 21    22 23
            24 25    26 27    28 29    30 31

        where the left entries are in the left graph, and the right
        entries are in the right graph (the vertically and horizontally-coupled
        nodes, respectively).
        """
        x = (i // 2) % n
        y = i // (2 * n)
        z = 0 if i % 2 == 0 else 1

        W = 0.2

        magnet_frame = v.frame(frame=global_frame)
        v.box(frame=magnet_frame, pos=(x + W / 2, y, z), size=(W, W, W), color=v.color.red)
        v.box(frame=magnet_frame, pos=(x - W / 2, y, z), size=(W, W, W),
            color=v.color.white)

        magnet_frame.rotate(angle=node.value, axis=(0, 0, 1), origin=(x, y, z))

    # Draw links
    for node_a, node_b in all_edges:
        i = graph.get_id(node_a)
        j = graph.get_id(node_b)

        x1 = (i // 2) % n
        y1 = i // (2 * n)
        z1 = 0 if i % 2 == 0 else 1

        x2 = (j // 2) % n
        y2 = j // (2 * n)
        z2 = 0 if j % 2 == 0 else 1

        color = v.color.red if graph.get_spin(node_a, node_b) == 1 else v.color.blue

        v.curve(frame=global_frame, pos=[(x1, y1, z1), (x2, y2, z2)], radius=0.05,
            color=color)

    global_frame.pos -= (n / 2, n / 2, 0)

if __name__ == "__main__":
    scene = v.display(title="Chimera Graph", x=0, y=0, width=600, height=600,
        center=(0, 0, 0))
    scene.forward = (0.5, 0.5, -1)

    SCALE = 0.1
    scene.scale = (SCALE, SCALE, SCALE)

    N = 8
    g = make_chimera_graph(N)
    draw_chimera_graph(g, N)
