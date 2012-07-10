# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

import copy
import itertools

def find_eulerian_tour(graph):
    nodes = []
    tour = []
    # iterately pick each starting edge in the graph to find tour
    for edge in graph:
        for v, w in itertools.permutations(edge):
            tg = copy.deepcopy(graph)
            tg.remove((v, w))
            s, n = v, w
            nodes.append(s)
            nodes.append(n)
            tour.append(make_edge(s, n))
            result = leap_in(tg, nodes, n, tour)
            if result:
                return result
            else:
                # retrace the searching path
                nodes.pop()
                nodes.pop()
                tour.pop()
    return None
            
def leap_in(graph, nodes, n, tour):
    related = [(v, w) for v, w in graph if v == n or w == n]
    # for each edge yields a new path until it reaches a dead end
    for edge in related:
        tg = copy.deepcopy(graph)
        tg.remove(edge)
        for v, w in itertools.permutations(edge):
            if v == n:
                nodes.append(w)
                tour.append(make_edge(n, w))
                result = leap_in(tg, nodes, w, tour)
                if result:
                    return result
                else:
                    # retrace the searching path
                    nodes.pop()
                    tour.pop()
    # recurrence reaching a dead end
    if nodes[0] == nodes[len(nodes) - 1] and not graph:
        return nodes, tour
    else:
        return None

def make_edge(v1, v2):
    return (v1, v2)

def get_degree(tour):
    degree = {}
    for x, y in tour:
        degree[x] = degree.get(x, 0) + 1
        degree[y] = degree.get(y, 0) + 1
    return degree

def check_edge(t, b, nodes):
    """
    t: tuple representing an edge
    b: origin node
    nodes: set of nodes already visited

    if we can get to a new node from `b` following `t`
    then return that node, else return None
    """
    if t[0] == b:
        if t[1] not in nodes:
            return t[1]
    elif t[1] == b:
        if t[0] not in nodes:
            return t[0]
    return None

def connected_nodes(tour):
    """return the set of nodes reachable from
    the first node in `tour`"""
    a = tour[0][0]
    nodes = set([a])
    explore = set([a])
    while len(explore) > 0:
        # see what other nodes we can reach
        b = explore.pop()
        for t in tour:
            node = check_edge(t, b, nodes)
            if node is None:
                continue
            nodes.add(node)
            explore.add(node)
    return nodes

def is_eulerian_tour(nodes, tour):
    # all nodes must be even degree
    # and every node must be in tour
    degree = get_degree(tour)
    for node in nodes:
        try:
            d = degree[node]
            if d % 2 == 1:
                print "Node %s has odd degree" % node
                return False
        except KeyError:
            print "Node %s was not in your tour" % node
            return False
    connected = connected_nodes(tour)
    if len(connected) == len(nodes):
        return True
    else:
        print "Your tour wasn't connected"
        return False

def tc_1():
    print "test case -- 1"
    graph = [(1, 2), (2, 3), (3, 1)]
    nodes, tour = find_eulerian_tour(graph)
    print nodes
    print tour
    if is_eulerian_tour(set(nodes), tour):
        print "Is Eulerian Tour"
    else:
        print "Not Eulerian Tour"

def tc_2():
    print "test case -- 2"
    graph = [(0, 1), (1, 5), (1, 7), (4, 5), 
            (4, 8), (1, 6), (3, 7), (5, 9), 
            (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
    nodes, tour = find_eulerian_tour(graph)
    print nodes
    print tour
    if is_eulerian_tour(set(nodes), tour):
        print "Is Eulerian Tour"
    else:
        print "Not Eulerian Tour"

def tc_3():
    print "test case -- 3"
    graph = [(1, 13), (1, 6), (6, 11), (3, 13),
            (8, 13), (0, 6), (8, 9),(5, 9), 
            (2, 6), (6, 10), (7, 9), (1, 12),
            (4, 12), (5, 14), (0, 1), (2, 3),
            (4, 11), (6, 9), (7, 14), (10, 13)]
    nodes, tour = find_eulerian_tour(graph)
    print nodes
    print tour
    if is_eulerian_tour(set(nodes), tour):
        print "Is Eulerian Tour"
    else:
        print "Not Eulerian Tour"

def tc_4():
    print "test case -- 4"
    graph = [(8, 16), (8, 18), (16, 17), (18, 19),
            (3, 17), (13, 17), (5, 13),(3, 4),
            (0, 18), (3, 14), (11, 14), (1, 8),
            (1, 9), (4, 12), (2, 19),(1, 10),
            (7, 9), (13, 15), (6, 12), (0, 1),
            (2, 11), (3, 18), (5, 6), (7, 15),
            (8, 13), (10, 17)]
    nodes, tour = find_eulerian_tour(graph)
    print nodes
    print tour
    if is_eulerian_tour(set(nodes), tour):
        print "Is Eulerian Tour"
    else:
        print "Not Eulerian Tour"
    
tc_1()
tc_2()
tc_3()
tc_4()
