import sys

import numpy as np

import bitmap_utilities as bu
import bitmap

sys.path.insert(1, '/Users/brianbunker/networkx_2.6.3/')
import networkx as nx

def dot(x_0, x_1):

    x_0.check_dims(x_1)

    return int(np.sum(x_0.array() == x_1.array()))

def distance(x_0, x_1):

    return x_0.m * x_0.n - dot(x_0, x_1)

def print_choices(choices):
    for choice in choices:
        print(str(choice[0]) + " : " + str(choice[1]))
        print(choice[2].array())
        print(choice[3])
        print("---------------------")

def best_tasks(x_0, x_1, bitmap_repertoire):

    # largest transformation which minimizes distance from target

    min_d = 2**(x_0.m * x_0.n)

    choices = [None] * 2 * len(bitmap_repertoire)

    cnt = 0
    for i in bitmap_repertoire:
        b = bitmap.BitMap(x_0.m, x_0.n, i)
        coverage = np.sum(b.array(), axis=None)
        for val in (0, 1):
            tmp = x_0.copy()
            tmp.apply(b, val)
            d = distance(tmp, x_1)
            min_d = min(d, min_d)
            choices[cnt] = (d, coverage, b, val)
            cnt += 1

    sub = [choice for choice in choices if choice[0] == min_d]
    # max_coverage = max([choice[1] for choice in sub])
    # sub = [choice for choice in sub if choice[1] == max_coverage]
    best_tasks = sub

    return best_tasks

def best_paths(x_0, x_1, bitmap_repertoire, completed_paths = [], open_paths = None):

    if open_paths is None:
        open_paths = [[x_0, ]]

    if len(open_paths) == 0:
        # terminal return
        tmp = [[b.i_value for b in path] for path in completed_paths]
        result = []
        for path in tmp:
            if path not in result:
                result.append(path)
        min_len = min([len(path) for path in result])
        result = [path for path in result if len(path) == min_len]
        return result

    next_open_paths = []

    for path in open_paths:
        x_c = path[-1]
        bt = best_tasks(x_c, x_1, bitmap_repertoire)

        for task in bt:

            tmp = x_c.copy()

            b, v = task[2:]
            tmp.apply(b, v)

            next_path = path.copy()
            next_path.append(tmp)
            if tmp == x_1:
                completed_paths.append(next_path)
            else:
                next_open_paths.append(next_path)

    return best_paths(x_0, x_1, bitmap_repertoire, completed_paths, next_open_paths)


if __name__ == "__main__":

    m = 3
    n = 3
    
    l = 2**(m*n)

    G = bu.get_patches_graph(m, n)

    bu.print_statistics(G)

    bitmap_repertoire = bu.get_patch_bitmaps(m, n)

    do_test = False
    if do_test:
        node_0 = 0
        node_1 = 170

        foo = bitmap.BitMap(m, n, node_0)
        bar = bitmap.BitMap(m, n, node_1)

        tmp = best_paths(foo, bar, bitmap_repertoire)
        sp = nx.shortest_path(G, node_0, node_1)

        print("-- got here --")

    for node_0 in range(l):

        print("node_0 = " + str(node_0))

        for node_1 in range(node_0 + 1, l):

            b_0 = bitmap.BitMap(m, n, node_0)
            b_1 = bitmap.BitMap(m, n, node_1)

            sp = nx.shortest_path(G, node_0, node_1)

            tmp = best_paths(b_0, b_1, bitmap_repertoire, completed_paths=[], open_paths=None)   
            min_n = min([len(path) for path in tmp])

            if len(sp) < min_n:
                print("-- got here --")

    print("-- done --")