# -*- coding: utf-8 -*-
#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        representingSentences.py
#
# Author:      Horacio
#
# Created:     2014/04/28
# representing sentences
#-----------------------------------------------------------------------------

##user = 'horacioCluster'
##user = 'horacioWindowsLSI'
user = 'majid'

import re
import string
import sys
import pickle
import nltk
##import numpy
##import pylab


#from nltk import *
from types import StringType, ListType
from nltk import stem
from nltk import tokenize
from nltk import tree
from os import listdir,system, fsync, remove
from os.path import split, splitext, abspath, exists, isfile
from math import *
import uuid
from copy import deepcopy
from nltk.corpus import wordnet as wn
##from nltk.app import wordfreq
##from matplotlib.pylab import da

if user == 'horacioCluster':
    sys.path.append('/home/usuaris/horacio/material/programs')
    workingDir = '/home/usuaris/horacio/tackbp/process2012/data/'
    workingDirAlicia = '/home/usuaris/chil/alicia/logs-kbp2012-Jul2013/'
    workingDirJordi = '/home/usuaris/turmo/kbp2013/docs/preprocessed-docs-from-queries/'
elif user == 'horacioWindowsLSI':
    sys.path.append('L:/NQ/intercambio/material/programs')
    workingDir = 'L:/NQ/intercambio/know2/tackbp/process2012/data/'
    workingDirJordi = 'L:/NQ/intercambio/know2/tackbp/process2012/data/preprocessed-docs-from-queries/'
elif user == 'majid':
    pythonPath='C:\Python27\lib\site-packages\graphviz'
    workingDir = 'D:\PhD\PhD Tesis\Project'
    workingDirMajid = 'D:/PhD/PhD Tesis/Project/RepresentingSentences/data/'
    sys.path.append(workingDir+'..\..\material')
    sys.path.append(workingDir+'\RepresentingSentences\data')
    sys.path.append(pythonPath)



try:
    from basic import *
except:
    pass
try:
    from auxiliar import *
except:
    pass

from rule import *

try:
    from auxiliarWP import *
except:
    pass

from auxiliarWN import *

from managingOntology import *

try:
    from auxiliarAcrophile import *
except:
    pass
##from pylab import *

#try:
#    import pylab
#except ImportError:
#    import warnings
#    warnings.warn("nltk.app.wordfreq not loaded "
#                     "(requires the pylab library).")
#else:
#    from wordfreq_app import app as wordfreq

#from marianoFeliceDistances import *
# try:
  #  from compatible import *
#except:
 #   pass

## global



## classes

class NGRAMS:
    def __init__(self):
        self._init_vars()

    def _init_vars(self):
        self._content={}
        self._size=0

class PAIR():

    def __init__(self,s1,s2):
        self.s1=s1
        self.s2=s2

    def getDistance(self,d):
        s1 = self.s1
        s2 = self.s2
        try:
            return eval('dist_'+str(d)+'(s1,s2)')
        except:
            return None

class CONSTRAINT():

    def __init__(self,p,args,vars):
        self._predicate = p
        self._arguments = args
        self._vars = vars
        self.var_token=VAR_TOKEN(args,vars)

    def describe(self):
        print 'Predicate::', self._predicate, 'With Arguments:', self._arguments, 'involving Variables:', self._vars

class VAR_TOKEN():

    def __init__(self,arg,var):
        self._argument = arg
        self._var = var

    def getVar_TK(self,idx):
        return self._var[idx]

    def getArgument_TK(self,idx):
        return self._argument[idx]

class CONSTRAINTS():

    def __init__(self):
        self._lastVariable = 0
        self._vars = []
        self._constraints = []


    def addNewVariable(self,arg):
        self._lastVariable +=1
        nV = 'X'+str(self._lastVariable)
        var_token=VAR_TOKEN(arg,nV)
        self._vars.append(var_token)
        return nV

    def addNewConstraint(self,p,args,vars):
        nC = CONSTRAINT(p,args,vars)
        self._constraints.append(nC)

    def describe(self):
        print 'Vars:'
        for var in self._vars:
            print '\t', var._var
        print 'Constraints for :'
        for c in self._constraints:
            print '\t', c._predicate+'('+ str(map(str,c._arguments)) +')', 'involving variables', c._vars



    def getVars(self):
        return self._vars

    def getConstraints(self):
        return self._constraints

class MYSENT(SENT):

    def setConstraints(self):
        self._constraints = CONSTRAINTS()

    def appendSent(self,sent):
        "appends a sent"
        for i in sent._get_tokens():
            self._put_token(i)

    def putSint(self,sint):
        self.sint = sint

    def getSint(self):
        return self.sint
            
    def getTokenWithPos(self,pos):
        "returns the list of tokens of sent having pos"
        rta=[]
        for i in range(0,len(self._get_tokens())):
            if self._get_tokens()[i].isPos(pos):
                rta.append(i)
        return rta

    def getTokenWithLemma(self,lemma):
        "returns the list of tokens of sent having lemma"
        rta=[]
        for i in range(0,len(self._get_tokens())):
            if self._get_tokens()[i]._lemma() == lemma:
                rta.append(i)
        return rta

    def getTokenInLemma(self,lemma):
        "returns the list of tokens of sent having lemma"
        rta=[]
        for i in range(0,len(self._get_tokens())):
            if lemma in self._get_tokens()[i]._lemma():
                rta.append(i)
        return rta

    def getTokenWithWordForm(self,word):
        "returns the list of tokens of sent having word"
        rta=[]
        for i in range(0,len(self._get_tokens())):
            if self._get_tokens()[i]._word() == word:
                rta.append(i)
        return rta

    def getTokenWithX(self):
        "returns the list of tokens of sent having XXXXXX"
        return self.getTokenInLemma('xxxxxx')

    def getTokenWithY(self):
        "returns the list of tokens of sent having YYYYYY"
        return self.getTokenInLemma('yyyyyy')

    def getTokenWithZ(self):
        "returns the list of tokens of sent having ZZZZZZ"
        return self.getTokenInLemma('zzzzzz')

    def insertToken(self,position,token):
        self._content.insert(position,token)

    def insertX(self,position):
        self.insertToken(position,MYTOKEN(['XXXXXXX','xxxxxxx','NP00P00',[],'nil','nil']))

    def getWordsInPositions(self,positions):
        if len(positions) == 0:
            return ''
        else:
            rta = self._content[positions[0]]._word()
            for i in positions[1:]:
                rta+=' '+self._content[i]._word()
            return rta
        

class MYTOKEN(TOKEN):
    def isPos(token,pos):
        "has token this pos?"
        if pos in cpatrPos:
            return cpatrPos[pos].match(token._pos())
        else:
            return token.get_pos() == pos
        
    def newWord(self,word):
        self._content[0] = word

    def newLemma(self,lemma):
        self._content[1] = lemma

    def newPos(self,pos):
        self._content[2] = pos

    def newNE(self,ne):
        self._content[3] = ne

    def newNE2(self,ne2):
        self._content[4] = ne2

    def newSynsets(self,synsets):
        self._content[5] = synsets

    def newOffset(self,offset):
        try:
            self._content[6] = offset
        except:
            self._content.append(offset)

    def newLabel(self,label):
        try:
            self._content[7] = label
        except:
            self._content.append(label)

    def _setLabel(self):
        if self._pos() == 'CD' or self._pos() == 'NNP_CD' :
            return '<DATE>'
        elif self._pos() == 'NNP_NNP':
            return '<PERSON>'
        elif self._pos() == 'NNP' and self._ne() != '0':
            return  '<'+self._ne()+'>'
        elif self._ne() != '0':
            return  '<'+self._ne()+'>'
        elif self._word()[0].isupper():
            return  '<ENTITY>'
        else:
            return  self._word()
            
    def _offset(self):
        return self._content[6]

    def _label(self):
        return self._content[7]

## auxiliar functions

def treeWidth(t):
    c = 0
    for st in t.subtrees():
        if len(st) == 0:
            c+=1
    return c
           
def savingSent(ss,outF):
    outF = open(outF,'w')
    outF.write('multifile sent/3.\n')
    outF.write('dynamic sent/3.\n')
    for s in ss:
        outF.write(ss[s].sent2Prolog())
    outF.close()
    
def savingSint(ss,outF):
    outF = open(outF,'w')
    outF.write('multifile sint/3.\n')
    outF.write('dynamic sint/3.\n')
    for s in ss:
        outF.write(ss[s].sint2Prolog())
    outF.close()

def exportNE(outF):
    global pairs
    outF = open(outF,'w')
    for p in pairs:
        nes = filter(
            lambda x: x._ne() not in ['nil','','0'],
            p.s1._get_tokens()+p.s2._get_tokens())
        for ne in nes:
            outF.write(_encode(ne._word())+'\n')
    outF.close()

def setTypeOfProcess(tOP):
    global typeOfProcess
    if tOP == 'freeling+dep':
        typeOfProcess ={
            'name':tOP,
            'positions':{'w':0,'off':1,'l':3,'p':4,'ss':5,'ne':8,'nx':9,'tx':10}
            }
    elif tOP == 'stanford':
        typeOfProcess ={
            'name':tOP,
            'positions':{'w':1,'tkId':0,'l':2,'p':3,'ne':4,'nx':6,'tx':7}
            }
    else:
        print 'invalid tOP'

def loadPreProcessedFile(inF):
    global typeOfProcess, lines
    lines = filter(
        lambda x:x != [''],
        map(lambda x:x.replace('\n','').split('\t'),open(inF).readlines()))
    print len(lines), 'lines read'
    if lines[0][0].startswith('\xef\xbb\xbf'):
        lines[0][0]=lines[0][0][3:]
    
def getSentenceSegmentation():
    global typeOfProcess, lines, sentenceSegmentation
    print 'performing sentence segmentation',
    sentenceSegmentation=[]
    if typeOfProcess['name'] == 'stanford':
        iniSent = 0
        tkIdPrevious = int(lines[0][typeOfProcess['positions']['tkId']])
        for i in range(1,len(lines)):
            tkId = int(lines[i][typeOfProcess['positions']['tkId']])
            if tkId < tkIdPrevious:
                sentenceSegmentation.append((iniSent,i-1))
                iniSent = i
            tkIdPrevious = tkId
        sentenceSegmentation.append((iniSent,i))
    print 'resulting on',len(sentenceSegmentation),'sentences'

def reSegmentNE():
    global typeOfProcess, lines, sentenceSegmentation
    print 'performing resegmentation of NE',
    c=0
    print 'resulting on', c, 'resegmentations'

def representSentences():
    global typeOfProcess, lines, sentenceSegmentation, sentences
    sentences={}
    print 'representing sentences', len(sentenceSegmentation)    
    for s in range(len(sentenceSegmentation)):
        representSentence(s)
    
def representSentence(s):
    global typeOfProcess, lines, sentenceSegmentation, sentences
    print 'representing sentence',s, 'from', sentenceSegmentation[s][0], 'to', sentenceSegmentation[s][1]
    sentences[s] = MYSENT(s,s)
    for tk in range(sentenceSegmentation[s][0], sentenceSegmentation[s][1]+1):
        sentences[s]._put_token(MYTOKEN(representToken(tk)))
    sentences[s].putSint(SINT())
    mappingsSentence(s)
    buildSintDep(s)
    buildSintConst(s)
    buildSintArtificialChunks(s)
    

def representDependency(iLine):
    global typeOfProcess, lines, sentenceSegmentation, sentences
    line = lines[iLine]
    tkId = line[typeOfProcess['positions']['tkId']]
    nx = line[typeOfProcess['positions']['nx']]
    tx = line[typeOfProcess['positions']['tx']]
    return [tkId, nx, tx]

def representToken(iLine):
    global typeOfProcess, lines, sentenceSegmentation, sentences
    line = lines[iLine]
    w = line[typeOfProcess['positions']['w']]
    l = line[typeOfProcess['positions']['l']]
    p = line[typeOfProcess['positions']['p']]
    try:
        ss = line[typeOfProcess['positions']['ss']]
    except:
        ss = []
    ne = line[typeOfProcess['positions']['ne']]
    if ne == 'O':
        ne = ''
    else:
        ne = ne[:3]
    ne2 = ''
    return [w,l,p,ne,ne2,ss]

def mappingsSentence(s):
    global sentences, inverseMappings, sentenceSegmentation
    global typeOfProcess, lines
    inverseMappings = {}
    for iLine in range(sentenceSegmentation[s][0], sentenceSegmentation[s][1]+1):
        line = lines[iLine]
        tkId = line[typeOfProcess['positions']['tkId']]
        inverseMappings[tkId] = iLine
    inverseMappings['0'] = -1



def buildSintDep(s):
    global sentences, inverseMappings, sentenceSegmentation, sint
    s1 = sentences[s]
    sint = s1.getSint()
    deps = []
    deps12 = set([])
    for iLine in range(sentenceSegmentation[s][0], sentenceSegmentation[s][1]+1):
        tkId, nx, tx = representDependency(iLine)
        ind = iLine - sentenceSegmentation[s][0]
        if nx == '':
            continue
        if int(nx) >= sentences[s]._size:
            continue
        f = inverseMappings[nx] - sentenceSegmentation[s][0]
        if (f,ind) in deps12 or (ind,f) in deps12:
            continue
        deps12.add((f,ind))
        if (f, ind, tx) not in deps:
            deps.append((f, ind, tx))
    sint._dependencies = deps


def buildSintConst(s):
    global sentences, forest
    s1 = sentences[s]
    sint = s1.getSint()
    if not sint._dependencies or sint._dependencies == []:
        return None
    fromS = set(map(lambda x:x[0], sint._dependencies))
    toS = set(map(lambda x:x[1], sint._dependencies))
    forest = dict(map(lambda x:(x,tree.ParentedTree(str(x),[])), toS.difference(fromS)))
    fromS = dict(map(lambda x: (x,[]),fromS))
    for i in sint._dependencies:
        if i[0] in fromS:
            fromS[i[0]].append(i[1])
    ok = True
    while (len(forest) > 1) and ok:
        ok = False
        for i in fromS:
            ok = True
            for j in fromS[i]:
                if j not in forest:
                    ok = False
                    break
            if ok:
                break
        if ok:
            children = map(lambda x:forest[x],fromS[i])
            for j in fromS[i]:
                del forest[j]
            forest[i] = tree.ParentedTree(str(i),children)
            del fromS[i]
    if len(forest) == 0:
        return None
    else:
        sint._constituents = forest[forest.keys()[0]]

def buildSintArtificialChunks(s):
    global sentences, forest
    s1 = sentences[s]
    sint = s1.getSint()
    for i in range(s1._size):
        tk = s1._get_token(i)
        ch = CHUNK(i,'tk',i,i)
        sint._chunks.append(ch)

##test



from nltk.tokenize import treebank
sent_tokenizer = treebank.TreebankWordTokenizer()



def processMajid(inF,outDir):
    global tOP, sentences,sint
    print 'loading WN'
    iniWN()
    tOP = 'stanford'
    setTypeOfProcess(tOP)
    loadPreProcessedFile(inF)
    getSentenceSegmentation()
    reSegmentNE()
    representSentences()
    savingSint(sentences, outDir+'sint/depconll.sint')
    savingSent(sentences, outDir+'sent/depconll.sent')





## main

##processMajid(workingDirMajid+'depconll.conll',workingDirMajid)


