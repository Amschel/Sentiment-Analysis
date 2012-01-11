#!/usr/bin/python

import collections
import data
from numpy import *

from scipy.sparse import lil_matrix, csr_matrix
def words(s):
    words = []
    current = ""
    not_mode = False
    not_words = set(["not", "isn't", "doesn't"])
    for i in s:
        if i.isalnum():
            current += i
        elif i.isspace():
            if not current:
                continue
            if not_mode:
                current += "_NOT"
            words.append(current)
            if current in not_words:
                not_mode = True
            current = ""
        else:
            words.append(i)
            not_mode = False
            if not current:
                continue
            if not_mode:
                current += "_NOT"
            words.append(current)
            current = ""
    if current:
        words.append(current)
    return words
            
def ngrams(n, s):
    lwr = s.lower()
    ws = words(lwr)
    current = collections.deque(ws[:n])
    grams = data.DefDict(1)
    for pos in range(n, len(ws)):
        grams[" ".join(current)] += 1
        current.popleft()
        current.append(ws[pos])
    grams[" ".join(current)] += 1
    return grams

def ngrams_range(b, e, s):
    g = {}
    for i in range(b, e+1):
        g.update(ngrams(i, s))
    return g

def ngrams_to_dictionary(grams):
    keysets = [set(k) for k in grams]
    allgramset = set()
    allgramset = apply(allgramset.union, keysets)
    return allgramset
    




def ngrams_to_matrix(grams, classes):
    print "Entering ngrams_to_matrix"
    keysets = [set(k) for k in grams]
    allgramset = set()
    print "b"
    allgramset = apply(allgramset.union, keysets)
    print "c"
    allgrams = list(allgramset)
    print "> Listed"
    vecs = []
    print "> []"
    allgramsdict = {}
    for i in range(len(allgrams)):
        allgramsdict[allgrams[i]] = i
    for g, c in zip(grams, classes):
        vec = ones(len(allgramsdict) + 1, dtype=uint16)
        for i in g:
            vec[allgramsdict[i]] = g[i]
        vec[-1] = c
        vecs.append(vec)
    print vstack(vecs).T.shape
    return data.Data(vstack(vecs).T)

def ngrams_to_sparse(grams, classes):
    print "a"
    keysets = [set(k) for k in grams]
    allgramset = set()
    print "b"
    allgramset = apply(allgramset.union, keysets)
    print "c"
    allgrams = list(allgramset)
    print "d"
    vecs = []
    print "e"
    allgramsdict = {}
    for i in range(len(allgrams)):
        allgramsdict[allgrams[i]] = i
    print "f"
    mat = lil_matrix((len(allgrams), len(grams)))
    print "g"
    for g in range(len(grams)):
        for i in range(len(grams[g])):
            if grams[g][i] > 1:
                mat[allgramsdict[grams[g][i]], g] = grams[g][allgrams[i]] - 1
        mat[g, -1] = classes[g]
    return data.Data(mat.tocsr())
        
    

def gen_indexdict(dictionary):
    allgramsdict = {}
    for i in range(len(dictionary)):
        allgramsdict[dictionary[i]] = i
    return allgramsdict
    
def ngram_vector(n, s, dictionary, allgramsdict = {}):
    grams = ngrams(n, s)
    if len(allgramsdict) == 0:
        allgramsdict = gen_indexdict(dictionary)
    vec = ones(len(dictionary), dtype=uint16)
    for g in grams:
        if g in allgramsdict:
            vec[allgramsdict[g]] = grams[g]
    return array(vec)
        
if __name__ == "__main__":
    print "Trigram example: %s" % ngrams(3, "Now is the time for all good men to not come to the aid of their party! Now is the time for all bad women to leave the aid of their country? This, being war, is bad")
    g1 = ngrams(1, "Hello how are you")
    g2 = ngrams(1, "Are you feeling well")
    g3 = ngrams(1, "Well hello there")


    print "Unigram example: %s" % g3
    print "Matrix example: %s" % ngrams_to_matrix([g1, g2, g3], [1, 2, 1]).asMatrix()

