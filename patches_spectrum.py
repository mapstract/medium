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

    dim_choices = ((2, 2), (2, 3), (2, 4), (3, 3), (2, 6), (3, 4))
    
    evals_lists = [None] * len(dim_choices)

    for i in range(len(dim_choices)):

        (m, n) = dim_choices[i]

        G = bu.get_patches_graph(m, n)

        laplacian = nx.directed_laplacian_matrix(G)
        ne = laplacian.shape[0]

        k = ne-1
        evals = sp.sparse.linalg.eigs(laplacian, k=k, return_eigenvectors=False)

        evals = sorted(evals.real)
        evals_lists[i] = list(evals)

    fig = plt.figure(figsize=(9, 7))

    ax_locations = (231, 232, 233, 234, 235, 236)

    y_max = max([max(l) for l in evals_lists])

    for i in range(len(dim_choices)):

        evals_list = evals_lists[i]
        ne = len(evals_list)

        ax = fig.add_subplot(ax_locations[i])
        ax.set_xlabel(str(dim_choices[i]))

        if i == 0:
            ax.set(yticklabels=[0, 0.25, 0.5, 0.75, 1.0, 1.25])
            ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25])
        else:
            ax.set(yticklabels=[])
            ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25])

        plt.xlim(-0.5, ne + 0.5)

        plt.ylim(0, y_max)

        plt.grid(axis='y', linestyle=':')

        plt.scatter(range(1,(ne+1)), evals_list, s=10, color='black')

    plt.show()

    fig.savefig("/Users/brianbunker/Dropbox/medium/graph_theory/figures/patches_spectra.png")
    print("--done--")