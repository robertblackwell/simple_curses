
from typing import List

class Rectangle:
    def __init__(self, nbr_rows, nbr_cols, y_beg, x_beg ):
        self.nbr_rows = nbr_rows
        self.nbr_cols = nbr_cols
        self.y_begin = y_beg
        self.x_begin = x_beg

class Partitian:
    def __init__(self, n: int, k: int):
        """Partitian n into k groups of a close to equal size as possible"""
        p = n // k
        r = n % k
        dim = k + 1
        if r == 0:
            dim = k
        index = 0
        self.groups = [0]*dim
        for i in range(0, n):
            if index == dim:
                index = 0
            self.groups[index] += 1
            index += 1

