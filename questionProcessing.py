__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        questionProcessing.py
#
# Author:      Majid
#
# Created:     2014/06/06
# classes used by RepresentingSentences for QAS
#-----------------------------------------------------------------------------

import string
import re
from rule import *
from representingSentences import *
from Constraints import *
from ExpectedAnswerTypes import *
from Answers import *
from managingOntology import *
from recursive_SOP_managingOntology import *
from Recursive_SPARQL_Ontology import *
from Recursive_SPARQL_Person import *
from graphConstraint import *
from prologGraph import *
from graphSentence import *
from mergePrologGraph import *



##functions
def removeTreesFromSentences():
    global sentences, sentences2
    sentences2 =sentences
    for iS in sentences2:
        s = sentences2[iS]
        s.sint._constituents = None

def applyRuleToSentence(r,s):
    workingDirMajid=r.workingDir
    constraintOut="CONST"
    mergeOut="MERGE"
    r.removeAllIndicators()
    r.clearAllVariables()
    # r.removeFilesContent()
    if r.executeConditions(s,r):
        r.removeAllIndicators()
        r.clearAllVariables()
        r.describeBoundedOntology()
        r.executeActions(s,r)
        print "checked before currentRule,r,r.boundedVars,bv:",r,r,r.boundedVars
        if r.boundedVars:
            print "checked r.boundedVars",r.boundedVars
            obtainEAT="obtainEATs" + r.type + "(r,s,workingDirMajid)"
            exec(obtainEAT)
            obtainAnswer="obtainAnswer" + r.type + "(r,s)"
            exec(obtainAnswer)
            s.setConstraints()
            obtainConstraints="obtainConstraints" + r.type + "(r,s)"
            exec(obtainConstraints)
            buildConstraintProlog="build_Constraint_Prolog_" + r.type + "(s,workingDirMajid)"
            exec(buildConstraintProlog)
            buildConstraintGraph="build_Prolog_Graph" + "(s,workingDirMajid,constraintOut)"
            exec(buildConstraintGraph)
            # mergeGenreal_ConstraintPrologGraph(s,workingDirMajid)
            # buildMergeGraph="build_Prolog_Graph" + "(s,workingDirMajid,mergeOut)"
            # exec(buildMergeGraph)
            addEAT2Prolog_Class="addEAT2prolog_Class(r,s)"
            exec(addEAT2Prolog_Class)
          return r.type, r.id, len(r.conds), r.boundedVars, r.boundedConsts
    return None


def applyRulesToSentences():
    global sentences, databaseRules, workingDirMajid, sint
    for iR in databaseRules:
        r = databaseRules[iR]

        for iS in range(len(sentences)):
            s = sentences[iS]
            print 'applying rule', iR, 'to sentence', iS
            R=applyRuleToSentence(r,s)
            print '\n Rule Type & Rule ID  & Rule Conditions are : ', R
            print "-----------------------------------------------------------------------"

           # print sint._dependencies


def applyRulesToSentencesRange(iR,iS1,iS2):
    global sentences, databaseRules
    if iR == 'all':
        iR = databaseRules.keys()

    ok=False
    id=0
    while iS1+id<=iS2:
        # print "Rule ID: ",databaseRules[r].id, " databaseRules[r], len",databaseRules[r].type, len(lR)
        iS=int(iS1)+int(id)
        print "Sentence NO. ", id, "is :", sentences[iS]._text()
        print "Question POS list:","\n",sentences[iS].descriibe_POS()
        print "Question Named Entity (NE) list:","\n",sentences[iS].descriibe_NE()
        print "Dependencies List: ",sentences[iS].sint.describe(True)

        for r in iR:
            R = applyRuleToSentence(databaseRules[r],sentences[iS])
            if R:
                print 'Applying Rule: ', databaseRules[r].type, '--->  To Question: ', sentences[iS]._text()
                print 'Rule Success Matched!!', r, iS, R
                ok = True
                toMapSPARQLFormat(iS,sentences[iS],databaseRules[r])

        id=id+1
    print  "\n","Result of Applying Rules To Sentences : ",ok


def applyRulesToSentences(iR,iS):
    global sentences, databaseRules
    if iR == 'all':
        iR = databaseRules.keys()

    if iS == 'all':
        iS = range(len(sentences))

    ok=False
    id=0
    for s in iS:
        # print "Rule ID: ",databaseRules[r].id, " databaseRules[r], len",databaseRules[r].type, len(lR)
        print "Sentence NO. ", id, "is :", sentences[s]._text()
        print "Question POS list:","\n",sentences[s].descriibe_POS()
        print "Question Named Entity (NE) list:","\n",sentences[s].descriibe_NE()
        print "Dependencies List: ",sentences[s].sint.describe(True)

        for r in iR:
            R = applyRuleToSentence(databaseRules[r],sentences[s])

            if R:
                print 'Applying Rule: ', databaseRules[r].type, '--->  To Question: ', sentences[s]._text()
                print 'Rule Success Matched!!', r, s, R ,"\n"
                ok = True
        id=id+1
    print  "\n","Result of Applying Rules To Sentences : ",ok


def applyRulesToSentence(iR,iS):
    global sentences, databaseRules
    priorityRules=[]
    ok=False
    # print "Rule ID: ",databaseRules[r].id, " databaseRules[r], len",databaseRules[r].type, len(lR)
    print "Sentence NO. ", iS, "is :", sentences[iS]._text()
    print "Question POS list:","\n",sentences[iS].descriibe_POS()
    print "Question Named Entity (NE) list:","\n",sentences[iS].descriibe_NE()
    print "Dependencies List: ",sentences[iS].sint.describe(True)

    if iR == 'all':
        iR = databaseRules.keys()
    elif iR in databaseRules.keys():
        print "Requested Rule to run is",iR
        r=iR
        R = applyRuleToSentence(databaseRules[r],sentences[iS])

        if R:
            print 'Applying Rule: ', databaseRules[r].type, '--->  To Question: ', sentences[iS]._text()
            print 'Rule Success Matched!!', r, iS, R
            ok = True
            priorityRules.append(databaseRules[r].id)
            toMapSPARQLFormat(iS,sentences[iS],databaseRules[r])
        print "\n","Result of Applying Rules To Sentences : ",ok,priorityRules
        return ok

    else:
        print "Request Rule is not defined!!"
        return False

    for r in iR:
        R = applyRuleToSentence(databaseRules[r],sentences[iS])

        if R:
            print 'Applying Rule: ', databaseRules[r].type, '--->  To Question: ', sentences[iS]._text()
            print 'Rule Success Matched!!', r, iS, R
            ok = True
            priorityRules.append(databaseRules[r].id)
            toMapSPARQLFormat(iS,sentences[iS],databaseRules[r])
    print "\n","Result of Applying Rules To Sentences : ",ok,priorityRules



def getAllPredicates():
    global sentences
    predicates={}
    for iS in sentences:
        s = sentences[iS]
        for a1,a2,p in s.sint._dependencies:
            if p not in predicates:
                predicates[p]=1
            else:
                predicates[p]+=1
            if p=="nsubjpass":
                print "nsubjpass:",iS, sentences[iS]._text(),s._text()

    for p in predicates:
        print p,predicates[p]
        



def getAllPOS():
    global sentences
    poses={}
    for iS in sentences:
        s = sentences[iS]
        tks=s._get_tokens()
        for itk in range(len(tks)):
            tk=tks[itk]
            pos=tk._pos()
            if pos not in poses:
                poses[pos]=1
            else:
                poses[pos]+=1

    for p in poses:
        print p,poses[p]


def getAllLemma():
    global sentences
    lemmas={}
    for iS in sentences:
        s = sentences[iS]
        tks=s._get_tokens()
        for itk in range(len(tks)):
            tk=tks[itk]
            lema=tk._lemma()
            if lema not in lemmas:
                lemmas[lema]=1
            else:
                lemmas[lema]+=1

    for l in lemmas:
        print "Accounting of lemma ",l,lemmas[l]


def getAllLevenEshtein():
    global sentences,workingDirMajid
    for iS in sentences:
        s = sentences[iS]
        print 'Applying LevenEshtein to sentence ', iS
        instances4Sentence(s,workingDirMajid)


def getAllNodeCurrentGraph(r):
    global sentences
    g=Graph(r.currentGraph,r.currentGraph_Inst)
    print "New Graph was produced for rule is:","\n", g.__str__()


##main
databaseRules={}

##   YesNO Question Part       ##################

databaseRules['IsthrPrS_1']=QTclassrule('IsthrPrS_1','IsThere_Person_Status')
databaseRules['IsthrPrS_1'].addCondition(QTclasscondition('Isthere','isIsthere(s,r,0)'))
databaseRules['IsthrPrS_1'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
databaseRules['IsthrPrS_1'].addCondition(QTclasscondition('isStatus','isStatus(s,r)'))
databaseRules['IsthrPrS_1'].addAction(QTclassAction('bindPerson','bindPerson(s,r)'))
databaseRules['IsthrPrS_1'].addAction(QTclassAction('bindStatus','bindStatus(s,r)'))

databaseRules['IsthrPrA_1']=QTclassrule('IsthrPrA_1','IsThere_Person_Action')
databaseRules['IsthrPrA_1'].addCondition(QTclasscondition('CIsthere','isIsthere(s,r,0)'))
databaseRules['IsthrPrA_1'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
databaseRules['IsthrPrA_1'].addCondition(QTclasscondition('isAction','isAction(s,r)'))
databaseRules['IsthrPrA_1'].addAction(QTclassAction('bindPerson','bindPerson(s,r)'))
databaseRules['IsthrPrA_1'].addAction(QTclassAction('bindAction','bindAction(s,r)'))



databaseRules['YNoPrAOrg_1']=QTclassrule('YNoPrAOrg_1','YNo_Person_Action_Organization')
databaseRules['YNoPrAOrg_1'].addCondition(QTclasscondition('CYesNo','isYesNo(s,r,0)'))
databaseRules['YNoPrAOrg_1'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
databaseRules['YNoPrAOrg_1'].addCondition(QTclasscondition('isAction','isAction(s,r)'))
databaseRules['YNoPrAOrg_1'].addCondition(QTclasscondition('isOrganization','isOrganization(s,r)'))
databaseRules['YNoPrAOrg_1'].addAction(QTclassAction('bindPerson','bindPerson(s,r)'))
databaseRules['YNoPrAOrg_1'].addAction(QTclassAction('bindAction','bindAction(s,r)'))
databaseRules['YNoPrAOrg_1'].addAction(QTclassAction('bindOrganization','bindOrganization(s,r)'))

databaseRules['YNoPrAOrg_2']=QTclassrule('YNoPrAOrg_2','YNo_Person_Action_Organization')
databaseRules['YNoPrAOrg_2'].addCondition(QTclasscondition('CYesNo','isYesNo(s,r,0)'))
databaseRules['YNoPrAOrg_2'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
databaseRules['YNoPrAOrg_2'].addCondition(QTclasscondition('isAction','isAction(s,r)'))
databaseRules['YNoPrAOrg_2'].addCondition(QTclasscondition('isOrganization','isOrganization(s,r)'))
databaseRules['YNoPrAOrg_2'].addCondition(QTclasscondition('isQuantifier','isQuantifier(s,r)'))
databaseRules['YNoPrAOrg_2'].addAction(QTclassAction('bindPerson','bindPerson(s,r)'))
databaseRules['YNoPrAOrg_2'].addAction(QTclassAction('bindAction','bindAction(s,r)'))
databaseRules['YNoPrAOrg_2'].addAction(QTclassAction('bindOrganization','bindOrganization(s,r)'))
databaseRules['YNoPrAOrg_2'].addAction(QTclassAction('bindQuantifier','bindQuantifier(s,r)'))


##   Where Person Action Question Part       ##################
##   Rule Type for WrPrA_1: Where    Person_tk    Action_tk       ##################

# databaseRules['WrPrA_1']=QTclassrule('WrPrA_1','Where_Person_Action')
# databaseRules['WrPrA_1'].addCondition(QTclasscondition('CWhere','isWhere(s,0)'))
# databaseRules['WrPrA_1'].addCondition(QTclasscondition('isPerson','isPerson(s)'))
# databaseRules['WrPrA_1'].addCondition(QTclasscondition('isAction','isAction(s)'))
# databaseRules['WrPrA_1'].addAction(QTclassAction('bindPerson','bindPerson(s)'))
# databaseRules['WrPrA_1'].addAction(QTclassAction('bindAction','bindAction(s)'))

##   Rule Type for WrPrA_2: Where    Person_Ontology   Action_tk       ##################

# databaseRules['WrPrA_2']=QTclassrule('WrPrA_2','Where_Person_Action')
# databaseRules['WrPrA_2'].addCondition(QTclasscondition('CWhere','isWhere(s,0)'))
# databaseRules['WrPrA_2'].addCondition(QTclasscondition('graphlook','isPersonInOntology(s,"'+workingDirMajid+'","i_en_proper_person")'))
# databaseRules['WrPrA_2'].addCondition(QTclasscondition('isAction','isAction(s)'))
# databaseRules['WrPrA_2'].addAction(QTclassAction('bindPersonOnt','bindPersonOnt(s,"'+workingDirMajid+'","i_en_proper_person")'))
# databaseRules['WrPrA_2'].addAction(QTclassAction('bindAction','bindAction(s)'))
# databaseRules['WrPrA_2'].addAction(QTclassAction('bindEAT','bindWhereOnt(s,"'+workingDirMajid+'","i_en_proper_organization")'))

##   Rule Type for WrPrA_3: Where_in    Person_Ontology   Action_tk       ##################

# databaseRules['WrPrA_3']=QTclassrule('WrPrA_3','Where_Person_Action')
# databaseRules['WrPrA_3'].addCondition(QTclasscondition('CWhere_in','isWhere_in(s)'))
# databaseRules['WrPrA_3'].addCondition(QTclasscondition('isPersonIn_Ont','isPersonIn_Ont(s,"'+workingDirMajid+'","i_en_proper_person")'))
# databaseRules['WrPrA_3'].addCondition(QTclasscondition('isAction','isAction(s)'))
# databaseRules['WrPrA_3'].addAction(QTclassAction('bindPersonOnt','bindPerson_Ont(s,"'+workingDirMajid+'","i_en_proper_person")'))
# databaseRules['WrPrA_3'].addAction(QTclassAction('bindAction','bindAction(s)'))
# databaseRules['WrPrA_3'].addAction(QTclassAction('bindWhere_in','bindWhere_in(s)'))

##   Rule Type for WrPrA_4: Where_in_Ontology    Person_Ontology   Action_tk       ##################

# databaseRules['WrPrA_4']=QTclassrule('WrPrA_4','Where_Person_Action')
# databaseRules['WrPrA_4'].addCondition(QTclasscondition('CWhere_Ont','isWhere(s,r,0)'))
# databaseRules['WrPrA_4'].addCondition(QTclasscondition('isPersonIn_Ont','isPersonIn_Ont(s,"'+workingDirMajid+'","i_en_proper_person")'))
# databaseRules['WrPrA_4'].addCondition(QTclasscondition('isAction','isAction(s,r)'))
# databaseRules['WrPrA_4'].addAction(QTclassAction('bindAction','bindAction(s,r)'))
# databaseRules['WrPrA_4'].addAction(QTclassAction('bindPersonOnt','bindPerson_Ont(s,"'+workingDirMajid+'","i_en_proper_person")'))
# databaseRules['WrPrA_4'].addAction(QTclassAction('bindWhere_Ont','bindWhere(s,r,0)'))


##   Rule Type for WrPrA_5: Where    Person_tk   Action_Ontology       ##################


# databaseRules['WrPrA_5']=QTclassrule('WrPrA_5','Where_Person_Action')
# databaseRules['WrPrA_5'].addCondition(QTclasscondition('CWhere','isWhere(s,0)'))
# databaseRules['WrPrA_5'].addCondition(QTclasscondition('isPerson','isPerson(s)'))
# databaseRules['WrPrA_5'].addCondition(QTclasscondition('graphlook','isActionInOntology(s,"'+workingDirMajid+'","action")'))
# databaseRules['WrPrA_5'].addAction(QTclassAction('bindPerson','bindPerson(s)'))
# databaseRules['WrPrA_5'].addAction(QTclassAction('bindAction','bindAction(s)'))
# databaseRules['WrPrA_5'].addAction(QTclassAction('bindActionOnt','bindActionOnt(s,"'+workingDirMajid+'","action")'))



#
databaseRules['WoPropPr_1']=QTclassrule('WoPropPr_1','Who_Properties_Person')
databaseRules['WoPropPr_1'].addCondition(QTclasscondition('CWho','isWho(s,r,0)'))
databaseRules['WoPropPr_1'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
databaseRules['WoPropPr_1'].addCondition(QTclasscondition('isProperties','isProperties(s,r)'))
databaseRules['WoPropPr_1'].addAction(QTclassAction('bindPersonOnt','bindPerson_Ont(s,"'+workingDirMajid+'","i_en_proper_person")'))
databaseRules['WoPropPr_1'].addAction(QTclassAction('bindProperties','bindProperties(s,r)'))
databaseRules['WoPropPr_1'].addAction(QTclassAction('bindWho','bindWho(s,r,0)'))

#
# databaseRules['WoCmpPropPr_1']=QTclassrule('WoCmpPropPr_1','Who_CompoundProperties_Person')
# databaseRules['WoCmpPropPr_1'].addCondition(QTclasscondition('CWho','isWho(s,r,0)'))
# databaseRules['WoCmpPropPr_1'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
# databaseRules['WoCmpPropPr_1'].addCondition(QTclasscondition('isCompound_Properties','isCompound_Properties(s,r)'))
# databaseRules['WoCmpPropPr_1'].addAction(QTclassAction('bindWho','bindWho(s,r,0)'))
# databaseRules['WoCmpPropPr_1'].addAction(QTclassAction('bindPerson','bindPerson(s,r)'))
# databaseRules['WoCmpPropPr_1'].addAction(QTclassAction('bindCompound_Properties','bindCompound_Properties(s,r)'))


# databaseRules['WchAProp_1']=QTclassrule('WchPrAProp_1','Which_Person_Action_Properties')
# databaseRules['WchPrAProp_1'].addCondition(QTclasscondition('CWhich','isWhich(s,r,0)'))
# databaseRules['WchPrAProp_1'].addCondition(QTclasscondition('isPerson','isPerson(s,r)'))
# databaseRules['WchPrAProp_1'].addCondition(QTclasscondition('isAction','isAction(s,r)'))
# databaseRules['WchPrAProp_1'].addCondition(QTclasscondition('isProperties','isProperties(s,r)'))
# databaseRules['WchPrAProp_1'].addAction(QTclassAction('bindWhich','bindWhich(s,r)'))
# databaseRules['WchPrAProp_1'].addAction(QTclassAction('bindPerson','bindPerson(s,r)'))
# databaseRules['WchPrAProp_1'].addAction(QTclassAction('bindAction','bindAction(s,r)'))
# databaseRules['WchPrAProp_1'].addAction(QTclassAction('bindProperties','bindProperties(s,r)'))
#
workingDirMajid=databaseRules['WoPropPr_1'].workingDir
databaseRules['WoPropPr_1'].removeFilesContent()
processMajid(workingDirMajid+'depconll.conll', workingDirMajid)
from representingSentences import sentences
from representingSentences import buildSintDep
# from representingSentences import workingDirMajid

from auxiliar import SENT as mysent

# for iS in sentences:
#         s = sentences[iS]
#         print "Sentence is :", sentences[iS]._text()
#         sentences[iS].describe()

print "Sentence is :", sentences[23]._text()
sentences[23].describe()

# getAllPredicates()
# getAllPOS()

#print mysent.describe()

# r1 = databaseRules['WrPrA_2']
##isInClass(s1,workingDirMajid)

#print applyRuleToSentence(r1,s1)

# applyRulesToSentences()


s=sentences[23]
import sys
print "Recursive stack is ",sys.getrecursionlimit()
sys.setrecursionlimit(30000)
print "Recursive stack is ",sys.getrecursionlimit()
allclasses4Sentence(s,workingDirMajid)
allslots4Sentence(s,workingDirMajid)
slots4Classes(s,workingDirMajid)
# subclasses4Class(s,workingDirMajid)
allinstances4Sentence(s,workingDirMajid)
# isPersonIn_Ont(s,workingDirMajid,"i_en_proper_person")
R=applyRuleToSentence(databaseRules['WoPropPr_1'],sentences[23])


# iS=54
# s=sentences[iS]
# print "Sentence is :", sentences[iS]._text()
# R=applyRulesToSentences('all','all')
# R=applyRulesToSentence('all',iS)

# removeTreesFromSentences()
# mappingSPARQL(sentences2)


# print "Sentence is :", sentences[iS]._text()
# print "Question POS list:","\n",s.descriibe_POS()
# print "Question Named Entity (NE) list:","\n",s.descriibe_NE()
# print "Dependencies List: ",s.sint.describe(True)
#
# if R!=None:
#     cs = s._constraints
#     cs.describe()





# classes4Sentence(s,workingDirMajid)

# slots4Classes(s,workingDirMajid)
# gen_graph(dot,workingDirMajid)




# getAllNodeCurrentGraph(r1)
# createGraphOntology()
# addTriples()
# creatGraphSentence(s,workingDirMajid)




# print "\n","All CLASSES that were founded in sentence are:","\n"
# isTokensInClass(s,workingDirMajid)
# print "\n","All SLOTS that were founded in sentence are:  ","\n"
# isTokensInSlot(s,workingDirMajid)
# print "\n","All INSTANCES that were founded in sentence are: ","\n"
# isTokensInInstance(s,workingDirMajid)

# getAllPredicates()
# getAllPOS()
# getAllLemma()

