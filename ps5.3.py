#!/usr/bin/env python
# -*- coding: utf8 -*- 
#
# Another way of thinking of a path in the Kevin Bacon game 
# is not about finding *short* paths, but by finding paths 
# that don’t use obscure movies.  We will give you a 
# list of movies along with their obscureness score.  
#
# For this assignment, we'll approximate obscurity 
# based on the multiplicative inverse of the amount of 
# money the movie made.  Though, its not really important where
# the obscurity score came from.
#
# Use the the imdb-1.tsv and imdb-weights.tsv files to find
# the obscurity of the “least obscure” 
# path from a given actor to another.  
# The obscurity of a path is the maximum obscurity of 
# any of the movies used along the path.
#
# You will have to do the processing in your local environment
# and then copy in your answer.
#
# Hint: A variation of Dijkstra can be used to solve this problem.
#

import csv
import heapq

# Change the `None` values in this dictionary to be the obscurity score
# of the least obscure path between the two actors
answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

# Here are some test cases.
# For example, the obscurity score of the least obscure path
# between 'Ali, Tony' and 'Allen, Woody' is 0.5657
test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
        (u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}

def make_link(G, name, book):
    if name not in G:
        G[name] = {}
    G[name][book] = 1
    if book not in G:
        G[book] = {}
    G[book][name] = 1
    return G

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    characters = {}
    for line in tsv:
        name, film = line[0], line[1]
#        name, film = name.encode('utf-8'), film.encode('utf-8')
        make_link(G, name, film)
        if name not in characters:
            characters[name] = True
    return G, characters

def read_obs_score(filename):
    tsv = csv.reader(open(filename), delimiter='\t')
    obscurities = {}
    for line in tsv:
        film, year, obs = line[0], line[1], line[2]
#        film, year, obs = film.encode('utf-8'), year.encode('utf-8'), obs.encode('utf-8')
        obscurities[film] = obs
    return obscurities

def HG_make_link(HG, ch1, ch2, obs):
    if ch1 not in HG:
        HG[ch1] = {}
    if ch2 not in HG:
        HG[ch2] = {}
    if ch2 not in HG[ch1]:
        HG[ch1][ch2] = obs
    if ch1 not in HG[ch2]:
        HG[ch2][ch1] = obs

def make_hop_graph(G, characters, obscurities):
    HG = {}
    for ch1 in characters:
        for book in G[ch1]:
            for ch2 in G[book]:
                if ch1 > ch2:
                    HG_make_link(HG, ch1, ch2, obscurities[book])
    return HG

def dijkstra(HG, v):
    dist_so_far = {v: 0}
    final_dist = {}
    heap = [(0, v)]
    while dist_so_far:
        (w, k) = heapq.heappop(heap)
        if k in final_dist or (k in dist_so_far and w > dist_so_far[k]):
            continue
        else:
            del dist_so_far[k]
            final_dist[k] = w
        for neighbor in [nb for nb in HG[k] if nb not in final_dist]:
            nw = max(final_dist[k], HG[k][neighbor])
            if neighbor not in dist_so_far or nw < dist_so_far[neighbor]:
                dist_so_far[neighbor] = nw
                heapq.heappush(heap, (nw, neighbor))
    return final_dist

def test():
    G, characters = read_graph('imdb-1.tsv')
    obscurities = read_obs_score('imdb-weights.tsv')
    HG = make_hop_graph(G, characters, obscurities)
    for t in answer:
        ch1, ch2 = t[0], t[1]
        routes = dijkstra(HG, ch1)
        answer[t] = routes[ch2]
        print '(', t[0], ', ', t[1], '):', answer[t]

test()
