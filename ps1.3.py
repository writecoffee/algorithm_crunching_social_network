# Eulerian Tour Ver 1
#
# Write a function, `create_tour` that takes as
# input a list of nodes
# and outputs a list of tuples representing
# edges between nodes that have an Eulerian tour.
#

import random

#################### my code ####################################

def create_tour_random(nodes):
    connected = []
    degree = {}
    unconnected = [n for n in nodes]
    tour = []
    # create a connected graph first, pick two random nodes from an edge
    x = poprandom(unconnected)
    y = poprandom(unconnected)
    connected.append(x)
    connected.append(y)
    tour.append(edge(x, y))
    degree[x] = 1
    degree[y] = 1
    # then pick a random edge from the unconnected list and create an edge tuple
    while len(unconnected) > 0:
        x = pickrandom(connected)
        y = poprandom(unconnected)
        connected.append(y)
        tour.append(edge(x, y))
        degree[x] += 1
        degree[y] = 1
    # now make sure each node has an even degree
    odd_nodes = [k for k , v in degree.items() if v % 2 == 1]
    even_nodes = [k for k, v in degree.items() if v % 2 == 0]
    # there will always be an even number of odd nodes, so we can just connect
    # pairs of unconnected edges
    while len(odd_nodes) > 0:
        x = poprandom(odd_nodes)
        cn = check_nodes(x, odd_nodes, tour)
        if cn is not None:
            even_nodes.append(x)
            even_nodes.append(cn)
            tour.append(edge(x, cn))
        else:
            cn = check_nodes(x, even_nodes, tour)
            if cn is not None:
                odd_nodes.append(cn)
                even_nodes.append(x)
                tour.append(edge(cn, x))
    # return
    return tour

def edge(v1, v2):
    return (v1, v2)

def poprandom(nodes):
    if len(nodes) > 0:
        index = random.randint(0, len(nodes) - 1)
        return nodes.pop(index)

def pickrandom(nodes):
    return random.choice(nodes)

def check_nodes(b, nodes, tour):
    for n in nodes:
        if (b, n) not in tour and (n, b) not in tour:
            nodes.remove(n)
            return n
    return None
    

#################################################################

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
    # and every node must be in graph
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
        print "Your graph wasn't connected"
        return False

def test():
    nodes = [0, 1, 2, 3, 4]
    tour = create_tour_random(nodes)
    print tour
    return is_eulerian_tour(nodes, tour)

print test()
