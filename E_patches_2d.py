import sys

def E_(n):
    return 2**n

def S(m, n, i, j, verify=False):

    result = (m - i + 1) * (n - j + 1) * E_(m*n - i*j)

    return result


def E_patches_2d_as_derived(m, n):
    # Verified up to computability

    ul1 = 1

    def Y(m, n):

        if m == 1 and n == 1:
            return 1

        elif m == 1:
            return E_(n - 2)
        
        elif n == 1:
            return E_(m - 2)

        else:

            y_A = y_B = y_D = E_(m*n - 4)
            y_C1 = E_(m*n - 4 - (n - 2)) * (E_(n-2) - 1)
            y_C2 = E_(m*n - 4 - (m - 2)) * (E_(m-2) - 1)
            y_E = E_((m - 1)*(n - 1) - 1) * (E_(m-2) - 1) * (E_(n-2) - 1)
            y_F = E_((m - 2) * (n - 2)) * (E_(m-2) - 1) * (E_(n-2) - 1) * (E_(m-2) - 1) * (E_(n-2) - 1)

            result = y_A + 4 * y_B + 2 * y_C1 + 2 * y_C2 + 2 * y_D + 4 * y_E + y_F
            return result

    e = 0
    for i in range(1, m + ul1):
        for j in range(1, n + ul1):
            f = (m - i + 1) * (n - j + 1) * E_(m * n - i * j)
            e += f * Y(i, j)

    result = 2 * e

    return result


def E_patches_2d(m, n, check=False):

    def Y(m, n):

        # Use only if m > 1 and n > 1

        result = 0

        result +=  E_(2*m + 2*n)
        result += -2 * E_(2*m + n)
        result += -2 * E_(m + 2*n)
        result += 8 * E_(m + n)
        result += E_(2*m)
        result += E_(2*n)
        result += - 8 * E_(m)               
        result += - 8 * E_(n)
        result += 16

        return result

    g = 0
    g += (1/324) * (81 * m*m*n*n - 189 * m*n*(m + n) + 927 * m*n + 306*(m*m + n*n) - 1290 * (m + n) + 2080)
    g += -(1/9) * (64 - 39*m + 9*m*m) * E_(-n) 
    g += -(1/9) * (64 - 39*n + 9*n*n) * E_(-m) 
    g += (1/162) * (112 - 57*n + 9*n*n) * E_(-2*m)
    g += (1/162) * (112 - 57*m + 9*m*m) * E_(-2*n)
    g += 8 * E_(-(m+n))
    g += -(8/9) * (E_(-(m+2*n)) + E_(-(n+2*m)))
    g += (16/81) * E_(-2*(m+n))
        
    result = 2 * g * E_(m*n)

    check = E_patches_2d_as_derived(m, n)
    if abs(result - check) > 0.00001:
        print("did not verify")

    return int(round(result))

def E_patches_2d_maximally_simplified(m, n, check=False):

    g = 0

    g += 8 * 443
    g += -8 * 9 * 29 * (m + n)
    g += 24 * (1 - 9*m) * (1 - 9*n)
    g += 4 * (34 - 21*m + 9*m*m)*(34 - 21*n + 9*n*n)
    
    g += -144 * (56 - 39*m + 9*m*m) * E_(-n) 
    g += -144 * (56 - 39*n + 9*n*n) * E_(-m) 
    g += 8 * (96 - 57*m + 9*m*m) * E_(-2*n)
    g += 8 * (96 - 57*n + 9*n*n) * E_(-2*m)
    g += 64 * (1 - 9*E_(-m)) * (1 - 9*E_(-n))
    g += 64 * (1 - 9*E_(-m) + 2*E_(-2*m)) * (1 - 9*E_(-n) + 2*E_(-2*n))

    result = (1 / 648) * g * E_(m*n)

    check = E_patches_2d_as_derived(m, n)
    if abs(result - check) > 0.00001:
        print("did not verify")

    return int(round(result))


if __name__ == "__main__":  

    for m in range(1, 6):
        for n in range(m, 6):
            test = E_patches_2d(m, n)
            test_2 = E_patches_2d_maximally_simplified(m, n)
            if test != test_2:
                print("E_patches_2d versions disagree")
            print("m = " + str(m) + ", n = " + str(n) + ", E = " + str(int(round(test))))

    print("-- done --")