import sys

sys.path.insert(1, '/Users/brianbunker/networkx_2.6.3/')
import networkx as nx

from bitmap import BitMap

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

# Specific bitmaps

def get_coordinate_bitmap(m, n, i, j):
    # use standard array coordinates - down from upper left.
    return 2**(m*n - (i * n + j + 1))

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


def get_patch_1d_bitmaps(m, n=1):

    all_coords = [(i, 0) for i in range(m)]

    s = set()

    for k in range(1, m + 1):
        for c in all_coords:
            B_c = get_patch_bitmap(m, 1, c, k, 1)
            s.add(B_c.i_value)

    result = sorted(list(s))

    return result

def get_patch_1d_nontoroidal_bitmaps(m, n=1):

    if n != 1:
        print("Expect n=1 for this graph type.")
        sys.exit(0)

    s = set()
    for k in range(1, m + 1):
        for i in range(m - k + 1):
            B_c = get_patch_bitmap(m, 1, (i, 0), k, 1)
            s.add(B_c.i_value)

    result = sorted(list(s))

    return result

def get_patch_1d_toroidal_bitmaps(m, n=1):

    if n != 1:
        print("Expect n=1 for this graph type.")
        sys.exit(0)

    s = set()
    for k in range(1, m + 1):
        for i in range(m):
            B_c = get_patch_bitmap(m, 1, (i, 0), k, 1)
            s.add(B_c.i_value)

    result = sorted(list(s))

    return result

def get_patch_bitmaps(m, n):

    ul1 = 1

    s = set()
    # i, j = size of patch
    # c1, c2 = coordinates of lower left corner of patch
    for i in range(1, m + ul1):
        for j in range(1, n + ul1):
            for c1 in range(m - i + ul1):
                for c2 in range(n - j + ul1):
                    B_c = get_patch_bitmap(m, n, (c1, c2), i, j)
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

# Groups and Equivalence Classes

def necklace_shift(i, n, direction='l'):

    E = 2**n
    if i > E:
        print("necklace_shift: i too large.")
        sys.exit(1)

    E2 = E // 2
    if direction == 'l':
        return (i // E2) + (i - (i // E2 * E2) << 1)
    elif direction == 'r':
        return (i % 2) * E2 + (i >> 1)

def necklace_orbit(i, n):

    orbit = set()
    orbit.add(i)

    i0 = i
    done = False
    while not done:
        i = necklace_shift(i, n)
        done = i0 == i
        if not done:
            orbit.add(i)
    return orbit

class EquivalenceClasses(object):

    def __init__(self, n, f_orbit):

        self.n = n
        self.f_orbit = f_orbit
        self.equiv = None
        self.filled = False

    def fill(self, verbose=False):

        equiv = {}
        traversed = set()

        E = 2**self.n
        for i in range(E):
            if i in traversed:
                continue
            orbit = necklace_orbit(i, self.n)
            traversed.update(orbit)
            equiv[i] = orbit
            if verbose:
                print(str(i) + " | " + str(E))

        self.filled = True
        self.equiv = equiv

    def len(self):
        if self.filled:
            return len(self.equiv)
        else:
            return None

    def get_nodes(self):
        return list(self.equiv.keys())

    def get(self):
        return self.equiv            

def get_group_informed_graph(n, f_orbit, verbose=False):

    equiv = EquivalenceClasses(n, f_orbit)
    equiv.fill(verbose)

    nodes = equiv.get_nodes()

    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    e = equiv.get()
    patch_bitmaps = get_patch_1d_bitmaps(n)

    for p in nodes:
        if verbose:
            print(str(p) + " | " + str(2**n))
        for q in patch_bitmaps:
            for l in (0, 1):
                B0 = BitMap(n, 1, p)
                B1 = BitMap(n, 1, q)
                B0.apply(B1, l)
                b = B0.i_value
                if b != p:
                    for node in nodes:
                        if b in e[node]:
                            if (p, node) not in G.edges:
                                G.add_edge(p, node)
                            break

    return G



# Specific Graphs

def get_complete_graph(m, n):
    q = 2**(m*n)   
    return nx.complete_graph(q)

def get_bitwise_graph(m, n):
    return get_graph(m, n, get_bitwise_bitmaps)

def get_lines_graph(m, n):
    return get_graph(m, n, get_line_bitmaps)

def get_patches_graph(m, n):
    return get_graph(m, n, get_patch_bitmaps)

def get_patches_1d_graph(m):
    return get_graph(m, 1, get_patch_1d_bitmaps)

def get_patches_1d_nontoroidal_graph(m):
    return get_graph(m, 1, get_patch_1d_nontoroidal_bitmaps)

def get_patches_1d_toroidal_graph(m):
    return get_graph(m, 1, get_patch_1d_toroidal_bitmaps)


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

