def E_(n):
    return 2**n

def sum_2_k(n, check=False):  
    # returns Sum_1^(n-1) 2^k
    if n < 1:
        return None
    else:
        result = E_(n) - 2
        if check:
            if result != sum([E_(k) for k in range(1, n)]):
                print("sum_2_k: check failed.")
        return result

def sum_k_2_k(n, check=False):  
    # returns Sum_1^(n-1) k 2^k
    if n < 1:
        return None
    else:
        result = (n - 2) * E_(n) + 2
        if check:
            if result != sum([k * E_(k) for k in range(1, n)]):
                print("sum_k_2_k: check failed.")
        return result

def sum_k_2_2_k(n, check=False):  
    # returns Sum_1^(n-1) k^2 2^k
    if n < 1:
        return None
    else:
        result = int((n * n - 4 * n + 6) * E_(n) - 6)
        if check:
            if result != sum([k * k * E_(k) for k in range(1, n)]):
                print("sum_k_2_2_k: check failed.")
        return result

def sum_k_3_2_k(n, check=False):  
    # returns Sum_1^(n-1) k^3 2^k
    if n < 1:
        return None
    else:
        result = int((n*n*n - 6 * n*n + 18 * n - 26) * E_(n) + 26)
        if check:
            if result != sum([k * k * k * E_(k) for k in range(1, n)]):
                print("sum_k_3_2_k: check failed.")
        return result

#---------------------------------------------------------------------------

def sum_2_m_i(m, n, check=False):
    # returns Sum_0^(n-1) (2^m)^i
    if m < 1:
        return None
    result = (2**(n*m) - 1) / (2**m - 1)
    if check:
        if result != sum([E_(m)**i for i in range(n)]):
            print("sum_2_m_i: check failed")
    return result

def sum_m_2_m_i(m, n, check=False):
    # returns Sum_0^(n-1) i (2^m)^i
    # A = E_(m) - 1
    # B = (m - 2) * E_(m) + 2
    # C = (m * n - 2) * E_(m * n) + 2
    # D = (2**(n*m) - 1) / (2**m - 1)

    # This is clearly correct but seems hard to simplify further.
    result = (
        E_(m * n) * ((E_(m) - 1) * n) - (E_(m * n) - 1) * E_(m) 
    )

    # This division is introducing small rounding error
    result *= 1 / (E_(m) - 1)**2
    result = int(round(result))

    if check:
        tmp = sum([ii * 2**(m * ii) for ii in range(n)])
        if tmp != result:
            print("sum_m_2_m_i: check failed")

    return result

#---------------------------------------------------------------------------

# Special purpose sums with lower limit starting at 2 for derivation of Y(i, j)
# for number of edges.

def sum_0(n, check=False):
    # returns sum_i=2_n(i)
    if n < 2:
        return None
    result = (n*n + n - 2) / 2
    if check:
        if result != sum([i for i in range(2, n+1)]):
            print("sum_0: check failed")
    return result

def sum_1(n, check=False):
    # returns sum_i=2_n(2^(-i))
    if n < 2:
        return None
    result = E_(-(n+1)) * (E_(n) - 2)
    if check:
        if result != sum([2**(-i) for i in range(2, n+1)]):
            print("sum_1: check failed")
    return result

def sum_2(n, check=False):
    # returns sum_i=2_n(i * 2^(-i))
    if n < 2:
        return None
    result = (3/2) - (n + 2) * E_(-n)
    if check:
        if result != sum([i*2**(-i) for i in range(2, n+1)]):
            print("sum_2: check failed")
    return result

def sum_3(n, check=False):
    # returns sum_i=2_n(2^(-2i))
    if n < 2:
        return None
    result = (1/12) * (1 - E_(-2*(n-1)))
    if check:
        if result != sum([2**(-2*i) for i in range(2, n+1)]):
            print("sum_3: check failed")
    return result

def sum_4(n, check=False):
    # returns sum_i=2_n(i * 2^(-2i))
    if n < 3:
        return None
    result = (1/36) * (7 - 4 * (3 * n + 4) * E_(-2*n))
    if check:
        if result != sum([i*2**(-2*i) for i in range(2, n+1)]):
            tmp = sum([i*2**(-2*i) for i in range(2, n+1)])
            print("sum_4: check failed")
    return result

if __name__ == "__main__":

    n_max = 30
    m_max = 3

    for n in range(n_max):
        tmp = sum_2_k(n, check=True)
        tmp = sum_k_2_k(n, check=True)
        tmp = sum_k_2_2_k(n, check=True)
        tmp = sum_k_3_2_k(n, check=True)

    n_max = 20
    m_max = 3

    for n in range(n_max):
        for m in range(1, m_max):
            tmp = sum_2_m_i(m, n, check=True)
            tmp = sum_m_2_m_i(m, n, check=True)

    n_max = 20
    for n in range(2, n_max):
        tmp = sum_0(n, check=True)
        tmp = sum_1(n, check=True)
        tmp = sum_2(n, check=True)
        tmp = sum_3(n, check=True)
        tmp = sum_4(n, check=True)

    print("-- done --")

