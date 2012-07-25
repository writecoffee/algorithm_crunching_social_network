# calculate the top 20 central actors
# line-format: Leacock, Viv    Are We There Yet?   2005


import csv
import random
import operator

def make_link(G, name, film):
    if name not in G['name']: G['name'][name] = {}
    if film not in G['film']: G['film'][film] = {}
    G['name'][name][film] = True
    G['film'][film][name] = True

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {'name':{}, 'film':{}}
    for (name, film, year) in tsv: make_link(G, name, film)
    return G

# Read the actor/actress-movie graph
AFG = read_graph('imdb-1.tsv')
G = dict(AFG['name'].items() + AFG['film'].items())

def centrality(G, v):
    distance_from_start = {v:0}
    open_list = [v]
    while open_list:
        current = open_list.pop(0)
        for nb in G[current].keys():
            if nb not in distance_from_start:
                distance_from_start[nb] = distance_from_start[current] + 1
                open_list.append(nb)
    return float(sum(distance_from_start.values())) / len(distance_from_start)

def get_top_20():
    cens = []
    for actor in AFG['name'].keys():
        cens.append((actor, centrality(G, actor)))
    result = top(cens, 20)
    return sorted(result, key=operator.itemgetter(1))

def top(cens, k):
    (v, vc) = operator.itemgetter(random.randrange(len(cens)))(cens)
    (smaller, middle, bigger) = partition(cens, (v, vc))
    if len(smaller) == k: return smaller
    if len(smaller) > k: return top(smaller, k)
    if len(smaller) < k: return smaller + top(middle + bigger, k - len(smaller))

def partition(L, (v, vc)):
    smaller = []
    bigger = []
    middle = []
    for (actor, cen) in L:
        if cen < vc: smaller.append((actor, cen))
        elif cen > vc: bigger.append((actor, cen))
        else: middle.append((actor, cen))
    return (smaller, middle, bigger)

def test():
    result = get_top_20()
    for i in range(20):
        print result[i]

test()
