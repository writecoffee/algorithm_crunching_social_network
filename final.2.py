#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#

import heapq

def feel_the_love(G, i, j):
    # return a path (a list of nodes) between `i` and `j`,
    # with `i` as the first node and `j` as the last node,
    # or None if no path exists
    dist_so_far = {i:0}
    final_dist = {}
    heap = [(0, i)]
    route = {i:[i]}
    while dist_so_far:
        (w, k) = heapq.heappop(heap)
        # jump over deprecated values
        if k in final_dist or (k in dist_so_far and w < dist_so_far[k]):
            continue
        del dist_so_far[k]
        final_dist[k] = w
        for neighbor in G[k]:
            # one step iteration for Dijkstra
            if neighbor not in final_dist:
                nw = G[k][neighbor]
                if neighbor not in dist_so_far or nw > dist_so_far[neighbor]:
                    route[neighbor] = route[k] + [neighbor]
                    heapq.heappush(heap, (nw, neighbor))
                    dist_so_far[neighbor] = nw
            # allow a cycle and never trace backward
            elif neighbor != route[k][len(route[k]) - 2]:
                oldw = final_dist[neighbor]
                # during the cycle, recompute the loop-start and its neighbors
                if w > oldw:
                    dist_so_far[neighbor] = w
                    route[neighbor] = route[k] + [neighbor]
                    heapq.heappush(heap, (w, neighbor))
                    del final_dist[neighbor]
    if j not in route:
        return None
    else:
        return route[j]

#########
#
# Test

def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love

def test():
    G = {'a':{'c':1},
         'b':{'c':1},
         'c':{'a':1, 'b':1, 'e':1, 'd':1},
         'e':{'c':1, 'd':2},
         'd':{'e':2, 'c':1},
         'f':{}}
    path = feel_the_love(G, 'a', 'b')
    print path
    assert score_of_path(G, path) == 2
    path = feel_the_love(G, 'a', 'f')
    assert path == None

test()

