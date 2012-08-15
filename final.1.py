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

def is_bipartite(G, L, R):
    for node in L:
        if not len(G[node].keys()):
            return False
        for neighbor in G[node]:
            if neighbor in L:
                return False
    for node in R:
        if not len(G[node].keys()):
            return False
        for neighbor in G[node]:
            if neighbor in R:
                return False
    return True

def k_subset(nodes, k):
    if len(nodes) < k:
        return []
    if len(nodes) == k:
        return [nodes]
    if k == 1:
        return [[i] for i in nodes]
    return k_subset(nodes[1:], k) + map(lambda x: x + [nodes[0]], k_subset(nodes[1:], k - 1))

def bipartite(G):
    for k in range(1, len(G.keys()) / 2 + 1):
        for L in k_subset(G.keys(), k):
            R = set(G.keys()) - set(L)
            if is_bipartite(G, L, R):
                return set(L)
    return None


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
