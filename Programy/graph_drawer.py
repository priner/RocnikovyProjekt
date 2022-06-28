import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import GraphParser
from sage.all import *

def main():
    # G=nx.Graph()
    graphsPath = ""

    for s in sys.argv:
        ss = s.split("=", maxsplit=1)
        if ss[0] == "-graph":
            graphsPath = ss[1]

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    graphs = [nx.Graph(g) for g in GraphParser.parse(graphsPath)]

    for graph in graphs:

        nx.draw(graph, with_labels = True)
        plt.show()

    # G.add_edges_from([(0, 30),
    # (0, 1),
    # (0, 5),
    # (1, 0),
    # (1, 2),
    # (1, 3),
    # (2, 1),
    # (2, 6),
    # (2, 8),
    # (3, 1),
    # (3, 4),
    # (3, 7),
    # (4, 3),
    # (4, 5),
    # (4, 10),
    # (5, 0),
    # (5, 4),
    # (5, 6),
    # (6, 2),
    # (6, 5),
    # (6, 7),
    # (7, 32),
    # (7, 3),
    # (7, 6),
    # (8, 2),
    # (8, 9),
    # (8, 11),
    # (9, 33),
    # (9, 8),
    # (9, 10),
    # (10, 18),
    # (10, 4),
    # (10, 9),
    # (11, 16),
    # (11, 8),
    # (11, 12),
    # (12, 11),
    # (12, 13),
    # (12, 14),
    # (13, 17),
    # (13, 19),
    # (13, 12),
    # (14, 15),
    # (14, 18),
    # (14, 12),
    # (15, 16),
    # (15, 21),
    # (15, 14),
    # (16, 15),
    # (16, 17),
    # (16, 11),
    # (17, 16),
    # (17, 18),
    # (17, 13),
    # (18, 17),
    # (18, 10),
    # (18, 14),
    # (19, 20),
    # (19, 22),
    # (19, 13),
    # (20, 19),
    # (20, 33),
    # (20, 21),
    # (21, 15),
    # (21, 20),
    # (21, 29),
    # (22, 19),
    # (22, 23),
    # (22, 27),
    # (23, 22),
    # (23, 24),
    # (23, 25),
    # (24, 30),
    # (24, 23),
    # (24, 28),
    # (25, 23),
    # (25, 26),
    # (25, 29),
    # (26, 32),
    # (26, 25),
    # (26, 27),
    # (27, 22),
    # (27, 26),
    # (27, 28),
    # (28, 24),
    # (28, 27),
    # (28, 29),
    # (29, 21),
    # (29, 25),
    # (29, 28),
    # (30, 0),
    # (30, 31),
    # (30, 24),
    # (31, 30),
    # (31, 32),
    # (31, 33),
    # (32, 31),
    # (32, 7),
    # (32, 26),
    # (33, 31),
    # (33, 20),
    # (33, 9)])
    # nx.draw(G, with_labels = True)
    # plt.show()

if __name__ == '__main__':
    main()
