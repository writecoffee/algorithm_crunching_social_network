#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
#

global cnn_comp
cnn_comp = {}

def process_graph(G):
    i = 0
    visited = {}
    for u in G:
        if u not in visited:
            to_cnn = [u]
            while to_cnn:
                n = to_cnn.pop()
                visited[n] = True
                cnn_comp[n] = i
                to_cnn += [v for v in G[n] if v not in visited]
            i += 1

#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def is_connected(i, j):
    return cnn_comp[i] == cnn_comp[j]

#######
# Testing
#
def test():
    G = {1:{2:1},
         2:{1:1},
         3:{4:1},
         4:{3:1},
         5:{}}
    process_graph(G)
    assert is_connected(1, 2) == True
    assert is_connected(1, 3) == False

    G = {1:{2:1, 3:1},
         2:{1:1},
         3:{4:1, 1:1},
         4:{3:1},
         5:{}}
    process_graph(G)
    assert is_connected(1, 2) == True
    assert is_connected(1, 3) == True
    assert is_connected(1, 5) == False

test()
