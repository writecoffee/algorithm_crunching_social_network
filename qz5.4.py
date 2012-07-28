# compute the weight of co-appear

import csv
import operator

def up_heapify(L, i):
    s = i
    while s is not 0: 
        if L[s] < L[parent(s)]:
            (L[parent(s)], L[s]) = (L[s], L[parent(s)])
            s = parent(s)
        else:
            break 

def down_heapify(L, i):
    # leaf
    if leaf(L, i): return
    # only one child
    if one_child(L, i):
        if L[i] > L[left(i)]:
            (L[i], L[left(i)]) = (L[left(i)], L[i])
        return
    # two children
    if min(L[left(i)], L[right(i)]) >= L[i]:
        return
    if L[left(i)] < L[right(i)]:
        (L[i], L[left(i)]) = (L[left(i)], L[i])
        down_heapify(L, left(i))
        return
    else:
        (L[i], L[right(i)]) = (L[right(i)], L[i])
        down_heapify(L, right(i))
        return

def leaf(L, i): return right(i) >= len(L) and left(i) >= len(L)

def one_child(L, i): return right(i) == len(L)

def left(i): return i * 2 + 1

def right(i): return i * 2 + 2

def parent(i): return (i - 1) / 2

def insert(L, nv):
    L.append(nv)
    up_heapify(L, len(L) - 1)

def pop_min(L):
    L[0] = L.pop()
    down_heapify(L, 0)

def make_link(G, name, book):
    if name not in G:
        G[name] = {}
    (G[name])[book] = 1
    if book not in G:
        G[book] = {}
    (G[book])[name] = 1
    return G

def CG_make_link(CG, ch1, ch2):
    if ch1 not in CG:
        CG[ch1] = {}
    if ch2 not in CG[ch1]:
        CG[ch1][ch2] = 1
    # accumulate strengths
    else:
        CG[ch1][ch2] += 1

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    characters = {}
    for (node1, node2) in tsv:
        make_link(G, node1, node2)
        if node1 not in characters:
            characters[node1] = 1
    return G, characters

def make_char_graph(G, characters):
    CG = {}
    for ch1 in characters:
        for book in G[ch1]:
            for ch2 in G[book]:
                # avoid double counting the values
                if ch1 > ch2: CG_make_link(CG, ch1, ch2)
    return CG

def get_top(CG, characters, k):
    heap = []
    for ch1 in CG.keys():
        for ch2 in CG[ch1]:
            if len(heap) < k:
                insert(heap, (CG[ch1][ch2], (ch1, ch2)))
            elif CG[ch1][ch2] > heap[0][0]:
                pop_min(heap)
                insert(heap, (CG[ch1][ch2], (ch1, ch2)))
    return heap

def test():
    (marvelG, characters) = read_graph('marvel_graph')
    CG = make_char_graph(marvelG, characters)
    top10 = get_top(CG, characters, 10)
    for t in sorted(top10, reverse=True):
        print t

test()
