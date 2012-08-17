#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

#from marvel import marvel, characters

import cPickle

marvel = cPickle.load(open("smallG.pkl"))
characters = cPickle.load(open("smallChr.pkl"))

def create_weighted_graph(bipartiteG, characters):
    comic_size = len(set(bipartiteG.keys()) - set(characters))
    # your code here
    AB = {}
    for ch1 in characters:
        if ch1 not in AB:
            AB[ch1] = {}
        for book in bipartiteG[ch1]:
            for ch2 in bipartiteG[book]:
                if ch1 != ch2:
                    if ch2 not in AB[ch1]:
                        AB[ch1][ch2] = 1
                    else:
                        AB[ch1][ch2] += 1
    contains = {}
    for ch1 in characters:
        if ch1 not in contains:
            contains[ch1] = {}
        contains[ch1] = len(bipartiteG[ch1].keys())
    G = {}
    for ch1 in characters:
        if ch1 not in G:
            G[ch1] = {}
        for book in bipartiteG[ch1]:
            for ch2 in bipartiteG[book]:
                if ch2 != ch1:
                    G[ch1][ch2] = (0.0 + AB[ch1][ch2]) / (contains[ch1] + contains[ch2] - AB[ch1][ch2])
    return G

######
#
# Test

def test():
    bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                  'charB':{'comicB':1, 'comicD':1},
                  'charC':{'comicD':1},
                  'comicB':{'charA':1, 'charB':1},
                  'comicC':{'charA':1},
                  'comicD': {'charC':1, 'charB':1}}
    G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
    # three comics contain charA or charB
    # charA and charB are together in one of them
    assert G['charA']['charB'] == 1.0 / 3
    assert G['charA'].get('charA') == None
    assert G['charA'].get('charC') == None

def test2():
    G = create_weighted_graph(marvel, characters)
    
test()
test2()
