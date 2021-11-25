import sys

sys.path.insert(1, '/Users/brianbunker/networkx_2.6.3/')
import networkx as nx

import bitmap_utilities as bu
import bitmap as b

def E_(n):
    return 2**n

def bitmap_optimized_graph(m, n, x1, bitmap_repertoire):

    verbose = False

    b1 = b.BitMap(m, n, x1)

    q_max = E_(m*n)

    G = nx.DiGraph()
    G.add_nodes_from(list(range(q_max)))

    for node in G.nodes:

        b0 = b.BitMap(m, n, node)

        best_tasks = b0.best_tasks(b1, bitmap_repertoire)
        t_v_s = [(task[2], task[3]) for task in best_tasks]

        if verbose:
            print("b0 :")
            print(b0.array())
            print("b1 :") 
            print(b1.array())       

        for i in range(len(t_v_s)):
            tmp = b0.copy()
            t_v = t_v_s[i]
            tmp.apply(t_v[0], t_v[1])

            if verbose:
                print("----------------------------")
                print(t_v[0].array())
                print(t_v[1])
                print("----------------------------")

                print(tmp.array())

            G.add_edge(node, tmp.i_value)

        if verbose:
            print("=========================")

    return G


if __name__ == "__main__":

    m = 3
    n = 3

    G = bu.get_patches_graph(m, n)
    bitmap_repertoire = bu.get_patch_bitmaps(m, n)

    bu.print_statistics(G)

    for node_1 in range(E_(m*n)):

        print(node_1)

        G_opt = bitmap_optimized_graph(m, n, node_1, bitmap_repertoire)
        print(str(len(G.edges)) + " | " + str(len(G_opt.edges)))

        for node_0 in range(2**(m*n)):

            sp = nx.shortest_path(G, node_0, node_1)
            sp_opt = nx.shortest_path(G_opt, node_0, node_1)

            if len(sp) != len(sp_opt):

                print("==============================")
                for x in sp:
                    print(b.BitMap(m, n, x).array())
                    print()
                print("------------------------------")
                for x in sp_opt:
                    print(b.BitMap(m, n, x).array())
                    print()
                print("==============================")


    print("-- done --")
