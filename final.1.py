#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where 
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

from collections import deque

def bipartite(G):
    if not G:
        return None
    start = next(G.iterkeys())
    lfrontier, rexplored, L, R = deque([start]), set(), set(), set()
    while lfrontier:
        head = lfrontier.popleft()
        if head in rexplored: 
            return None
        if head in L: 
            continue
        L.add(head)
        for successor in G[head]:
            if successor in rexplored:
                continue
            R.add(successor)
            rexplored.add(successor)
            for nxt in G[successor]:
                lfrontier.append(nxt)
    return L



########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5), (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None

test()
