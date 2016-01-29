
""" Module containing functions that primarily take in a graph and draw
    a model for it.
"""

from example_graphs import make_chimera_graph
import visual as v

import numpy as np
import matplotlib.pyplot as plt

from problem import Problem

#from commands import getoutput
#from time import sleep

def draw_chimera_graph(graph, n, magnet_frames=None):
    """ Draws a chimera graph to a window and displays it.

    Args:
        graph: Graph object
        n: dimension of Chimera graph
        magnet_frames: supply an empty list, which gets populated
            by (Frame, angle) tuples for drawing

    Returns:
        frame
    """
    # Draw nodes
    all_nodes = graph.all_nodes()
    all_edges = graph.all_edges()

    global_frame = v.frame()

    for node in all_nodes:
        """ The Chimera graph is ID'd as follows:

            e.g. n = 4,

            x -->

         y  00 04    08 12    16 20    24 28
         |  01 05    09 13    17 21    25 29
         v  02 06    10 14    18 22    26 30
            03 07    11 15    19 23    27 31

            32 36    40 44    48 52    56 60
            33 37    41 45    49 53    57 61
            34 38    42 46    50 54    58 62
            35 39    43 47    51 55    59 63
             ...      ...      ...      ...

        where the left entries are in the left graph, and the right
        entries are in the right graph (the vertically and horizontally-coupled
        nodes, respectively).
        """
        i = graph.get_id(node)
        k = i % 4

        SPACING = 0.1
        x = (i // 8) % n + (SPACING if k in (0, 2) else -SPACING)
        y = i // (8 * n) + (SPACING if k in (0, 1) else -SPACING)
        z = 0 if i % 8 < 4 else 1

        model = node.model()
        model.pos = (x, y, z)
        model.frame = global_frame

    # Draw links
    for node_a, node_b in all_edges:
        i = graph.get_id(node_a)
        j = graph.get_id(node_b)

        k1 = i % 4
        k2 = j % 4

        x1 = (i // 8) % n + (SPACING if k1 in (0, 2) else -SPACING)
        y1 = i // (8 * n) + (SPACING if k1 in (0, 1) else -SPACING)
        z1 = 0 if i % 8 < 4 else 1

        x2 = (j // 8) % n + (SPACING if k2 in (0, 2) else -SPACING)
        y2 = j // (8 * n) + (SPACING if k2 in (0, 1) else -SPACING)
        z2 = 0 if j % 8 < 4 else 1

        color = v.color.red if graph.get_spin(node_a, node_b) == 1 else v.color.blue

        v.curve(frame=global_frame, pos=[(x1, y1, z1), (x2, y2, z2)], radius=0.05,
            color=color)

    global_frame.pos -= (n / 2, n / 2, 0)

if __name__ == "__main__":
    scene = v.display(title="Chimera Graph", x=0, y=0, width=600, height=600,
        center=(0, 0, 0))
    scene.forward = (0.5, 0.5, -1)

    SCALE = 0.2
    scene.scale = (SCALE, SCALE, SCALE)


    N = 4
    g = make_chimera_graph(N)

    magnet_frames = []
    draw_chimera_graph(g, N, magnet_frames)

    TEMP = 0.22
    problem = Problem(g, TEMP)

    xs = []
    ys = []
    #screenshot_schedule = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    #screen_index = 0

    #sleep(5)
    while not problem.is_finished():
        prev_time = problem._time
        problem.iterate()

        #if prev_time <= screenshot_schedule[screen_index] and \
        #   problem._time >= screenshot_schedule[screen_index]:
        #    getoutput("xwd -name \"Chimera Graph\" | convert xwd:- images/image_{0:03}.png".format(int(problem._time * 100)))
        #    screen_index += 1

        energy = problem.hamiltonian()
        xs.append(problem._time)
        ys.append(energy)
        print(problem._time, energy)

    xs = np.array(xs)
    ys = np.array(ys)

    np.save("times", xs)
    np.save("energy", ys)

    plt.title("Ground State Energy Over Time (A = A(1), B = B(1))")
    plt.xlabel("Time $(t / t_f)$")
    plt.ylabel("Energy (GHz)")
    plt.plot(xs, ys)
    plt.savefig("plot.png")
    plt.show()
