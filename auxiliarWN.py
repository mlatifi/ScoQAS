#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        auxiliarWN.py
#
# Author:      Horacio
#
# Created:     2008/07/29
# management English WN
#-----------------------------------------------------------------------------


import nltk
from nltk.corpus.reader.wordnet import *
from string import *
from copy import deepcopy
import sys



SYNSETTHRESHOLD=5

ptb2WNmaps = {
    'JJR':ADJ,
    'JJS':ADJ,
    'JJ':ADJ,
    'NNS':NOUN,
    'NNPS':NOUN,
    'NN':NOUN,
    'NNP':NOUN,
    'RBR':ADV,
    'RBS':ADV,
    'RB':ADV,
    'VBP':VERB,
    'VBN':VERB,
    'VBG':VERB,
    'VBD':VERB,
    'VBZ':VERB,
    'VB':VERB
    }

def normalizeName(name):
    namestr=str(name)
    if not(namestr.isdigit()):
        return list(set([name.lower().replace(' ','_'), name.replace(' ','_')]))

def pos2WN(pos):
    global ptb2WNmaps
    if pos in ptb2WNmaps:
        return ptb2WNmaps[pos]
    else:
        return None

def iniWN():
    global wn,S,L
    print 'loading wordnet'
    wn = WordNetCorpusReader(nltk.data.find('corpora/wordnet'))
    print 'done loading'
    S = wn.synset
    L = wn.lemma


def getallLemmas(w,pos=None):
    "returns the list of lemmas of a word, pos) or [] if not occurring in WN)"
    ws=normalizeName(w)
    ls = []
    for w in ws:
        ls += wn.lemmas(w,pos)
    return ls

def getallVariants(w,pos=None):
    global variants
    "returns the list of variants of all the variants of a word, pos) or [] if not occurring in WN)"
    ls = getallLemmas(w,pos=None)
    variants={}
    #variants = deepcopy(ls)
    #print "variants:",variants
    i=1
    for l in ls:
        lsyn = l.synset
        lname=l.name
        lst1=wn.synsets(w)
        print "Synset is :", lsyn
        print "Name is :", lname
        print "Wordnet direct is :", lst1
        variants[i]= lsyn
        i+=1

    return variants.items()

def getallSynsets(w,pos=None):
    "returns the list of Synsets of a word, pos) or [] if not occurring in WN)"
    ws=normalizeName(w)
    ls = []
    for w in ws:
        ls += map(lambda x:x.synset,wn.lemmas(w,pos))
    return ls


def getSynsets(w,pos=None):
    "returns the list of Synsets of a word, pos) or [] if not occurring in WN)"
    ws=normalizeName(w)
    ls = []
    for w in ws:
        ls += wn.synsets(w,pos)
        #ls += map(lambda x:x.synset,wn.lemmas(w,pos))
    return ls

def getAllNameVariants(w,pos=None):
    vs = getallVariants(w,pos)
    names = set([])
    i=0
    for lst in vs:
        i+=1
        print "list:", lst.__getitem__(i)
        #names.add(l.name)
        #names.add(l.synset.split('.')[0])

    return list(names)

def lemmalist(str):
    syn_set = []
    i=0
    for synset in wn.synsets(str):
        for item1 in synset.lemma_names():
            syn_set.append(item1)
            ln=len(syn_set[i])
            syn_set[i]=syn_set[i][0:ln]
            i+=1

    return syn_set

def entityList(str):
    syn_set = []
    ls_synset=getSynsets(str,pos='n')
    i=0
    for synset in ls_synset:
        # for item1 in synset.lemma_names():
        ls = map(lambda x:x[0].lemma_names(),getHypernymsPruned(synset,10))
        syn_set.append(synset)
        syn_set[i]=ls
        # ln=len(syn_set[i])
        # syn_set[i]=syn_set[i][0:ln]
        i+=1

    return syn_set

def getHypernymsPruned(s,height=1):
    "returns a list of pairs <synset, distance> of hyperonyms at a maximum distance of height"
    hps = s.hypernym_paths()
    if height == 'all':
        height = 1e300
    rta = {}
    for i in hps:
        for ij in range(min(height,len(i))):
            j = i[ij]
            if j not in rta:
                rta[j]=ij+1
    if len(rta)==0:
        return None
    return map(lambda x:(x,rta[x]),rta.keys())

def get_gloss(offset, pos):
    "returns the gloss of a synset"
    return getSynset(pos,offset).gloss

def computing_similarities(synsets,measure='leacock_chodorow'):
    "from a list of synsets computes a list of tuples <similarity,synset1,synset2>"
    rta=[]
    for i in synsets:
        for j in synsets:
            if i != j:
                if (i.pos == 'noun' or i.pos == 'verb') and (j.pos == 'noun' or j.pos == 'verb'):
                    try:
                        if measure == 'path_distance':
                            sim= i.getSenses()[0].path_distance_similarity(j.getSenses()[0])
                        elif measure == 'leacock_chodorow':
                            sim= i.getSenses()[0].leacock_chodorow_similarity(j.getSenses()[0])
                        elif measure == 'wu_palmer':
                            sim= i.getSenses()[0].wu_palmer_similarity(j.getSenses()[0])
                        if sim > -1:
                            if not (sim,i,j) in rta:
                                rta.append((sim,i,j))
                    except TypeError:
                        continue
    rta.sort()
    return rta

def are_related_synsets(s1,s2,form='simple'):
    "get from s1, s2 form = simple: the list of relations holding, form = extended: the list of scores"
    related=[]
    if form == 'simple':
        for i in s1.getPointers():
            if i.type not in ['frames','verb group']:
                try:
                    if i.getTarget() == s2:
                        if not i.type in related:
                            related.append(i.type)
##                    elif i.getSource() == s2:
##                        if not i.type+'-1' in related:
##                            related.append(i.type+'-1')
                except IndexError:
                    continue
                except ValueError:
                    continue
        return related
    else:
        return computing_similarities([s1,s2])


def are_related_words(w1,w2,form='simple'):
    "get from w1, w2 form = simple: the list of relations holding, form = extended: the list of scores"
    s1s=get_synsets_of_word(lower(w1))[0:SYNSETTHRESHOLD]
    s2s=get_synsets_of_word(lower(w2))[0:SYNSETTHRESHOLD]
    related=[]
    for s1 in s1s:
        print s1
        for s2 in s2s:
            print s2
            for r in are_related_synsets(s1,s2,form):
                if not r in related:
                    related.append(r)
    return related


def get_related_synsets(ss1,ss2,form='simple'):
    "get from ss1, ss2 form = simple: the list of relations holding, form = extended: the list of scores"
    related=[]
    for s1 in ss1:
        for s2 in ss2:
            for r in are_related_synsets(s1,s2,form):
                if not r in related:
                    related.append(r)
    return related


def get_related_words(sw1,sw2,form='simple'):
    "get from sw1, sw2 form = simple: the list of relations holding, form = extended: the list of scores"
    related=[]
    for w1 in sw1:
        print w1
        for w2 in sw2:
            print '\t'+w2
            s1s=get_synsets_of_word(lower(w1))
            s2s=get_synsets_of_word(lower(w2))
            for s1 in s1s:
                for s2 in s2s:
                    for r in are_related_synsets(s1,s2,form):
                        if not r in related:
                            related.append((w1,w2,r))
    return related


def complement(u, v):
    """Return the complement of _u_ and _v_ respect intersection.

    >>> complement((1,2,3), (2,3,4))
    ([1],[4])
    """
    i=intersection(u,v)
    u1=[]
    v1=[]
    for e in u:
        if e not in i:
            u1.append(e)
    for e in v:
        if e not in i:
            v1.append(e)
    return (u1,v1)

def getOffsetDict(pos):
    """
    builds a dict with domain = offsets and codomain = synsets filtered by
    pos = n, a, v, r, s, all
    """
    global wn
    ss = list(wn.all_synsets())
    print len(ss), 'synsets in wn'
    if pos == 'all':
        ssf = ss
    else:
        ssf = filter(lambda x:x.pos == pos,ss)
    print len(ssf), 'synsets with pos', pos
    offsetD = {}
    for i in ssf:
        offsetD[i.offset] = i
    print 'built offsetD with ', len(offsetD), 'entries'
    return offsetD


def getAllVariantsOfOffset(offset,pos,offsetD):
    """
    gets all the variants of offset with pos occurring in offsetD
    """
    if offset not in offsetD:
        return []
    ss = offsetD[offset]
    if ss.pos != pos:
        return []
    return ss.lemma_names

##
##
##V['learn'][0].getPointers()boundedVars
##V['teach'][0].getPointers()
##POINTER_TYPES
##('antonym', 'hypernym', 'hyponym', 'attribute', 'also see', 'entailment',
## 'cause', 'verb group', 'member meronym', 'substance meronym', 'part meronym',
## 'member holonym', 'substance holonym', 'part holonym', 'similar',
## 'participle of', 'pertainym', 'frames', 'domain category', 'domain usage',
## 'domain regional', 'class category', 'class usage', 'class regional',
## 'hypernym (instance)', 'hyponym (instance)')
##N['poodle'][0].leacock_chodorow_similarity(N['bulldog'][0])
##V['learn'][0].getPointerTargets()
##_lcs_by_depth(V['learn'][0].synset,V['learn'][0].synset)
##V['carry out']
##for i in V['learn']:
##	print i.synset

##>>> source=N['spanish'][0]
##>>> source.getPointerTargets(CLASSIF_REGIONAL)
##[{noun: Spain, Kingdom of Spain, Espana}]


##for i in V['learn']:
##	print i.getPointers()
##V['learn'][0].synset.offset
##V['learn'].getSenses()
##for i in V['learn'].getSenses():
##	print i.synset.offset
##N['dog'].taggedSenseCount
##V.has_key('aaa')
##getSynset('noun',6215070)
##c=getSynset('noun',6215070)
##c.offset
##c.pos
##c.getPointers()[0]
##d=c.getPointers()[0]
##d.getSource()
##d.getTarget()
##d.type
##path_distance
##leacock_chodorow
##wu_palmer


## in module wntools
"""
Utility functions to use with the wordnet module.

    >>> dog = N['dog'][0]

(First 10) adjectives that are transitively SIMILAR to the main sense of 'red'

    >>> closure(ADJ['red'][0], SIMILAR)[:10]
    ['red' in {adj: red, reddish, ruddy, blood-red, carmine, cerise, cherry, cherry-red, crimson, ruby, ruby-red, scarlet}, {adj: chromatic}, {adj: amber, brownish-yellow, yellow-brown}, {adj: amber-green}, {adj: amethyst}, {adj: auburn}, {adj: aureate, gilded, gilt, gold, golden}, {adj: avocado}, {adj: azure, cerulean, sky-blue, bright blue}, {adj: beige}]

Adjectives that are transitively SIMILAR to any of the senses of 'red'

    >>> #flatten1(map(lambda sense:closure(sense, SIMILAR), ADJ['red']))    # too verbose

Hyponyms of the main sense of 'dog'(n.) that are homophonous with verbs

    >>> filter(lambda sense:V.get(sense.form), flatten1(map(lambda e:e.getSenses(), hyponyms(N['dog'][0]))))
    ['dog' in {noun: dog, domestic dog, Canis familiaris}, 'pooch' in {noun: pooch, doggie, doggy, barker, bow-wow}, 'toy' in {noun: toy dog, toy}, 'hound' in {noun: hound, hound dog}, 'basset' in {noun: basset, basset hound}, 'cocker' in {noun: cocker spaniel, English cocker spaniel, cocker}, 'bulldog' in {noun: bulldog, English bulldog}]

Find the senses of 'raise'(v.) and 'lower'(v.) that are antonyms

    >>> filter(lambda p:p[0] in p[1].getPointerTargets(ANTONYM), product(V['raise'].getSenses(), V['lower'].getSenses()))
    [('raise' in {verb: raise, lift, elevate, get up, bring up}, 'lower' in {verb: lower, take down, let down, get down, bring down})]
"""
"""
POINTER_TYPES = (
    ANTONYM,
    HYPERNYM,
    HYPONYM,
    ATTRIBUTE,
    ALSO_SEE,
    ENTAILMENT,
    CAUSE,
    VERB_GROUP,
    MEMBER_MERONYM,
    SUBSTANCE_MERONYM,
    PART_MERONYM,
    MEMBER_HOLONYM,
    SUBSTANCE_HOLONYM,
    PART_HOLONYM,
    SIMILAR,
    PARTICIPLE_OF,
    PERTAINYM,
    # New in wn 2.0:
    FRAMES,
    CLASSIF_CATEGORY,
    CLASSIF_USAGE,
    CLASSIF_REGIONAL,
    CLASS_CATEGORY,
    CLASS_USAGE,
    CLASS_REGIONAL,
    # New in wn 2.1:
    INSTANCE_HYPERNYM,
    INSTANCE_HYPONYM,
    )
"""

def get_opinion_verbs():
    verbs=['affirm','believe','corroborate','declare','describe','feel','say','suggest','tell','think']
    forms=[]
    for w in verbs:
        try:
            for f in getallVariants(w,pos='verb'):
                if f not in forms:
                    forms.append(f)
        except ValueError:
            pass
    return forms

def get_negation_verbs():
    verbs=['reject','deny','refuse','oppose']
    forms=[]
    for w in verbs:
        try:
            for f in getallVariants(w,pos='verb'):
                if f not in forms:
                    forms.append(f)
        except ValueError:
            pass
    return forms

def get_opinion_nouns():
    nouns=['affirmation','believe','corroboration','declaration','description','feeling','opinion','suggestion','thinking']
    forms=[]
    for w in nouns:
        try:
            for f in getallVariants(w,pos='noun'):
                if f not in forms:
                    forms.append(f)
        except ValueError:
            pass
    return forms

def get_negation_nouns():
    nouns=['rejection','denial','refusal','opposition','negation']
    forms=[]
    for w in nouns:
        try:
            for f in getallVariants(w,pos='noun'):
                if f not in forms:
                    forms.append(f)
        except ValueError:
            pass
    return forms
