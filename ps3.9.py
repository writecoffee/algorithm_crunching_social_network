# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs 
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
# 
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1}, 
#      'b': {'a': 1, 'd': 1}, 
#      'c': {'a': 1, 'd': 1}, 
#      'd': {'c': 1, 'b': 1, 'e': 1}, 
#      'e': {'d': 1, 'g': 1, 'f': 1}, 
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1} 
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'}, 
#      'b': {'a': 'green', 'd': 'red'}, 
#      'c': {'a': 'green', 'd': 'green'}, 
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'} 
#      }
#       

import itertools

def create_rooted_spanning_tree(G, root):
    S = {root:{}}
    node_list = [root]
    node_exists = {root:True}
    while node_list:
        curr = node_list.pop()
        rvs = [val for val in G[curr].keys()]
        rvs.reverse()
        for neighbor in rvs:
            if neighbor not in node_exists:
                node_exists[neighbor] = True
                node_list.append(neighbor)
                S[neighbor] = {}
                S[curr][neighbor] = 'green'
            elif curr in S[neighbor] and S[neighbor][curr] == 'green':
                S[curr][neighbor] = 'green'
            else:
                S[curr][neighbor] = 'red'
    return S

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'}, 
                 'b': {'a': 'green', 'd': 'red'}, 
                 'c': {'a': 'green', 'd': 'green'}, 
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'} 
                 }

###########

def post_order(S, root):
    # return mapping between nodes of S and the post-order value
    # of that node
    po = {}
    visited = {root:True}
    node_list = [root]
    i = 1
    while node_list:
        curr = node_list[len(node_list) - 1]
        leaf = True
        for desc in S[curr]:
            if S[curr][desc] == 'green' and desc not in visited:
                visited[desc] = True
                node_list.append(desc)
                leaf = False
        if leaf:
            node_list.pop()
            po[curr] = i
            i += 1
    return po

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}

##############

def number_of_descendants(S, root):
    # return mapping between nodes of S and the number of descendants
    # of that node
    num_of_desc = {}
    visited = {root:True}
    node_list = [root]
    while node_list:
        curr = node_list[len(node_list) - 1]
        leaf = True
        for desc in S[curr]:
            if S[curr][desc] == 'green' and desc not in visited:
                visited[desc] = True
                node_list.append(desc)
                leaf = False
        if leaf:
            num_of_desc[curr] = 1
            for desc in S[curr]:
                if S[curr][desc] == 'green' and desc in num_of_desc:
                    num_of_desc[curr] += num_of_desc[desc]
            node_list.pop()
    return num_of_desc

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'}, 
          'b': {'a': 'green', 'd': 'red'}, 
          'c': {'a': 'green', 'd': 'green'}, 
          'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
          'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'} 
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

###############

def lowest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the lowest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    l = {}
    visited = {root:True}
    reacheable = {}
    node_list = [root]
    # compute all reacheable nodes for each node
    while node_list:
        curr = node_list[len(node_list) - 1]
        leaf = True
        for neighbor in S[curr]:
            if neighbor not in visited:
                visited[neighbor] = True
                node_list.append(neighbor)
                leaf = False
        if leaf:
            reacheable[curr] = [curr]
            node_list.pop()
            for w in S[curr]:
                if S[curr][w] == 'red':
                    if w in reacheable:
                        reacheable[curr].extend(reacheable[w])
                        reacheable[curr] = [v for v in set(reacheable[curr])]
                    else:
                        reacheable[curr].append(w)
                elif S[curr][w] == 'green' and w in reacheable:
                    reacheable[curr].extend(reacheable[w])
                    reacheable[curr] = [v for v in set(reacheable[curr])]
    # compute lowest post order
    for v in reacheable:
        min_set = [po[w] for w in reacheable[v]]
        l[v] = min(min_set)
    return l

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}


################

def highest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    l = {}
    visited = {root:True}
    reacheable = {}
    node_list = [root]
    # compute all reacheable nodes for each node
    while node_list:
        curr = node_list[len(node_list) - 1]
        leaf = True
        for neighbor in S[curr]:
            if neighbor not in visited:
                visited[neighbor] = True
                node_list.append(neighbor)
                leaf = False
        if leaf:
            reacheable[curr] = [curr]
            node_list.pop()
            for w in S[curr]:
                if S[curr][w] == 'red':
                    if w in reacheable:
                        reacheable[curr].extend(reacheable[w])
                        reacheable[curr] = [v for v in set(reacheable[curr])]
                    else:
                        reacheable[curr].append(w)
                elif S[curr][w] == 'green' and w in reacheable:
                    reacheable[curr].extend(reacheable[w])
                    reacheable[curr] = [v for v in set(reacheable[curr])]
    # compute lowest post order
    for v in reacheable:
        min_set = [po[w] for w in reacheable[v]]
        l[v] = max(min_set)
    return l

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}
    
#################

def bridge_edges(G, root):
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    S = create_rooted_spanning_tree(G, root)
    po = post_order(S, root)
    nd = number_of_descendants(S, root)
    l = lowest_post_order(S, root, po)
    h = highest_post_order(S, root, po)
    node_list = [root]
    visited = {root:True}
    checked = {}
    be = []
    while node_list:
        curr = node_list[len(node_list) - 1]
        leaf = True
        for neighbor in [nb for nb in S[curr] if nb not in visited]:
            visited[neighbor] = True
            node_list.append(neighbor)
            leaf = False
        if leaf:
            node_list.pop()
            checked[curr] = True
            if h[curr] <= po[curr] and l[curr] > po[curr] - nd[curr]:
                for v in [v for v in S[curr] if S[curr][v] == 'green' and v not in checked]:
                    be.append((v, curr))
    return be


def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    bridges = bridge_edges(G, 'a')
    assert bridges == [('d', 'e')]

test_post_order()
test_number_of_descendants()
test_create_rooted_spanning_tree()
test_lowest_post_order()
test_highest_post_order()
test_bridge_edges()
