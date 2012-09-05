#
# This is the same problem as "Distance Oracle I" except that instead of
# only having to deal with binary trees, the assignment asks you to
# create labels for all tree graphs.
#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a tree and returns a dictionary, mapping each
# node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#
import random
import math
import pdb
import random

def count_nodes(treeG, node):
    # count all sub-nodes including itself
    cnts = {}
    visited = {}
    cnts[node] = count_nodes_rec(treeG, node, cnts, visited)
    return cnts

def count_nodes_rec(treeG, node, cnts, visited):
    visited[node] = True
    frontier = [node]
    cnts[node] = 1
    for v in treeG[node]:
        if v not in visited:
            cnts[node] += count_nodes_rec(treeG, v, cnts, visited)
    return cnts[node]

def create_labels(treeG):
    # find center node via rotation
    def find_cen(treeG, tmt_root, cnts):
        if cnts[tmt_root] == 1:
            return tmt_root
        mcc, mc = max((cnts[v], v) for v in treeG[tmt_root] if v not in cens_nodes)
        # center node found!
        if cnts[tmt_root] - mcc >= mcc:
            return tmt_root
        # rotate 'tmt_root' to mc
        cnts[mc] += cnts[tmt_root] - mcc
        cnts[tmt_root] -= mcc
        return find_cen(treeG, mc, cnts)
    # recursively finding center node for each 'sub-tree'
    def label_tree(tmt_root):
        cen = find_cen(treeG, tmt_root, cnts)
        label_sub(cen)
        for child in treeG[cen]:
            if child not in cens_nodes:
                label_tree(child)
    # BFS routine for tagging each descendant node with its sub-center node
    def label_sub(sub_cen):
        if sub_cen not in labels:
            labels[sub_cen] = {}
        labels[sub_cen][sub_cen] = 0
        cens_nodes[sub_cen] = True
        frontier = [sub_cen]
        visited = {}
        while frontier:
            v = frontier.pop(0)
            for neighbor in treeG[v]:
                if neighbor not in visited and neighbor not in cens_nodes:
                    visited[neighbor] = True
                    frontier += [neighbor]
                    if neighbor not in labels:
                        labels[neighbor] = {neighbor: 0}
                    labels[neighbor][sub_cen] = treeG[v][neighbor] + labels[v][sub_cen]
    #pdb.set_trace()
    cens_nodes = {}
    labels = {}
    tmt_root = iter(treeG).next()
    cnts = count_nodes(treeG, tmt_root)
    label_tree(tmt_root)
    return labels




#######
# Testing
#


def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    print labels
    if labels:
        distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][4] == 2
    assert distances[1][2] == 1
    assert distances[1][4] == 2
    assert distances[4][1] == 2
    assert distances[1][4] == 2
    assert distances[2][1] == 1
    assert distances[1][2] == 1
    assert distances[1][1] == 0
    assert distances[2][2] == 0
    assert distances[9][9] == 0
    assert distances[2][3] == 2
    assert distances[12][13] == 2
    assert distances[13][8] == 6
    assert distances[11][12] == 6
    assert distances[1][12] == 3

test()

def test2():
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
             (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    print labels
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][3] == 2
    assert distances[1][13] == 12
    assert distances[6][1] == 5
    assert distances[6][13] == 7
    assert distances[8][3] == 5
    assert distances[10][4] == 6
    print('test2 passed')

test2()
