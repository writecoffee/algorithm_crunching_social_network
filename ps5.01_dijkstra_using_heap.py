#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

import heapq

def dijkstra(G,v):
    heap, TX, X = [(0, v)], {v:0}, {}

    while heap:
        (w, k) = heapq.heappop(heap)

        # jump over deprecated values
        if k in X or w > TX[k]:
            continue

        X[k] = w

        for neighbor in G[k]:
            nw = X[k] + G[k][neighbor]
            if neighbor not in X and (neighbor not in TX or nw < TX[neighbor]):
                TX[neighbor] = nw
                heapq.heappush(heap, (nw, neighbor))

    return X

#
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G

def test():
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    for elem in 'ABCDEFG':
        dist = dijkstra(G, elem)
        print dist

test()
