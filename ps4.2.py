#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
# 
# Your code should run in Theta(n) time
#

import random

def partition(L, v):
    smaller = []
    bigger = []
    middle = []
    for elem in L:
        if elem < v: smaller.append(elem)
        elif elem > v: bigger.append(elem)
        else: middle.append(elem)
    return (smaller, middle, bigger)

def find_mid(L, m, sm_r, bg_l):
    v = L[random.randrange(len(L))]
    (left, middle, right) = partition(L, v)
    if sm_r + len(left) + len(middle) - 1 == m: 
        return middle[0]
    if sm_r + len(left) + len(middle) - 1 > m: 
        return find_mid(left + middle, m, sm_r, sm_r + len(left) + len(middle))
    if sm_r + len(left) + len(middle) - 1 < m: 
        return find_mid(middle + right, m , sm_r + len(left), bg_l)

def minimize_absolute(L):
    mp = len(L) / 2
    return find_mid(L, mp, 0, len(L))

def test():
    L = [4, 3, 9, 2, 11, 5, 7, 53, 12, 27, 2]
#   L = [2, 2, 3, 4]
#   L = [6, 5, 4, 5]
    mid = minimize_absolute(L)
    sr = sorted(L)
    print sr
    print mid
    assert mid == sr[len(L) / 2]

test()
