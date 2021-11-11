
import sys

from identities import sum_m_2_m_i

def S_1d(n, j, check=True):

    # Let m = n - k - 1  and k = n - m - 1
    # if k = j, then m = n - j - 1
    # if k = n - 1 then m = 0

    S_check = 0
    for k in range(j, n):
        S_check += (k - j + 1) * (n - k + 3) * 2**(n - k - 2)
    S_check += n - j + 1

    S = (n - j + 1) * E_(n - j)

    if S != S_check:
        print("Check failed.")
        sys.exit(1)

    return int(S)

def S_n_1_recursive(n, d=None):
    # this is verified as correct

    ul1 = 1

    one = 1

    if d is None:
        d = {1 : 1}

    if n in d:
        return d[n]

    result = S_n_1_recursive(n - 1)
    result += (n - one + 1)
    for m in range(1, n - one + ul1):
        tmp = (m - one + 1) * 2**(n - m - one)
        result += tmp
    
    for m in range(1, n - one - 1 + ul1):
        tmp = S_n_1_recursive(n - m - 1)
        result += tmp
    
    d[n] = result

    return result

def S_n_j_recursive(n, j, d=None):
    # this is verified as correct
    ul1 = 1

    if d is None:
        d = {}
        for i in range(1, n - 1 + ul1):
            d[(i, i)] = 1

    if (n, j) in d:
        return d[(n, j)]

    def pos_part(x):
        if x < 0:
            return 0
        else:
            return x

    result = 0    
    for m in range(j, n + ul1):
        tmp =  (m - j + 1) * 2**(pos_part(n - m - 1))
        result += tmp

    for m in range(0, n - j - 1 + ul1):
        tmp = S_n_j_recursive(n - m - 1, j, d)
        result += tmp

    d[(n, j)] = result

    return result

def S_m_n_m_j_recursive(m, n, j, d=None):
    # Verified correct through 2 x 3

    ul1 = 1

    if d is None:
        d = {}
        for i in range(1, n - 1 + ul1):
            d[(i, i)] = 1

    if (n, j) in d:
        return d[(n, j)]

    result = (n - j + 1)

    for k in range(j, n - 1 + ul1):
        tmp =  (k - j + 1) * 2**((n - k - 1) * m) * (2**m - 1)
        result += tmp

    for k in range(0, n - j - 1 + ul1):
        tmp = S_m_n_m_j_recursive(m, n - k - 1, j, d)
        tmp *= 2**m - 1
        result += tmp

    d[(n, j)] = result

    return result

def S_m_n_m_j(m, n, j):
    # This has been extensively checked but remains to be full proved.
    # see S_m_n_m_j_working and S_m_n_m_j_recursive
    return E_(m*(n - j)) * (n - j + 1)

def S_m_n_m_j_working(m, n, j, d=None, verify=False):
    # Verified correct through 2 x 3

    ul1 = 1

    if d is None:
        d = {}
        for i in range(1, n - 1 + ul1):
            d[(i, i)] = 1

    if (n, j) in d:
        return d[(n, j)]

    #--------------------------------

    speculated_answer = E_(m*(n - j)) * (n - j + 1)
    result = speculated_answer


    # The speculated identity is very occasionally wrong! Main example is m= 3, n = 2, j = 1
    # This appears to be the result of a mistake in the algebra rather than the answer.
    # To correct, I'd need to go back to S_m_n_m_j_recursive and try to refine it again.
    speculated_identity = 0

    speculated_identity -= (1 / E_(m)) * sum_m_2_m_i(m, n - j + 1)

    tmp = 0
    for k in range(0, n - j - 1 + ul1):
        tmp += S_m_n_m_j_working(m, n - k - 1, j, d) 
    
    speculated_identity += tmp

    speculated_identity *= E_(m) - 1
    print("Speculated identity: " + str(speculated_identity))

    result  += speculated_identity

    #--------------------------------

    d[(n, j)] = result

    if (speculated_answer != result):
        print("got here")

    if verify:
        test = test_S(m, n, m, j)
        if speculated_answer != test:
            print("S_m_n_m_j_working doesn't verify")

    return result



def first_try_S(m, n, i, j, d = None, indent = "", verify=False):

    # number of black sub-blocks of dimension (i, j) in the black
    # patterns of all vertices of an m x n bitmap graph.

    indent += "  "

    if i > m or j > n:
        return 0

    if d is None:
        d = {}
        for k in range(1, m + 1):
            for l in range(1, n + 1):
                d[(1, 1, k, l)] = k * l * 2**(k * l - 1)

    if (i, j, m, n) in d:
        result = d[(i, j, m, n)] 
        print("Using dictionary: " + str((i, j, m, n)) + " : " + str(result))
        return result

    # main results

    if i == m:
        result = S_m_n_m_j(m, n, j)
    elif j == n:
        result =  S_m_n_m_j(n, m, i)

    else:

        # boundary_ratio = (m - i + 1) * (n - j + 1) / (m*n)
        # bit_overlap_multiple = E_(m * n * (i - 1))
        # expected_ratio = boundary_ratio / bit_overlap_multiple
        # flattened_S = S(i, m*n, i, j)
        # result = flattened_S * expected_ratio

        # This doesn't work for i > 2
        denominator = (m - i + 1) * n - (j - 1)
        numerator = denominator - (m - i) * (j - 1)

        # This is 2 ^ (number of overlapped bits to form the ribbon)
        bits_overlap = E_((i - 1) * (m - i) * n)    

        expected_ratio = numerator / (denominator * bits_overlap)
        flattened_S = S(i, n * (m - i + 1), i, j)
        result = flattened_S * expected_ratio

    if verify:
        test = test_S(m, n, i, j)
        if test != result:
            print("S_m_n_m_j doesn't verify")

    # print(str((i, j, m, n)) + " : " + indent + str(result))
    return result




