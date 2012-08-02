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
    heap, dist_so_far, final_dist = [(0, v)], {v:0}, {}
    while dist_so_far:
        (w, k) = heapq.heappop(heap)
        # jump over deprecated values
        if k in final_dist or (k in dist_so_far and w > dist_so_far[k]):
            continue
        else:
            del dist_so_far[k]
            final_dist[k] = w
        for neighbor in [nb for nb in G[k] if nb not in final_dist]:
            nw = final_dist[k] + G[k][neighbor]
            if neighbor not in dist_so_far or nw < dist_so_far[neighbor]:
                dist_so_far[neighbor] = nw
                # insert the new value first and jump over the older later
                heapq.heappush(heap, (final_dist[k] + G[k][neighbor], neighbor))
    return final_dist

############
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
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    for elem in 'ABCDEFG':
        dist = dijkstra(G, elem)
        print dist
#    assert dist[g] == 8 #(a -> d -> e -> g)
#    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)

test()
