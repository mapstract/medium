import sys

import math

def E_(n):
    return 2**n

def z(k):
    # z(k) is the number of runs of length (n - k + 1) bits in the set of all possible
    # binary strings of length k.
    # (I forgot how I derived this, and threw away my original notes.)

    # I also asked the same question in Stack Exchange without remembering I had answered
    # the question - and Rezha Tanuharja solved it!

    if k == 1:
        result = 1
    else:
        result = int((k + 2) * E_(k - 3))
    return result

def nCm(n,m):
    f = math.factorial
    return f(n) / f(m) / f(n-m)

def E_patches_1d(n):
    return (n * (n + 3) / 4) * E_(n)

def E_patches_1d_toroidal(n):
    return ((n*n - n + 4) / 2) * E_(n)  - 2

