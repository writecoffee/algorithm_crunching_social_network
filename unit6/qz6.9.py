#
# Modify long_and_simple_path 
# to build and return the path
# 

# Find me that path!
def long_and_simple_path(G,u,v,l):
    """
    G: Graph
    u: starting node
    v: ending node
    l: minimum length of path
    """
    def long_and_simple_decision(G,u,v,l):
        """
        inner function
        """
        def check_path(G,path):
            # for each edge in current permutation
            for i in range(len(path)-1):
                # if not in edge table, than no path guaranteed
                if path[i+1] not in G[path[i]]: return False
            return True
    
        # return all permutations of a sequence list
        def all_perms(seq):
            if len(seq) == 0: return [[]]
            if len(seq) == 1: return [seq, []]
            most = all_perms(seq[1:])
            first = seq[0]
            rest = []
            for perm in most:
                for i in range(len(perm)+1):
                    rest.append(perm[0:i] + [first] + perm[i:])
            return most + rest
        """
        end of inner function
        """

        if l == 0:
            return False
        n = len(G)
        perms = all_perms(G.keys())
        print perms
        for perm in perms:
            # check path
            if (len(perm) >= l and check_path(G,perm) and perm[0] == u and perm[len(perm)-1] == v):
                return True
        return False

    if not long_and_simple_decision(G,u,v,l):
        return False
    # Otherwise, build and return the path
    for node1 in G:
        for node2 in G[node1].keys():
            G = break_link(G, node1, node2)
            # check if current edge is dispensable
            if not long_and_simple_decision(G, u, v, l):
                G = make_link(G, node1, node2)
    path = [u]
    node = u
    next = (G[node].keys())[0]
    while (next != v):
        path.append(next)
        nextnext0 = (G[next].keys())[0]
        nextnext1 = (G[next].keys())[1]
        if nextnext0 == node:
            (node, next) = (next, nextnext1)
        else:
            (node, next) = (next, nextnext0)
    return path + [v]

#############

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def break_link(G, node1, node2):
    if node1 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G[node1]:
        print "error: breaking non-existent link"
        return
    if node1 not in G[node2]:
        print "error: breaking non-existent link"
        return
    del G[node1][node2]
    del G[node2][node1]
    return G

flights = [(1,2),(1,3),(2,3),(2,6),(2,4),(2,5),(3,6),(4,5)]
G = {}
for (x,y) in flights: make_link(G,x,y)


print long_and_simple_path(G, 1, 5, 4)
