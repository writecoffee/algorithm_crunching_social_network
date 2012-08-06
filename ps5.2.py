# compute the weight of co-appear

import csv
import operator
import heapq

def make_link(G, name, book):
    if name not in G:
        G[name] = {}
    (G[name])[book] = 1
    if book not in G:
        G[book] = {}
    (G[book])[name] = 1
    return G

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

def HG_make_link(CG, ch1, ch2):
    if ch1 not in CG:
        CG[ch1] = {}
    if ch2 not in CG:
        CG[ch2] = {}
    if ch2 not in CG[ch1]:
        CG[ch1][ch2] = 0
    if ch1 not in CG[ch2]:
        CG[ch2][ch1] = 0
    CG[ch1][ch2] += 1
    CG[ch2][ch1] += 1

def make_hop_graph(G, characters):
    HG = {}
    for ch1 in characters:
        for book in G[ch1]:
            for ch2 in G[book]:
                # avoid double counting the route quantities
                if ch1 > ch2: HG_make_link(HG, ch1, ch2)
    return HG

def WG_make_link(HG, WG, ch1, ch2, routes):
    routes[ch1], WG[ch1] = dijkstra(HG, ch1)

def make_weight_graph(HG, characters):
    WG = {} 
    routes = {}
    for ch1 in HG:
        for ch2 in HG[ch1]:
            if ch1 > ch2: WG_make_link(HG, WG, ch1, ch2, routes)
    return WG, routes

# should compute the entire route: len([v, b, c, e])
def dijkstra(HG, v):
    heap = [(0, v)]
    dist_so_far = {v: 0}
    route_cnt = {v: 0}
    final_dist = {}
    while dist_so_far:
        (w, k) = heapq.heappop(heap)
        if k in final_dist or (k in dist_so_far and w > dist_so_far[k]):
            continue
        else:
            del dist_so_far[k]
            final_dist[k] = w
        for neighbor in [nb for nb in HG[k] if nb not in final_dist]:
            nw = final_dist[k] + 1.00 / HG[k][neighbor]
            if neighbor not in dist_so_far or nw < dist_so_far[neighbor]:
                dist_so_far[neighbor] = nw
                route_cnt[neighbor] = route_cnt[k] + 1
                heapq.heappush(heap, (final_dist[k] + 1.00 / HG[k][neighbor], neighbor))
    return route_cnt, final_dist

def sub_test():
    (marvelG, characters) = ({
            'A': {'AB_book', 'AC_book', 'ABCD_book', 'AB_book2'},
            'AB_book': {'A', 'B'},
            'AB_book2': {'A', 'B'},
            'B': {'AB_book', 'BD_book', 'ABCD_book', 'AB_book2'},
            'BD_book': {'B', 'D'},
            'D': {'BD_book', 'CD_book', 'ABCD_book'},
            'CD_book': {'C', 'D'},
            'C': {'CD_book', 'AC_book', 'ABCD_book'},
            'AC_book': {'A', 'C'},
            'ABCD_book': {'A', 'B', 'C', 'D'}
        }, {'A': 1, 'B': 1, 'C': 1, 'D': 1})
    HG = make_hop_graph(marvelG, characters)
    (WG, w_routes) = make_weight_graph(HG, characters)
    print HG
    print WG
    print w_routes
    count = 0
    for ch1 in w_routes:
        for ch2 in w_routes[ch1]:
            if ch1 != ch2 and 1 != w_routes[ch1][ch2]:
                count += 1
    print count

def test():
    (marvelG, characters) = read_graph('marvel_graph')
    HG = make_hop_graph(marvelG, characters)
    (WG, w_routes) = make_weight_graph(HG, characters)
    count = 0
    for ch1 in w_routes:
        for ch2 in w_routes[ch1]:
            if ch1 != ch2 and 1 != w_routes[ch1][ch2]:
                count += 1
    print count

sub_test()
test()
