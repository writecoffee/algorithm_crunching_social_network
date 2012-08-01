#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

def shortest_dist_node(dist_so_far, dist_heapq):
    if len(dist_heapq) > 1:
        (key, val) = dist_heapq[0]
        # remove the end of list
        dist_heapq[0] = dist_heapq.pop(len(dist_heapq) - 1)
        # update the index mapping
        del dist_so_far[key]
        dist_so_far[getk(root(dist_heapq))] = 0
        down_heapify(dist_so_far, dist_heapq, 0)
        return (key, val)
    else:
        del dist_so_far[getk(root(dist_heapq))]
        return dist_heapq.pop()

def insert(S, L, (key, val)):
    L.append((key, val))
    S[key] = len(L) - 1
    up_heapify(S, L, len(L) - 1)

def update(S, L, (key, new_val)):
    L[S[key]] = (key, new_val)
    up_heapify(S, L, S[key])

def up_heapify(S, L, i):
    if i is 0:
        return
    if getv(L[i]) < getv(L[parent(i)]):
        swap(S, L, i, parent(i))
        up_heapify(S, L, parent(i))

def swap(S, L, a, b):
    (L[a], L[b]) = (L[b], L[a])
    (S[getk(L[a])], S[getk(L[b])]) = (S[getk(L[b])], S[getk(L[a])])

def down_heapify(S, L, i):
    if leaf(L, i):
        return
    if one_child(L, i):
        if getv(L[left_child(i)]) < getv(L[i]):
            swap(S, L, i, left_child(i))
        return
    if min(getv(L[left_child(i)]), getv(L[right_child(i)])) < getv(L[i]):
        if getv(L[left_child(i)]) < getv(L[right_child(i)]):
            swap(S, L, i, left_child(i))
            down_heapify(S, L, left_child(i))
        else:
            swap(S, L, i, right_child(i))
            down_heapify(S, L, right_child(i))

def root(L):
    return L[0]

def leaf(L, index):
    if left_child(index) >= len(L):
        return True
    else:
        return False

def one_child(L, index):
    if right_child(index) >= len(L):
        return True
    else:
        return False

def left_child(index):
    return 2 * index + 1

def right_child(index):
    return 2 * index + 2

def parent(index):
    return (index - 1) / 2

def getv((key, val)):
    return val

def getk((key, val)):
    return key

def dijkstra(G,v):
    dist_heapq = [(v, 0)]
    dist_so_far = {v:0}
    final_dist = {}
    while len(final_dist) < len(G):
        (w, wd) = shortest_dist_node(dist_so_far, dist_heapq)
        # lock it down!
        final_dist[w] = wd
        # iterate all neighbors
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    insert(dist_so_far, dist_heapq, (x, final_dist[w] + G[w][x]))
                elif final_dist[w] + G[w][x] < getv(dist_heapq[dist_so_far[x]]):
                    update(dist_so_far, dist_heapq, (x, final_dist[w] + G[w][x]))
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
