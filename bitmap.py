import sys

import math
import numpy as np
from numpy.ma.core import is_string_or_list_of_strings

import utilities

# Credentials:

# git:
# git clone https://github.com/mapstract/medium.git

# AWS
# PAT: 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
# ssh -i /Users/brianbunker/Dropbox/aws/pem/brian.pem  ec2-user@ec2-18-217-114-64.us-east-2.compute.amazonaws.com
# ssh -i /Users/brianbunker/Dropbox/aws/pem/brian.pem  ubuntu@ - is this valid?

# c6g.8xlarge
# to-do:

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

