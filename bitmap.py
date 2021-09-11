import sys

sys.path.insert(1, '/Users/brianbunker/networkx_2.6.3/')

import math
import matplotlib.pyplot as plt
import networkx as nx
from networkx.linalg.laplacianmatrix import laplacian_matrix
from networkx.linalg.laplacianmatrix import directed_laplacian_matrix
import numpy as np
from numpy.ma.core import is_string_or_list_of_strings
import scipy as sp

# git clone https://github.com/mapstract/medium.git
# PAT: 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
# ssh -i /Users/brianbunker/Dropbox/aws/pem/brian.pem  ec2-user@ec2-18-217-114-64.us-east-2.compute.amazonaws.com
# ssh -i /Users/brianbunker/Dropbox/aws/pem/brian.pem  ubuntu@
# c6g.8xlarge
# to-do:
# ( ) add non-square patches
# ( ) patches_1d

def invb(b, mn):
    return(2**mn - 1 - b)

def apply_bitmap(b, b0, mn, val):
    if val == 1:
        return b | b0
    else: 
        return invb(invb(b0, mn) | b, mn) 

class BitMap(object):

    def __init__(self, m, n, i_value = 0):
        self.m = m
        self.n = n
        self.i_value = i_value

        self.mn = self.m * self.n

    def __eq__(self, other):
        """Overrides the default implementation of =="""
        if isinstance(other, BitMap):
            return self.i_value == other.i_value
        return False

    def __str__(self):
        return str(self.array())
 
    # Representation functions

    def bin(self):
        return bin(self.i_value)

    def list_1d(self):
        result = [None] * self.mn
        tmp = self.i_value
        for i in range(self.mn):
            result[self.mn - 1 - i] = tmp % 2
            tmp = tmp >> 1
        return result

    def array(self):
        return np.reshape(np.array(self.list_1d()), (self.m, self.n))

    # tranformations

    def apply(self, B, val):
        self.i_value = apply_bitmap(B.i_value, self.i_value, self.mn, val)


def get_coordinate_bitmap(m, n, i, j):
    # use standard array coordinates - down from upper left.
    return 2**(m*n - (i * n + j + 1))

def get_inclusive_range(i1, i2):
    if i2 > i1:
        return list(range(i1, i2 + 1))
    else:
        return list(range(i1, i2 - 1, -1))

def signum(x):
    if x > 0:
        return 1
    else:
        return -1

def get_bitwise_bitmaps(m, n):

    mn = m*n

    result = [None] * m * n

    for i in range(m):
        for j in range(n):
            b_c = get_coordinate_bitmap(m, n, i, j)
            B_c = BitMap(m, n, b_c)
            result[i * n + j] = B_c.i_value           

    return result


def get_patch_bitmap(m, n, c, p, q):

    (i, j) = c

    i_range = [(i + k) % m for k in range(p)]
    j_range = [(j + k) % n for k in range(q)]

    i_value = 0
    for ii in i_range:
        for jj in j_range:
            i_value += get_coordinate_bitmap(m, n, ii, jj)

    result = BitMap(m, n, i_value)

    return result

def get_patch_bitmaps(m, n):

    mn = m*n

    km_max = int(math.floor(math.log(m)/math.log(2)))
    kn_max = int(math.floor(math.log(n)/math.log(2)))
    k_max = min(km_max, kn_max)

    all_coords = [(i, j) for i in range(m) for j in range(n)]

    result = [None] * (k_max + 1) * m * n

    cnt = 0
    for k in range(k_max + 1):
        f = 2**k
        for c in all_coords:
            B_c = get_patch_bitmap(m, n, c, f, f)
            result[cnt] = B_c.i_value
            cnt += 1

    return result

def get_patch_1d_bitmaps(m, n=1):

    all_coords = [(i, 0) for i in range(m)]

    s = set()

    cnt = 0
    for k in range(1, m + 1):
        for c in all_coords:
            B_c = get_patch_bitmap(m, 1, c, k, 1)
            s.add(B_c.i_value)

    result = sorted(list(s))

    return result



def get_line_bitmap(m, n, c1, c2):

    (i1, j1) = c1
    (i2, j2) = c2

    p = min(abs(i2 - i1), abs(j2 - j1))
    q = max(abs(i2 - i1), abs(j2 - j1))
 
    if q == 0:
        cc = [(0, 0)]
    else:
        slope = p / q # m < 1
        cc = [(k, round(slope * k)) for k in range(q + 1)]

    irange = get_inclusive_range(i1, i2)
    jrange = get_inclusive_range(j1, j2)

    i_signum = signum(i2 - i1)
    j_signum = signum(j2 - j1)

    if len(jrange) < len(irange):
        coords = [(i1 + i_signum * c[0], j1 + j_signum * c[1]) for c in cc]
    else:
        coords = [(i1 + i_signum * c[1], j1 + j_signum * c[0]) for c in cc]

    i_value = 0
    for coord in coords:
        i_value += get_coordinate_bitmap(m, n, coord[0], coord[1])

    result = BitMap(m, n, i_value)

    return result        

def get_line_bitmaps(m, n):

    mn = m*n
    q = 2**mn

    all_coords = [(i, j) for i in range(m) for j in range(n)]

    result = [None] * int((mn * (mn + 1) / 2))

    cnt = 0
    for p in range(mn):
        for q in range(p + 1):
            B_c = get_line_bitmap(m, n, all_coords[p], all_coords[q])
            result[cnt] = B_c.i_value
            cnt += 1
            
    return result

def get_graph(m, n, f_bitmaps):

    mn = m*n

    q_max = 2**mn
    G = nx.DiGraph()
    G.add_nodes_from(list(range(q_max)))

    bitmaps = f_bitmaps(m, n)

    for q in range(q_max):
        if q % 1000 == 0:
            print(str(q) + " | " + str(q_max))
        for p in bitmaps:        
            B_c = BitMap(m, n, p)
            for l in (0, 1):
                B0 = BitMap(m, n, q)
                b0 = B0.i_value
                B0.apply(B_c, l)
                b1 = B0.i_value
                if b0 != b1:
                    if (b0, b1) not in G.edges:
                        G.add_edge(b0, b1)

    return G

def get_complete_graph(m, n):

    mn = m*n
    q = 2**mn
   
    return nx.complete_graph(q)

def get_bitwise_graph(m, n):
    return get_graph(m, n, get_bitwise_bitmaps)

def get_lines_graph(m, n):
    return get_graph(m, n, get_line_bitmaps)

def get_patches_graph(m, n):
    return get_graph(m, n, get_patch_bitmaps)

def get_patches_1d_graph(m):
    return get_graph(m, 1, get_patch_1d_bitmaps)


def print_statistics(G, short=True):

    print("Nodes: " + str(nx.number_of_nodes(G)))
    print("Edges: " + str(nx.number_of_edges(G)))
    is_regular = nx.is_regular(G)
    print("Is regular: " + str(is_regular))

    if short:
        print("Skipping diameter")
    else:
        d = nx.diameter(G)
        print("Diameter: " + str(d))


if __name__ == "__main__":

    # m = 11
    # foo = get_patch_1d_bitmaps(m)

    # expected_length = (m - 1) * m + 1

    # print("len(foo) = " + str(len(foo)) + " | expected = " + str(expected_length))

    # patches maximum eigenvalue
    # 1   
    # 2  
    # 3  
    # 4  
    # 5  
    # 6  
    # 7  
    # 8  
    # 9  
    # 10 [0.482232, 1.171977, 1.295349]
    # 11 [0.480888, 1.167144, 1.293266]
    # 12 [0.474396, 1.166785, 1.291815]
    # 13 [0.46179,  1.16779,  1.290785]

    m = 3
    n = 2

    short = False

    graph_choice = "patches"
    scale_method = "maximum eigenvalue"

    undirected_choices = ("complete")
    directed_choices = ("bitwise", "lines", "patches", "patches_1d")

    if graph_choice == "complete":
        G = get_complete_graph(m, n)
    elif graph_choice == "bitwise":
        G = get_bitwise_graph(m, n)
    elif graph_choice == "lines":
        G = get_lines_graph(m, n)
    elif graph_choice == "patches":
        G = get_patches_graph(m, n)
    elif graph_choice == "patches_1d":
        G = get_patches_1d_graph(m)
    else:
        print("Unknown graph type.")
        sys.exit(0)

    degrees = [t[1] for t in G.degree()]
    mean_degree = np.sum(degrees) / len(degrees)

    if graph_choice in undirected_choices:
        laplacian = laplacian_matrix(G).asfptype()
    elif graph_choice in directed_choices:
        laplacian = directed_laplacian_matrix(G)
    else:
        print("should not get here")
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

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)

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