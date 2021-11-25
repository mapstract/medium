from importlib import machinery
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

import bitmap_utilities as bu
import utilities as u

sys.path.insert(1, '/Users/brianbunker/networkx_2.6.3/')
import networkx as nx

if __name__ == "__main__":

    m = 3
    n = 3

    graph_choice = "patches"
    scale_method = "maximum eigenvalue"

    undirected_choices = ("complete")
    directed_choices = ("bitwise", "lines", "patches", "patches_1d", "patches_1d_nontoroidal", "patches_1d_toroidal",
        "necklace")

    if graph_choice == "complete":
        G = bu.get_complete_graph(m, n)
    elif graph_choice == "bitwise":
        G = bu.get_bitwise_graph(m, n)
    elif graph_choice == "lines":
        G = bu.get_lines_graph(m, n)
    elif graph_choice == "patches":
        G = bu.get_patches_graph(m, n)
    elif graph_choice == "patches_1d":
        G = bu.get_patches_1d_graph(m)
    elif graph_choice == "patches_1d_nontoroidal":
        G = bu.get_patches_1d_nontoroidal_graph(m)
    elif graph_choice == "patches_1d_toroidal":
        G = bu.get_patches_1d_toroidal_graph(m)
    elif graph_choice == "necklace":
        G = bu.get_group_informed_graph(m, bu.necklace_orbit, verbose=True)
    else:
        print("Unknown graph type.")
        sys.exit(0)

    bu.print_statistics(G)

    degrees = [t[1] for t in G.degree()]
    mean_degree = np.sum(degrees) / len(degrees)

    if graph_choice in undirected_choices:
        laplacian = nx.laplacian_matrix(G).asfptype()
    elif graph_choice in directed_choices:
        laplacian = nx.directed_laplacian_matrix(G)
    else:
        print("Unexpected graph choice")
        sys.exit(0)

    ne = laplacian.shape[0]

    k = ne-1
    # spectrum = np.linalg.eig(laplacian)
    evals = sp.sparse.linalg.eigs(laplacian, k=k, return_eigenvectors=False)
    # v = evecs.flatten().real

    evals = sorted(evals.real)
    evals_list = list(evals)

    if len(evals_list) < 50:
        print([round(x, 6) for x in evals_list])
    else: 
        print(str([round(x, 6) for x in evals_list[:10]]) + " ... " + str([round(x, 6) for x in evals_list[-10:]]))

    do_plot = True
    if do_plot:

        fig = plt.figure(figsize=(9, 3))
        ax = fig.add_subplot(131)

        plt.xlim(-0.5, ne + 0.5)

        if scale_method == "none":
            plt.ylim(-0.5, ne + 0.5)
        elif scale_method == "average degree":
            plt.ylim(-0.05, (mean_degree + 1) * 1.05)
        elif scale_method == "maximum eigenvalue":
            plt.ylim(0, np.max(evals_list))

        plt.grid()

        plt.scatter(range(1,(ne+1)), evals_list)
        plt.show()

    print("--done--")