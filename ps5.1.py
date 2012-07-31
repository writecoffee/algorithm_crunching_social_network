#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

def shortest_dist_node(dist):
    if len(dist) > 1:
        result = dist[0]
        dist[0] = dist.pop(len(dist) - 1)
        down_heapify(dist, 0)
        return result
    else:
        return dist.pop()

def insert(L, (key, val)):
    L.append((key, val))
    up_heapify(L, len(L) - 1)

def update(L, (key, new_val)):
    index = find(L, key)
    L[index] = (key, new_val)
    up_heapify(L, index)

def find(L, key):
    d = dict(L)
    if key not in d.keys():
        return None
    else:
        return L.index((key, d[key]))

def up_heapify(L, index):
    if index is 0:
        return
    if val(L[index]) < val(L[parent(index)]):
        (L[index], L[parent(index)]) = (L[parent(index)], L[index])
        up_heapify(L, parent(index))

def down_heapify(L, index):
    if leaf(L, index):
        return
    if one_child(L, index):
        if val(L[left_child(index)]) < val(L[index]):
            (L[index], L[left_child(index)]) = (L[left_child(index)], L[index])
        return
    if min(val(L[left_child(index)]), val(L[right_child(index)])) < val(L[index]):
        if val(L[left_child(index)]) < val(L[right_child(index)]):
            (L[index], L[left_child(index)]) = (L[left_child(index)], L[index])
            down_heapify(L, left_child(index))
        else:
            (L[index], L[right_child(index)]) = (L[right_child(index)], L[index])
            down_heapify(L, right_child(index))

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

def val((key, val)):
    return val

def dijkstra(G,v):
    dist_so_far = [(v, 0)]
    final_dist = {}
    while len(final_dist) < len(G):
        print dist_so_far
        (w, wd) = shortest_dist_node(dist_so_far)
        # lock it down!
        final_dist[w] = wd
        # iterate all neighbors
        for x in G[w]:
            if x not in final_dist:
                xi = find(dist_so_far, x)
                if xi is None:
                    insert(dist_so_far, (x, final_dist[w] + G[w][x]))
                elif final_dist[w] + G[w][x] < dist_so_far[xi]:
                    update(dist_so_far, (x, final_dist[w] + G[w][x]))
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

    dist = dijkstra(G, a)
    print dist
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)

test()
