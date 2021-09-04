import math
import networkx as nx
import numpy as np


if __name__ == "__main__":

    G = nx.Graph()
    G.add_nodes_from([0,1])
    G.add_edge(0,1)

    L = nx.normalized_laplacian_spectrum(G)

    print(L)

    print("--done--")