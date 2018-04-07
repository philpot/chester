#!/usr/bin/env python

from __future__ import print_function

from collections import MutableSequence

def fval(f):
    return {'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7}[f.lower()]


def canon_indices(indices):
    (f, r) = indices
    try:
        x = f - 1
    except:
        x = fval(f)
    y = r - 1
    if 1 <= x <= 8 and 1 <= y <= 8:
        return (x, y)
    else:
        raise ValueError

def impl_y(r):
    y = r - 1
    if 0 <= y <= 7:
        return y
    else:
        raise ValueError

def impl_x(f):
    try:
        x = f - 1
    except:
        x = fval(f)
    if 0 <= x <= 7:
        return x
    else:
        raise ValueError

class Chessboard(MutableSequence):
    def __init__(self):

        self.b = [[ 64,  32,  48,  80,  82,  50,  34,  66],
                  [ 16,  18,  20,  22,  24,  26,  28,  30],
                  [  0,   0,   0,   0,   0,   0,   0,   0],
                  [  0,   0,   0,   0,   0,   0,   0,   0],
                  [  0,   0,   0,   0,   0,   0,   0,   0],
                  [  0,   0,   0,   0,   0,   0,   0,   0],
                  [144, 146, 148, 150, 152, 154, 156, 158],
                  [192, 160, 176, 208, 224, 178, 162, 194]]

# pw   0 001 000 0 .. 0 001 111 0  16,  18,  20,  22,  24,  26,  28,  30
# pb   1 001 000 0 .. 1 001 111 0 144, 146, 148, 150, 152, 154, 156, 158
# Nw   0 010 000 0 .. 0 010 001 0  32,  34
# Nb   1 010 000 0 .. 1 010 001 0 160, 162
# Bw   0 011 000 0 .. 0 011 001 0  48,  50
# Bb   1 011 000 0 .. 1 011 001 0 176, 178
# Rw   0 100 000 0 .. 0 100 001 0  64,  66
# Rb   1 100 000 0 .. 1 100 001 0 192, 194
# Qw   0 101 000 0                 80 (.. 82, ...)
# Qb   1 101 000 0                208 (.. 210, ...)
# Kw   0 110 000 0                 96
# Kb   1 110 000 0                224

        super(Chessboard, self).__init__()

    def __getitem__(self, indices):
        (x, y) = canon_indices(indices)
        return self.b[y][x]

    def __delitem__(self, i):
        pass

    def __setitem__(self, indices, val):
        (x, y) = canon_indices(indices)
        self.b[y][x] = val

    def insert(self, i):
        pass

    def __len__(self):
        return len(self.b)

    def rank(self, r):
        return self.b[impl_y(r)]

    def file(self, f):
        x = impl_x(f)
        return [row[x] for row in self.b]
