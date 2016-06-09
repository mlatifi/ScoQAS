__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        rule.py
#
# Author:      Majid
#
# Created:     2014/06/06
# classes used by RepresentingSentences for QAS
#-----------------------------------------------------------------------------

import string
import re
from managingOntology import *
from recursive_SOP_managingOntology import *
from Recursive_SPARQL_Ontology import *
# from questionProcessing import *
# from dbpediaTests import *
# from Recursive_Endpoint_SPARQL_Person import *
from Recursive_SPARQL_Person import *
from graphviz import Digraph,Graph
import networkx as nx


##classes

class QTclassrule(object):

    def __init__(self,id,t):
        self._init_vars(id,t)

    def _init_vars(self,id,t):
        global currentRule
        currentRule = self
        self.id=id
        self.workingDir = 'D:/PhD/PhD Tesis/Project/RepresentingSentences/data/'
        self.conds=[]
        self.actions=[]
        self.constraints=[]
        self.EATs=[]
        self.tk_indicators=[]

        self.type=t
        self.boundedVars={}
        self.boundedConsts={}
        self.boundedEATs={}

        self.boundedClass={}
        self.boundedSubClass={}
        self.boundedSlot={}
        self.boundedSlot4Class={}
        self.boundedInstance={}

        self.boundedGraphClass={}
        self.boundedGraphSubClass={}
        self.boundedGraphSlot={}
        self.boundedGraphSlot4Class={}
        self.boundedGraphInstance={}

        self.currentDGraph=nx.DiGraph()
        self.currentConsDGraph=nx.DiGraph()
        self.currentPrologDGraph=nx.DiGraph()
        self.currentMergeDGraph=nx.DiGraph()
        self.currentGraph_Inst={}

        self.boundedClassAnswer={}
        self.boundedSubClassAnswer={}
        self.boundedSlotAnswer={}
        self.boundedSlotTypeAnswer={}
        self.boundedInstanceAnswer={}
        self.boundedExactSlotAnswer={}
        self.boundedExactInstanceAnswer={}
        self.boundedExactAnswer={}

        self.boundedClassAction={}
        self.boundedSlotAction={}
        self.boundedSlotTypeAction={}
        self.boundedInstanceAction={}

        self.boundedClassWhere={}
        self.boundedSubClassWhere={}
        self.boundedSlotWhere={}
        self.boundedSlotTypeWhere={}
        self.boundedInstanceWhere={}

        self.boundedClassWhich={}
        self.boundedSlotWhich={}
        self.boundedInstanceWhich={}

        self.boundedClassItem={}
        self.boundedSubClassItem={}
        self.boundedSlotItem={}
        self.boundedSlotTypeItem={}
        self.boundedInstanceItem={}

        self.boundedClassWhere_in={}
        self.boundedSubClassWhere_in={}
        self.boundedSlotWhere_in={}
        self.boundedSlotTypeWhere_in={}
        self.boundedInstanceWhere_in={}

        self.boundedClassWho={}
        self.boundedSubClassWho={}
        self.boundedSlotWho={}
        self.boundedSlotTypeWho={}
        self.boundedInstanceWho={}

        self.boundedClassWhat={}
        self.boundedSubClassWhat={}
        self.boundedSlotWhat={}
        self.boundedSlotTypeWhat={}
        self.boundedInstanceWhat={}

        self.boundedClassWhen={}
        self.boundedSubClassWhen={}
        self.boundedSlotWhen={}
        self.boundedSlotTypeWhen={}
        self.boundedInstanceWhen={}

        self.boundedClassHowmuch={}
        self.boundedSubClassHowmuch={}
        self.boundedSlotHowmuch={}
        self.boundedSlotTypeHowmuch={}
        self.boundedInstanceHowmuch={}

        self.boundedClassMemb={}
        self.boundedSubClassMemb={}
        self.boundedSlotMemb={}
        self.boundedSlotTypeMemb={}
        self.boundedInstanceMemb={}

        self.boundedClassStatus={}
        self.boundedSubClassStatus={}
        self.boundedSlotStatus={}
        self.boundedSlotTypeStatus={}
        self.boundedInstanceStatus={}

        self.boundedClassEnt={}
        self.boundedSubClassEnt={}
        self.boundedSlotEnt={}
        self.boundedSlotTypeEnt={}
        self.boundedInstanceEnt={}

        self.boundedClassPerson={}
        self.boundedSubClassPerson={}
        self.boundedSlotPerson={}
        self.boundedSlotTypePerson={}
        self.boundedInstancePerson={}

        self.boundedClassCmpProp={}
        self.boundedSubClassCmpProp={}
        self.boundedSlotCmpProp={}
        self.boundedSlotTypeCmpProp={}
        self.boundedInstanceCmpProp={}

        self.boundedClassProp={}
        self.boundedSubClassProp={}
        self.boundedSlotProp={}
        self.boundedSlotTypeProp={}
        self.boundedInstanceProp={}


    def addCondition(self,c):
        self.conds.append(c)

    def addAction(self,a):
        self.actions.append(a)

    def addConstraint(self,c):
        self.constraints.append(c)

    def addEAT(self,answT):
        self.EATs.append(answT)

    def addIndicators_tk(self,tk_ind):
        if not (tk_ind in self.tk_indicators):
            self.tk_indicators.append(tk_ind)

    def addIndicatorsList_tk(self,tkList_ind):
        tkList_Indicator=list(set(tkList_ind))
        for item in range(len(tkList_Indicator)):
            if not (tkList_Indicator[item] in self.tk_indicators):
                self.tk_indicators.append(tkList_Indicator[item])


    def addBoundedVars(self,item,bindVars):

        if not(self.existBoundedVars(item,bindVars)):
            self.boundedVars[item]=bindVars
            # print "This Vars added to bindVars,item: ",bindVars,item,self.boundedVars
            return True
        else:
            return False


    def addBoundedList_Vars(self,item,bindListVars):
        bListVars=list(set(bindListVars))
        if not(self.existBoundedVars(item,bListVars)):
            self.boundedVars[item]=bListVars
            # print "This Vars added to bindListVars,item: ",bListVars,item,self.boundedVars
            return True
        else:
            return False

    def addBoundedClass(self,bindClass,tk,i):
        if not(self.existBoundedClass(bindClass,tk,i)):
            self.boundedClass[tk,i]=bindClass
            # print "WOOW!!, This class added to list,itk,i",bindClass,tk,i
            return True
        else:
            return False


    def addBoundedClassItem(self,bindClassItem0,tk,i):
        if not(self.existBoundedClassItem(bindClassItem0,tk,1)):
            self.boundedClassItem[tk,i]=bindClassItem0
            return True
        else:
            return False


    def addBoundedClassAction(self,bindClassAction0,tk,i):
        if not(self.existBoundedClassAction(bindClassAction0,tk,1)):
            self.boundedClassAction[tk,i]=bindClassAction0
            return True
        else:
            return False


    def addBoundedClassAnswer(self,bindClassAnswer0,tk,i):
        if not(self.existBoundedClassAnswer(bindClassAnswer0,tk,1)):
            self.boundedClassAnswer[tk,i]=bindClassAnswer0
            return True
        else:
            return False

    def addBoundedClassWhere(self,bindClassW0,tk,i):
        if not(self.existBoundedClassWhere(bindClassW0,tk,1)):
            self.boundedClassWhere[tk,i]=bindClassW0
            return True
        else:
            return False

    def addBoundedClassWho(self,bindClassW0,tk,i):
        if not(self.existBoundedClassWho(bindClassW0,tk,1)):
            self.boundedClassWho[tk,i]=bindClassW0
            # print "This class added to list ClassWhere_in",bindClassW0,tk,i
            return True
        else:
            return False

    def addBoundedClassWhen(self,bindClassW0,tk,i):
        if not(self.existBoundedClassWhen(bindClassW0,tk,1)):
            self.boundedClassWhen[tk,i]=bindClassW0
            # print "This class added to list ClassWhere_in",bindClassW0,tk,i
            return True
        else:
            return False


    def addBoundedClassWhat(self,bindClassW0,tk,i):
        if not(self.existBoundedClassWhat(bindClassW0,tk,1)):
            self.boundedClassWhat[tk,i]=bindClassW0
            # print "This class added to list ClassWhere_in",bindClassW0,tk,i
            return True
        else:
            return False

    def addBoundedClassHowmuch(self,bindClassHM0,tk,i):
        if not(self.existBoundedClassHowmuch(bindClassHM0,tk,1)):
            self.boundedClassHowmuch[tk,i]=bindClassHM0
            return True
        else:
            return False

    def addBoundedClassPerson(self,bindClassP0,tk,i):
        if not(self.existBoundedClassPerson(bindClassP0,tk,1)):
            self.boundedClassPerson[tk,i]=bindClassP0
            return True
        else:
            return False

    def addBoundedClassMemb(self,bindClassMemb0,tk,i):
        if not(self.existBoundedClassMemb(bindClassMemb0,tk,1)):
            self.boundedClassMemb[tk,i]=bindClassMemb0
            return True
        else:
            return False


    def addBoundedClassStatus(self,bindClassStatus0,tk,i):
        if not(self.existBoundedClassStatus(bindClassStatus0,tk,1)):
            self.boundedClassStatus[tk,i]=bindClassStatus0
            return True
        else:
            return False


    def addBoundedClassCmpProp(self,bindClassCmpProp0,tk,i):
        if not(self.existBoundedClassCmpProp(bindClassCmpProp0,tk,1)):
            self.boundedClassCmpProp[tk,i]=bindClassCmpProp0
            return True
        else:
            return False

    def addBoundedClassEnt(self,bindClassEnt0,tk,i):
        if not(self.existBoundedClassEnt(bindClassEnt0,tk,1)):
            self.boundedClassEnt[tk,i]=bindClassEnt0
            return True
        else:
            return False


    def addBoundedSubClass(self,bindSubClass,tk,i):
        bindSubClasslocal=bindSubClass
        if not(self.existBoundedSubClass(bindSubClass,tk,i)):
            self.boundedSubClass[tk,i]=bindSubClasslocal
            self.boundedSubClass[tk,i][0]=bindSubClasslocal[0]
            self.boundedSubClass[tk,i][1]=bindSubClasslocal[1]

            return True

        else:
            return False

    def addBoundedSubClassWhere_in(self,bindSubClassW,bindSubClassW0,bindSubClassW1,tk,i):
        bindSubClasslocal=bindSubClassW
        if not(self.existBoundedSubClassWhere_in(bindSubClassW0,bindSubClassW1,tk,i)):
            self.boundedSubClassWhere_in[tk,i]=bindSubClasslocal
            self.boundedSubClassWhere_in[tk,i][0]=bindSubClassW0
            self.boundedSubClassWhere_in[tk,i][1]=bindSubClassW1

            return True

        else:
            return False

    def addBoundedSubClassWho(self,bindSubClassW,bindSubClassW0,bindSubClassW1,tk,i):
        bindSubClasslocal=bindSubClassW
        if not(self.existBoundedSubClassWho(bindSubClassW0,bindSubClassW1,tk,i)):
            self.boundedSubClassWho[tk,i]=bindSubClasslocal
            self.boundedSubClassWho[tk,i][0]=bindSubClassW0
            self.boundedSubClassWho[tk,i][1]=bindSubClassW1

            return True

        else:
            return False


    def addBoundedSubClassPerson(self,bindSubClassP,bindSubClassP0,bindSubClassP1,tk,i):
        bindSubClasslocal=bindSubClassP
        if not(self.existBoundedSubClassPerson(bindSubClassP0,bindSubClassP1,tk,i)):
            self.boundedSubClassPerson[tk,i]=bindSubClasslocal
            self.boundedSubClassPerson[tk,i][0]=bindSubClassP0
            self.boundedSubClassPerson[tk,i][1]=bindSubClassP1

            return True

        else:
            return False


    def addBoundedSlot(self,bindSlot,tk,i):
        bindSlotlocal=bindSlot
        if not(self.existBoundedSlot(bindSlot,tk,i)):
            self.boundedSlot[tk,i]=bindSlotlocal
            self.boundedSlot[tk,i][0]=bindSlotlocal[0]
            self.boundedSlot[tk,i][1]=bindSlotlocal[1]
            return True
        else:
            return False

    def addBoundedSlots4Classes(self,bindSlot4Class,bindSlot4Class0,bindSlot4Class1,tk,i):
        bindSlot4Clslocal=bindSlot4Class
        if not(self.existBoundedSlot4Class(bindSlot4Class0,bindSlot4Class1,tk,i)):
            self.boundedSlot4Class[tk,i]=bindSlot4Clslocal
            self.boundedSlot4Class[tk,i][0]=bindSlot4Class0
            self.boundedSlot4Class[tk,i][1]=bindSlot4Class1
            return True
        else:
            return False


    def addBoundedExactSlotAnswer(self,bindExSlotAnswer,bindExSlotAnswer0,bindExSlotAnswer1,tk,i):
        bindSlotlocal=bindExSlotAnswer
        if not(self.existBoundedExactSlotAnswer(bindExSlotAnswer0,bindExSlotAnswer1,tk,i)):
            self.boundedExactSlotAnswer[tk,i]=bindSlotlocal
            self.boundedExactSlotAnswer[tk,i][0]=bindExSlotAnswer0
            self.boundedExactSlotAnswer[tk,i][1]=bindExSlotAnswer1
            return True
        else:
            return False


    def addBoundedSlotItem(self,bindSlotItem,bindSlotItem0,bindSlotItem1,tk,i):
        bindSlotlocal=bindSlotItem
        if not(self.existBoundedSlotItem(bindSlotItem0,bindSlotItem1,tk,i)):
            # print "WOOW1!!, This slot added to SlotWhere_in,itk,i",bindSlotW0,bindSlotW1,tk,i
            self.boundedSlotItem[tk,i]=bindSlotlocal
            self.boundedSlotItem[tk,i][0]=bindSlotItem0
            self.boundedSlotItem[tk,i][1]=bindSlotItem1
            return True
        else:
            return False


    def addBoundedSlotAction(self,bindSlotAction,bindSlotAction0,bindSlotAction1,tk,i):
        bindSlotlocal=bindSlotAction
        if not(self.existBoundedSlotAction(bindSlotAction0,bindSlotAction1,tk,i)):
            # print "WOOW1!!, This slot added to SlotWhere_in,itk,i",bindSlotW0,bindSlotW1,tk,i
            self.boundedSlotAction[tk,i]=bindSlotlocal
            self.boundedSlotAction[tk,i][0]=bindSlotAction0
            self.boundedSlotAction[tk,i][1]=bindSlotAction1
            return True
        else:
            return False


    def addBoundedSlotAnswer(self,bindSlotAnswer,bindSlotAnswer0,bindSlotAnswer1,tk,i):
        bindSlotlocal=bindSlotAnswer
        if not(self.existBoundedSlotAnswer(bindSlotAnswer0,bindSlotAnswer1,tk,i)):
            # print "WOOW1!!, This slot added to SlotWhere_in,itk,i",bindSlotW0,bindSlotW1,tk,i
            self.boundedSlotAnswer[tk,i]=bindSlotlocal
            self.boundedSlotAnswer[tk,i][0]=bindSlotAnswer0
            self.boundedSlotAnswer[tk,i][1]=bindSlotAnswer1
            return True
        else:
            return False

    def addBoundedSlotWho(self,bindSlotW,bindSlotW0,bindSlotW1,tk,i):
        bindSlotlocal=bindSlotW
        if not(self.existBoundedSlotWho(bindSlotW0,bindSlotW1,tk,i)):
            # print "WOOW1!!, This slot added to SlotWhere_in,itk,i",bindSlotW0,bindSlotW1,tk,i
            self.boundedSlotWho[tk,i]=bindSlotlocal
            self.boundedSlotWho[tk,i][0]=bindSlotW0
            self.boundedSlotWho[tk,i][1]=bindSlotW1
            return True
        else:
            return False


    def addBoundedSlotWhere(self,bindSlotW,bindSlotW0,bindSlotW1,tk,i):
        bindSlotlocal=bindSlotW
        if not(self.existBoundedSlotWhere(bindSlotW0,bindSlotW1,tk,i)):
            # print "WOOW1!!, This slot added to SlotWhere_in,itk,i",bindSlotW0,bindSlotW1,tk,i
            self.boundedSlotWhere[tk,i]=bindSlotlocal
            self.boundedSlotWhere[tk,i][0]=bindSlotW0
            self.boundedSlotWhere[tk,i][1]=bindSlotW1
            return True
        else:
            return False


    def addBoundedSlotWhen(self,bindSlotW,bindSlotW0,bindSlotW1,tk,i):
        bindSlotlocal=bindSlotW
        if not(self.existBoundedSlotWhen(bindSlotW0,bindSlotW1,tk,i)):
            self.boundedSlotWhen[tk,i]=bindSlotlocal
            self.boundedSlotWhen[tk,i][0]=bindSlotW0
            self.boundedSlotWhen[tk,i][1]=bindSlotW1
            return True
        else:
            return False


    def addBoundedSlotHowmuch(self,bindSlotHM,bindSlotHM0,bindSlotHM1,tk,i):
        bindSlotlocal=bindSlotHM
        if not(self.existBoundedSlotHowmuch(bindSlotHM0,bindSlotHM1,tk,i)):
            self.boundedSlotHowmuch[tk,i]=bindSlotlocal
            self.boundedSlotHowmuch[tk,i][0]=bindSlotHM0
            self.boundedSlotHowmuch[tk,i][1]=bindSlotHM1
            return True
        else:
            return False


    def addBoundedSlotWhat(self,bindSlotW,bindSlotW0,bindSlotW1,tk,i):
        bindSlotlocal=bindSlotW
        if not(self.existBoundedSlotWhat(bindSlotW0,bindSlotW1,tk,i)):
            # print "WOOW1!!, This slot added to SlotWhere_in,itk,i",bindSlotW0,bindSlotW1,tk,i
            self.boundedSlotWhat[tk,i]=bindSlotlocal
            self.boundedSlotWhat[tk,i][0]=bindSlotW0
            self.boundedSlotWhat[tk,i][1]=bindSlotW1
            return True
        else:
            return False


    def addBoundedSlotMemb(self,bindSlotMemb,bindSlotMemb0,bindSlotMemb1,tk,i):
        bindSlotlocal=bindSlotMemb
        if not(self.existBoundedSlotMemb(bindSlotMemb0,bindSlotMemb1,tk,i)):
            self.boundedSlotMemb[tk,i]=bindSlotlocal
            self.boundedSlotMemb[tk,i][0]=bindSlotMemb0
            self.boundedSlotMemb[tk,i][1]=bindSlotMemb1
            return True
        else:
            return False


    def addBoundedSlotStatus(self,bindSlotStatus,bindSlotStatus0,bindSlotStatus1,tk,i):
        bindSlotlocal=bindSlotStatus
        if not(self.existBoundedSlotStatus(bindSlotStatus0,bindSlotStatus1,tk,i)):
            self.boundedSlotStatus[tk,i]=bindSlotlocal
            self.boundedSlotStatus[tk,i][0]=bindSlotStatus0
            self.boundedSlotStatus[tk,i][1]=bindSlotStatus1
            return True
        else:
            return False


    def addBoundedSlotCmpProp(self,bindSlotCmpProp,bindSlotCmpProp0,bindSlotCmpProp1,tk,i):
        bindSlotlocal=bindSlotCmpProp
        if not(self.existBoundedSlotCmpProp(bindSlotCmpProp0,bindSlotCmpProp1,tk,i)):
            self.boundedSlotCmpProp[tk,i]=bindSlotlocal
            self.boundedSlotCmpProp[tk,i][0]=bindSlotCmpProp0
            self.boundedSlotCmpProp[tk,i][1]=bindSlotCmpProp1
            return True
        else:
            return False

    def addBoundedSlotEnt(self,bindSlotEnt,bindSlotEnt0,bindSlotEnt1,tk,i):
        bindSlotlocal=bindSlotEnt
        if not(self.existBoundedSlotEnt(bindSlotEnt0,bindSlotEnt1,tk,i)):
            self.boundedSlotEnt[tk,i]=bindSlotlocal
            self.boundedSlotEnt[tk,i][0]=bindSlotEnt0
            self.boundedSlotEnt[tk,i][1]=bindSlotEnt1
            return True
        else:
            return False


    def addBoundedSlotTypeAction(self,bindSlotTypeAction,bindSlotTypeAction0,bindSlotTypeAction1,tk,i):
        bindSlotlocal=bindSlotTypeAction
        if not(self.existBoundedSlotTypeAction(bindSlotTypeAction0,bindSlotTypeAction1,tk,i)):
            # print "WOOW1!!, This slot added to SlotTypeAction",bindSlotTypeAction0,bindSlotTypeAction1,i
            self.boundedSlotTypeAction[tk,i]=bindSlotlocal
            self.boundedSlotTypeAction[tk,i][0]=bindSlotTypeAction0
            self.boundedSlotTypeAction[tk,i][1]=bindSlotTypeAction1
            return True
        else:
            return False


    def addBoundedSlotTypeAnswer(self,bindSlotTypeAnswer,bindSlotTypeAnswer0,bindSlotTypeAnswer1,tk,i):
        bindSlotlocal=bindSlotTypeAnswer
        if not(self.existBoundedSlotTypeAnswer(bindSlotTypeAnswer0,bindSlotTypeAnswer1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeAnswer",bindSlotTypeAnswer0,bindSlotTypeAnswer1,i
            self.boundedSlotTypeAnswer[tk,i]=bindSlotlocal
            self.boundedSlotTypeAnswer[tk,i][0]=bindSlotTypeAnswer0
            self.boundedSlotTypeAnswer[tk,i][1]=bindSlotTypeAnswer1
            return True
        else:
            return False

    def addBoundedSlotTypeMemb(self,bindSlotTypeMemb,bindSlotTypeMemb0,bindSlotTypeMemb1,tk,i):
        bindSlotlocal=bindSlotTypeMemb
        if not(self.existBoundedSlotTypeMemb(bindSlotTypeMemb0,bindSlotTypeMemb1,tk,i)):
            # print "WOOW1!!, This slot added to SlotTypeMemb",bindSlotTypeMemb0,bindSlotTypeMemb1,i
            self.boundedSlotTypeMemb[tk,i]=bindSlotlocal
            self.boundedSlotTypeMemb[tk,i][0]=bindSlotTypeMemb0
            self.boundedSlotTypeMemb[tk,i][1]=bindSlotTypeMemb1
            return True
        else:
            return False


    def addBoundedSlotTypeStatus(self,bindSlotTypeStatus,bindSlotTypeStatus0,bindSlotTypeStatus1,tk,i):
        bindSlotlocal=bindSlotTypeStatus
        if not(self.existBoundedSlotTypeStatus(bindSlotTypeStatus0,bindSlotTypeStatus1,tk,i)):
            # print "WOOW1!!, This slot added to SlotTypeStatus",bindSlotTypeStatus0,bindSlotTypeStatus1,i
            self.boundedSlotTypeStatus[tk,i]=bindSlotlocal
            self.boundedSlotTypeStatus[tk,i][0]=bindSlotTypeStatus0
            self.boundedSlotTypeStatus[tk,i][1]=bindSlotTypeStatus1
            return True
        else:
            return False


    def addBoundedSlotTypeCmpProp(self,bindSlotTypeCmpProp,bindSlotTypeCmpProp0,bindSlotTypeCmpProp1,tk,i):
        bindSlotlocal=bindSlotTypeCmpProp
        if not(self.existBoundedSlotTypeCmpProp(bindSlotTypeCmpProp0,bindSlotTypeCmpProp1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeStatus",bindSlotTypeCmpProp0,bindSlotTypeCmpProp1,i
            self.boundedSlotTypeStatus[tk,i]=bindSlotlocal
            self.boundedSlotTypeStatus[tk,i][0]=bindSlotTypeCmpProp0
            self.boundedSlotTypeStatus[tk,i][1]=bindSlotTypeCmpProp1
            return True
        else:
            return False



    def addBoundedSlotTypePerson(self,bindSlotTypePer,bindSlotTypePer0,bindSlotTypePer1,tk,i):
        bindSlotlocal=bindSlotTypePer
        if not(self.existBoundedSlotTypePerson(bindSlotTypePer0,bindSlotTypePer1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypePerson",bindSlotTypePer0,bindSlotTypePer1,i
            self.boundedSlotTypePerson[tk,i]=bindSlotlocal
            self.boundedSlotTypePerson[tk,i][0]=bindSlotTypePer0
            self.boundedSlotTypePerson[tk,i][1]=bindSlotTypePer1
            return True
        else:
            return False

    def addBoundedSlotTypeEnt(self,bindSlotTypeEnt,bindSlotTypeEnt0,bindSlotTypeEnt1,tk,i):
        bindSlotlocal=bindSlotTypeEnt
        if not(self.existBoundedSlotTypeEnt(bindSlotTypeEnt0,bindSlotTypeEnt1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeEnt",bindSlotTypeEnt0,bindSlotTypeEnt1,i
            self.boundedSlotTypeEnt[tk,i]=bindSlotlocal
            self.boundedSlotTypeEnt[tk,i][0]=bindSlotTypeEnt0
            self.boundedSlotTypeEnt[tk,i][1]=bindSlotTypeEnt1
            return True
        else:
            return False



    def addBoundedSlotTypeWho(self,bindSlotTypeW,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        bindSlotlocal=bindSlotTypeW
        if not(self.existBoundedSlotTypeWho(bindSlotTypeW0,bindSlotTypeW1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeWho",bindSlotTypeW0,bindSlotTypeW1,i
            self.boundedSlotTypeWho[tk,i]=bindSlotlocal
            self.boundedSlotTypeWho[tk,i][0]=bindSlotTypeW0
            self.boundedSlotTypeWho[tk,i][1]=bindSlotTypeW1
            return True
        else:
            return False


    def addBoundedSlotTypeWhen(self,bindSlotTypeW,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        bindSlotlocal=bindSlotTypeW
        if not(self.existBoundedSlotTypeWhen(bindSlotTypeW0,bindSlotTypeW1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeWhen",bindSlotTypeW0,bindSlotTypeW1,i
            self.boundedSlotTypeWhen[tk,i]=bindSlotlocal
            self.boundedSlotTypeWhen[tk,i][0]=bindSlotTypeW0
            self.boundedSlotTypeWhen[tk,i][1]=bindSlotTypeW1
            return True
        else:
            return False


    def addBoundedSlotTypeWhat(self,bindSlotTypeW,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        bindSlotlocal=bindSlotTypeW
        if not(self.existBoundedSlotTypeWhat(bindSlotTypeW0,bindSlotTypeW1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeWhat",bindSlotTypeW0,bindSlotTypeW1,i
            self.boundedSlotTypeWhat[tk,i]=bindSlotlocal
            self.boundedSlotTypeWhat[tk,i][0]=bindSlotTypeW0
            self.boundedSlotTypeWhat[tk,i][1]=bindSlotTypeW1
            return True
        else:
            return False


    def addBoundedSlotTypeHowmuch(self,bindSlotTypeW,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        bindSlotlocal=bindSlotTypeW
        if not(self.existBoundedSlotTypeHowmuch(bindSlotTypeW0,bindSlotTypeW1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeHowmuch",bindSlotTypeW0,bindSlotTypeW1,i
            self.boundedSlotTypeHowmuch[tk,i]=bindSlotlocal
            self.boundedSlotTypeHowmuch[tk,i][0]=bindSlotTypeW0
            self.boundedSlotTypeHowmuch[tk,i][1]=bindSlotTypeW1
            return True
        else:
            return False


    def addBoundedSlotTypeWhere(self,bindSlotTypeW,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        bindSlotlocal=bindSlotTypeW
        if not(self.existBoundedSlotTypeWhere(bindSlotTypeW0,bindSlotTypeW1,tk,i)):
            # print "WOOW1!!, This slot added to SlotTypeWhere",bindSlotTypeW0,bindSlotTypeW1,i
            self.boundedSlotTypeWhere[tk,i]=bindSlotlocal
            self.boundedSlotTypeWhere[tk,i][0]=bindSlotTypeW0
            self.boundedSlotTypeWhere[tk,i][1]=bindSlotTypeW1
            return True
        else:
            return False

    def addBoundedSlotTypeWhere_in(self,bindSlotTypeW,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        bindSlotlocal=bindSlotTypeW
        if not(self.existBoundedSlotTypeWhere_in(bindSlotTypeW0,bindSlotTypeW1,tk,i)):
            print "WOOW1!!, This slot added to SlotTypeWhere_in",bindSlotTypeW0,bindSlotTypeW1,i
            self.boundedSlotTypeWhere_in[tk,i]=bindSlotlocal
            self.boundedSlotTypeWhere_in[tk,i][0]=bindSlotTypeW0
            self.boundedSlotTypeWhere_in[tk,i][1]=bindSlotTypeW1
            return True
        else:
            return False

    def addBoundedSlotPerson(self,bindSlotP,bindSlotP0,bindSlotP1,tk,i):
        bindSlotlocal=bindSlotP
        if not(self.existBoundedSlotPerson(bindSlotP0,bindSlotP1,tk,i)):
            # print "WOOW1!!, This slot added to Slot Person,itk,i",bindSlotP0,bindSlotP1,tk,i
            self.boundedSlotPerson[tk,i]=bindSlotlocal
            self.boundedSlotPerson[tk,i][0]=bindSlotP0
            self.boundedSlotPerson[tk,i][1]=bindSlotP1
            return True
        else:
            return False


    def addBoundedInstance(self,bindInstance,tk,i):
        if not(self.existBoundedInstance(bindInstance,tk,i)):
            self.boundedInstance[tk,i]=bindInstance
            self.boundedInstance[tk,i][0]=bindInstance[0]
            self.boundedInstance[tk,i][1]=bindInstance[1]
            self.boundedInstance[tk,i][2]=bindInstance[2]
            return True
        else:
            return False


    def addBoundedInstanceAction(self,bindInstanceAction,tk,i):
        if not(self.existBoundedInstanceAction(bindInstanceAction,tk,i)):
            self.boundedInstanceAction[tk,i]=bindInstanceAction
            self.boundedInstanceAction[tk,i][0]=bindInstanceAction[0]
            self.boundedInstanceAction[tk,i][1]=bindInstanceAction[1]
            self.boundedInstanceAction[tk,i][2]=bindInstanceAction[2]
            return True
        else:
            return False


    def addBoundedInstanceAnswer(self,bindInstanceAnswer,tk,i):
        if not(self.existBoundedInstanceAnswer(bindInstanceAnswer,tk,i)):
            self.boundedInstanceAnswer[tk,i]=bindInstanceAnswer
            self.boundedInstanceAnswer[tk,i][0]=bindInstanceAnswer[0]
            self.boundedInstanceAnswer[tk,i][1]=bindInstanceAnswer[1]
            self.boundedInstanceAnswer[tk,i][2]=bindInstanceAnswer[2]
            self.boundedInstanceAnswer[tk,i][3]=bindInstanceAnswer[3]
            return True
        else:
            return False


    def addBoundedExactInstanceAnswer(self,bindExactInstAnswer,tk,i):
        if not(self.existBoundedExactInstanceAnswer(bindExactInstAnswer,tk,i)):
            self.boundedExactInstanceAnswer[tk,i]=bindExactInstAnswer
            self.boundedExactInstanceAnswer[tk,i][0]=bindExactInstAnswer[0]
            self.boundedExactInstanceAnswer[tk,i][1]=bindExactInstAnswer[1]
            self.boundedExactInstanceAnswer[tk,i][2]=bindExactInstAnswer[2]
            self.boundedExactInstanceAnswer[tk,i][3]=bindExactInstAnswer[3]

            return True
        else:
            return False


    def addBoundedExactAnswer(self,bindExactAnswer,tk,i):
        if not(self.existBoundedExactAnswer(bindExactAnswer,tk,i)):
            self.boundedExactAnswer[tk,i]=bindExactAnswer
            self.boundedExactAnswer[tk,i][0]=bindExactAnswer[0]
            self.boundedExactAnswer[tk,i][1]=bindExactAnswer[1]
            self.boundedExactAnswer[tk,i][2]=bindExactAnswer[2]
            return True
        else:
            return False


    def addBoundedInstanceWhere(self,bindInstanceW,tk,i):
        if not(self.existBoundedInstanceWhere(bindInstanceW,tk,i)):
            self.boundedInstanceWhere[tk,i]=bindInstanceW
            self.boundedInstanceWhere[tk,i][0]=bindInstanceW[0]
            self.boundedInstanceWhere[tk,i][1]=bindInstanceW[1]
            self.boundedInstanceWhere[tk,i][2]=bindInstanceW[2]
            return True
        else:
            return False

    def addBoundedInstanceWho(self,bindInstanceW,tk,i):
        if not(self.existBoundedInstanceWho(bindInstanceW,tk,i)):
            self.boundedInstanceWho[tk,i]=bindInstanceW
            self.boundedInstanceWho[tk,i][0]=bindInstanceW[0]
            self.boundedInstanceWho[tk,i][1]=bindInstanceW[1]
            self.boundedInstanceWho[tk,i][2]=bindInstanceW[2]
            return True
        else:
            return False


    def addBoundedInstanceWhen(self,bindInstanceW,tk,i):
        print "Called addBoundedInstanceWhen:",bindInstanceW
        if not(self.existBoundedInstanceWhen(bindInstanceW,tk,i)):
            self.boundedInstanceWhen[tk,i]=bindInstanceW
            self.boundedInstanceWhen[tk,i][0]=bindInstanceW[0]
            self.boundedInstanceWhen[tk,i][1]=bindInstanceW[1]
            self.boundedInstanceWhen[tk,i][2]=bindInstanceW[2]
            return True
        else:
            return False


    def addBoundedInstanceWhat(self,bindInstanceW,tk,i):
        if not(self.existBoundedInstanceWhat(bindInstanceW,tk,i)):
            self.boundedInstanceWhat[tk,i]=bindInstanceW
            self.boundedInstanceWhat[tk,i][0]=bindInstanceW[0]
            self.boundedInstanceWhat[tk,i][1]=bindInstanceW[1]
            self.boundedInstanceWhat[tk,i][2]=bindInstanceW[2]
            return True
        else:
            return False


    def addBoundedInstancePerson(self,bindInstanceP,tk,i):
        if not(self.existBoundedInstancePerson(bindInstanceP,tk,i)):
            self.boundedInstancePerson[tk,i]=bindInstanceP
            self.boundedInstancePerson[tk,i][0]=bindInstanceP[0]
            self.boundedInstancePerson[tk,i][1]=bindInstanceP[1]
            self.boundedInstancePerson[tk,i][2]=bindInstanceP[2]
            return True
        else:
            return False

    def addBoundedInstanceMemb(self,bindInstanceMemb,tk,i):
        if not(self.existBoundedInstanceMemb(bindInstanceMemb,tk,i)):
            self.boundedInstanceMemb[tk,i]=bindInstanceMemb
            self.boundedInstanceMemb[tk,i][0]=bindInstanceMemb[0]
            self.boundedInstanceMemb[tk,i][1]=bindInstanceMemb[1]
            self.boundedInstanceMemb[tk,i][2]=bindInstanceMemb[2]
            return True
        else:
            return False


    def addBoundedInstanceStatus(self,bindInstanceStatus,tk,i):
        if not(self.existBoundedInstanceStatus(bindInstanceStatus,tk,i)):
            self.boundedInstanceStatus[tk,i]=bindInstanceStatus
            self.boundedInstanceStatus[tk,i][0]=bindInstanceStatus[0]
            self.boundedInstanceStatus[tk,i][1]=bindInstanceStatus[1]
            self.boundedInstanceStatus[tk,i][2]=bindInstanceStatus[2]
            return True
        else:
            return False


    def addBoundedInstanceCmpProp(self,bindInstanceCmpProp,tk,i):
        if not(self.existBoundedInstanceCmpProp(bindInstanceCmpProp,tk,i)):
            self.boundedInstanceCmpProp[tk,i]=bindInstanceCmpProp
            self.boundedInstanceCmpProp[tk,i][0]=bindInstanceCmpProp[0]
            self.boundedInstanceCmpProp[tk,i][1]=bindInstanceCmpProp[1]
            self.boundedInstanceCmpProp[tk,i][2]=bindInstanceCmpProp[2]
            return True
        else:
            return False


    def addBoundedInstanceEnt(self,bindInstanceEnt,tk,i):
        if not(self.existBoundedInstanceEnt(bindInstanceEnt,tk,i)):
            self.boundedInstanceEnt[tk,i]=bindInstanceEnt
            self.boundedInstanceEnt[tk,i][0]=bindInstanceEnt[0]
            self.boundedInstanceEnt[tk,i][1]=bindInstanceEnt[1]
            self.boundedInstanceEnt[tk,i][2]=bindInstanceEnt[2]
            return True
        else:
            return False


    def addBoundedInstanceHowmuch(self,bindInstanceW,tk,i):
        if not(self.existBoundedInstanceHowmuch(bindInstanceW,tk,i)):
            self.boundedInstanceHowmuch[tk,i]=bindInstanceW
            self.boundedInstanceHowmuch[tk,i][0]=bindInstanceW[0]
            self.boundedInstanceHowmuch[tk,i][1]=bindInstanceW[1]
            self.boundedInstanceHowmuch[tk,i][2]=bindInstanceW[2]
            return True
        else:
            return False


    def removeFilesContent(self):
        path=self.workingDir + "graphsentence/"
        fileConst=open(path + "constraintGraph.txt", 'w')
        fileGen=open(path + "generalGraph.txt", 'w')
        fileMerge=open(path + "mergePrologGraph.txt", 'w')
        fileConst.close()
        # fileGen.close()
        fileMerge.close()

    def removeAllIndicators(self):
        # print "Content of Indicator before",self.tk_indicators
        lnIdx=len(self.tk_indicators)
        i=0
        while i<lnIdx:
            self.tk_indicators.pop()
            i=i+1
            # self.tk_indicators.remove(x)
        # print "Content of Indicator",self.tk_indicators

    def clearAllVariables(self):
        for key in self.boundedVars.keys():
            del self.boundedVars[key]

    def existBoundedVars(self,ex_item,ex_bindVar):

        Flag=0
        for bndvars in self.boundedVars:
            if str(bndvars)==str(ex_item):
                # print "was Found var for self.boundedVars[bndvars],str(ex_bindVar),ex_bindVar,bndvars, ex_item ",self.boundedVars[bndvars],str(ex_bindVar),bndvars,ex_item
                Flag=1
        if Flag==1:
            return True
        else:
            return False

    def existBoundedClass(self,ex_bindClass,tk,i):
        print "existBoundedClass,tk , idxClass",tk
        digtkClass=removeAlphabetfromIdx(tk)
        Flag=0
        for bndcls in self.boundedClass:
            digbndClass=removeAlphabetfromIdx(bndcls[0])
            if str(self.boundedClass[bndcls])==str(ex_bindClass):
                print "was Found class for digtkClass , self.boundedClass[bndcls],str(bindClass[0]),bindClass,bndcls,i ",digtkClass,self.boundedClass[bndcls],str(ex_bindClass),ex_bindClass,bndcls,i
                if int(digbndClass)==int(digtkClass):
                    Flag=1
                    print "Exist also Alphabet , tk, bndcls", tk, bndcls[0]
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassItem(self,ex_bindClassItem0,tk,i):

        Flag=0
        for bndcls in self.boundedClassItem:
            if str(self.boundedClassItem[bndcls])==str(ex_bindClassItem0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassAction(self,ex_bindClassAction0,tk,i):

        Flag=0
        for bndcls in self.boundedClassAction:
            if str(self.boundedClassAction[bndcls])==str(ex_bindClassAction0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False

    def existBoundedClassAnswer(self,ex_bindClassAnswer0,tk,i):

        Flag=0
        for bndcls in self.boundedClassAnswer:
            if str(self.boundedClassAnswer[bndcls])==str(ex_bindClassAnswer0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False

    def existBoundedClassWhere(self,ex_bindClassW0,tk,i):

        Flag=0
        for bndcls in self.boundedClassWhere:
            if str(self.boundedClassWhere[bndcls])==str(ex_bindClassW0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False

    def existBoundedClassWho(self,ex_bindClassW0,tk,i):

        Flag=0
        for bndcls in self.boundedClassWho:
            if str(self.boundedClassWho[bndcls])==str(ex_bindClassW0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassWhen(self,ex_bindClassW0,tk,i):

        Flag=0
        for bndcls in self.boundedClassWhen:
            if str(self.boundedClassWhen[bndcls])==str(ex_bindClassW0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassWhat(self,ex_bindClassW0,tk,i):

        Flag=0
        for bndcls in self.boundedClassWhat:
            if str(self.boundedClassWhat[bndcls])==str(ex_bindClassW0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassHowmuch(self,ex_bindClassHM0,tk,i):

        Flag=0
        for bndcls in self.boundedClassHowmuch:
            if str(self.boundedClassHowmuch[bndcls])==str(ex_bindClassHM0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassPerson(self,ex_bindClassP0,tk,i):

        Flag=0
        for bndcls in self.boundedClassPerson:
            if str(self.boundedClassPerson[bndcls])==str(ex_bindClassP0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False

    def existBoundedClassMemb(self,ex_bindClassMemb0,tk,i):

        Flag=0
        for bndcls in self.boundedClassMemb:
            if str(self.boundedClassMemb[bndcls])==str(ex_bindClassMemb0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassStatus(self,ex_bindClassStatus0,tk,i):

        Flag=0
        for bndcls in self.boundedClassStatus:
            if str(self.boundedClassStatus[bndcls])==str(ex_bindClassStatus0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassCmpProp(self,ex_bindClassCmpProp0,tk,i):

        Flag=0
        for bndcls in self.boundedClassCmpProp:
            if str(self.boundedClassCmpProp[bndcls])==str(ex_bindClassCmpProp0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedClassEnt(self,ex_bindClassEnt0,tk,i):

        Flag=0
        for bndcls in self.boundedClassEnt:
            if str(self.boundedClassEnt[bndcls])==str(ex_bindClassEnt0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedSubClass(self,ex_bindSubClass,tk,i):
        Flag=0
        for bndsubclsi,bndsubclsj in self.boundedSubClass:
            if str(self.boundedSubClass[bndsubclsi,bndsubclsj][0])==str(ex_bindSubClass[0]) and str(self.boundedSubClass[bndsubclsi,bndsubclsj][1])==str(ex_bindSubClass[1]) and tk:
                Flag=1
            elif tk==bndsubclsi and i==bndsubclsj:
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedSubClassWhere_in(self,ex_bindSubClassW0,ex_bindSubClassW1,tk,i):
        Flag=0
        # print "bindSubClass has sent is argument for j!!==Null",ex_bindSubClassW0,ex_bindSubClassW1,self.boundedSubClassWhere_in.viewitems()

        for bndsubclsi,bndsubclsj in self.boundedSubClassWhere_in:
            if str(self.boundedSubClassWhere_in[bndsubclsi,bndsubclsj][0])==str(ex_bindSubClassW0) and str(self.boundedSubClassWhere_in[bndsubclsi,bndsubclsj][1])==str(ex_bindSubClassW1) and tk:
                Flag=1
            elif tk==bndsubclsi and i==bndsubclsj:
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSubClassWho(self,ex_bindSubClassW0,ex_bindSubClassW1,tk,i):
        Flag=0
        # print "bindSubClass has sent is argument for j!!==Null",ex_bindSubClassW0,ex_bindSubClassW1,self.boundedSubClassWhere_in.viewitems()

        for bndsubclsi,bndsubclsj in self.boundedSubClassWho:
            if str(self.boundedSubClassWho[bndsubclsi,bndsubclsj][0])==str(ex_bindSubClassW0) and str(self.boundedSubClassWho[bndsubclsi,bndsubclsj][1])==str(ex_bindSubClassW1) and tk:
                Flag=1
            elif tk==bndsubclsi and i==bndsubclsj:
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSubClassPerson(self,ex_bindSubClassP0,ex_bindSubClassP1,tk,i):
        Flag=0
        # print "bindSubClass has sent is argument for j!!==Null",ex_bindSubClassP0,ex_bindSubClassP1,self.boundedSubClassPerson.viewitems()

        for bndsubclsi,bndsubclsj in self.boundedSubClassPerson:
            if str(self.boundedSubClassPerson[bndsubclsi,bndsubclsj][0])==str(ex_bindSubClassP0) and str(self.boundedSubClassPerson[bndsubclsi,bndsubclsj][1])==str(ex_bindSubClassP1) and tk:

                Flag=1
            elif tk==bndsubclsi and i==bndsubclsj:
                # print "Wow Index Founded In subclass!!!, last ex_bindSubClass",tk,i, self.boundedSubClass[bndsubclsi,bndsubclsj],ex_bindSubClassW
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlot(self,ex_bindSlot,tk,i):
        Flag=0
        for bndsloti,bndslotj in self.boundedSlot:
            if str(self.boundedSlot[bndsloti,bndslotj][0])==str(ex_bindSlot[0]) and str(self.boundedSlot[bndsloti,bndslotj][1])==str(ex_bindSlot[1]):
                Flag=1
            elif tk==bndsloti and i==bndslotj:
                # print "Wow Index Founded In Slot!!!, last ex_bindSubClass",tk,i, self.boundedSubClass[bndsloti,bndslotj],ex_bindSlot
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlot4Class(self,ex_bindSlot4Class0,ex_bindSlot4Class1,tk,i):
        Flag=0
        for bndsloti,bndslotj in self.boundedSlot4Class:
            if str(self.boundedSlot4Class[bndsloti,bndslotj][0])==str(ex_bindSlot4Class0) and str(self.boundedSlot4Class[bndsloti,bndslotj][1])==str(ex_bindSlot4Class1):
                Flag=1
            elif tk==bndsloti and i==bndslotj:
                # print "Wow Index Founded In Slot!!!, last ex_bindSubClass",tk,i, self.boundedSubClass[bndsloti,bndslotj],ex_bindSlot4Class0
                Flag=1

        if Flag==1:
            return True
        else:
            return False



    def existBoundedExactSlotAnswer(self,bindExSlotAnswer0,bindExSlotAnswer1,tk,i):
        Flag=0
        for bndsloti in self.boundedExactSlotAnswer:
            if str(self.boundedExactSlotAnswer[bndsloti][0])==str(bindExSlotAnswer0) and str(self.boundedExactSlotAnswer[bndsloti][1])==str(bindExSlotAnswer1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotItem(self,bindSlotItem0,bindSlotItem1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotItem:
            if str(self.boundedSlotItem[bndsloti][0])==str(bindSlotItem0) and str(self.boundedSlotItem[bndsloti][1])==str(bindSlotItem1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotAction(self,bindSlotAction0,bindSlotAction1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotAction:
            if str(self.boundedSlotAction[bndsloti][0])==str(bindSlotAction0) and str(self.boundedSlotAction[bndsloti][1])==str(bindSlotAction1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotAnswer(self,bindSlotAnswer0,bindSlotAnswer1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotAnswer:
            if str(self.boundedSlotAnswer[bndsloti][0])==str(bindSlotAnswer0) and str(self.boundedSlotAnswer[bndsloti][1])==str(bindSlotAnswer1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotWhere(self,bindSlotW0,bindSlotW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotWhere:
            if str(self.boundedSlotWhere[bndsloti][0])==str(bindSlotW0) and str(self.boundedSlotWhere[bndsloti][1])==str(bindSlotW1):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeWhere(self,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeWhere:
            if str(self.boundedSlotTypeWhere[bndsloti][0])==str(bindSlotTypeW0) and str(self.boundedSlotTypeWhere[bndsloti][1])==str(bindSlotTypeW1):
                Flag=1
        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeWhere_in(self,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeWhere_in:
            if str(self.boundedSlotTypeWhere_in[bndsloti][0])==str(bindSlotTypeW0) and str(self.boundedSlotTypeWhere_in[bndsloti][1])==str(bindSlotTypeW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedSlotWho(self,bindSlotW0,bindSlotW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotWho:
            if str(self.boundedSlotWho[bndsloti][0])==str(bindSlotW0) and str(self.boundedSlotWho[bndsloti][1])==str(bindSlotW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotWhen(self,bindSlotW0,bindSlotW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotWhen:
            if str(self.boundedSlotWhen[bndsloti][0])==str(bindSlotW0) and str(self.boundedSlotWhen[bndsloti][1])==str(bindSlotW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotHowmuch(self,bindSlotHM0,bindSlotHM1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotHowmuch:
            if str(self.boundedSlotHowmuch[bndsloti][0])==str(bindSlotHM0) and str(self.boundedSlotHowmuch[bndsloti][1])==str(bindSlotHM1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotWhat(self,bindSlotW0,bindSlotW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotWhat:
            if str(self.boundedSlotWhat[bndsloti][0])==str(bindSlotW0) and str(self.boundedSlotWhat[bndsloti][1])==str(bindSlotW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotMemb(self,bindSlotMemb0,bindSlotMemb1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotMemb:
            if str(self.boundedSlotMemb[bndsloti][0])==str(bindSlotMemb0) and str(self.boundedSlotMemb[bndsloti][1])==str(bindSlotMemb1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotStatus(self,bindSlotStatus0,bindSlotStatus1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotStatus:
            if str(self.boundedSlotStatus[bndsloti][0])==str(bindSlotStatus0) and str(self.boundedSlotStatus[bndsloti][1])==str(bindSlotStatus1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotCmpProp(self,bindSlotCmpProp0,bindSlotCmpProp1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotCmpProp:
            if str(self.boundedSlotCmpProp[bndsloti][0])==str(bindSlotCmpProp0) and str(self.boundedSlotCmpProp[bndsloti][1])==str(bindSlotCmpProp1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedSlotEnt(self,bindSlotEnt0,bindSlotEnt1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotEnt:
            if str(self.boundedSlotEnt[bndsloti][0])==str(bindSlotEnt0) and str(self.boundedSlotEnt[bndsloti][1])==str(bindSlotEnt1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeAction(self,bindSlotTypeAction0,bindSlotTypeAction1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeAction:
            if str(self.boundedSlotTypeAction[bndsloti][0])==str(bindSlotTypeAction0) and str(self.boundedSlotTypeAction[bndsloti][1])==str(bindSlotTypeAction1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeAnswer(self,bindSlotTypeAnswer0,bindSlotTypeAnswer1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeAnswer:
            if str(self.boundedSlotTypeAnswer[bndsloti][0])==str(bindSlotTypeAnswer0) and str(self.boundedSlotTypeAnswer[bndsloti][1])==str(bindSlotTypeAnswer1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedSlotTypeEnt(self,bindSlotTypeEnt0,bindSlotTypeEnt1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeEnt:
            if str(self.boundedSlotTypeEnt[bndsloti][0])==str(bindSlotTypeEnt0) and str(self.boundedSlotTypeEnt[bndsloti][1])==str(bindSlotTypeEnt1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeMemb(self,bindSlotTypeMemb0,bindSlotTypeMemb1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeMemb:
            if str(self.boundedSlotTypeMemb[bndsloti][0])==str(bindSlotTypeMemb0) and str(self.boundedSlotTypeMemb[bndsloti][1])==str(bindSlotTypeMemb1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeStatus(self,bindSlotTypeStatus0,bindSlotTypeStatus1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeStatus:
            if str(self.boundedSlotTypeStatus[bndsloti][0])==str(bindSlotTypeStatus0) and str(self.boundedSlotTypeStatus[bndsloti][1])==str(bindSlotTypeStatus1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeCmpProp(self,bindSlotTypeCmpProp0,bindSlotTypeCmpProp1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeCmpProp:
            if str(self.boundedSlotTypeCmpProp[bndsloti][0])==str(bindSlotTypeCmpProp0) and str(self.boundedSlotTypeCmpProp[bndsloti][1])==str(bindSlotTypeCmpProp1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypePerson(self,bindSlotTypePer0,bindSlotTypePer1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypePerson:
            if str(self.boundedSlotTypePerson[bndsloti][0])==str(bindSlotTypePer0) and str(self.boundedSlotTypePerson[bndsloti][1])==str(bindSlotTypePer1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeWho(self,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeWho:
            if str(self.boundedSlotTypeWho[bndsloti][0])==str(bindSlotTypeW0) and str(self.boundedSlotTypeWho[bndsloti][1])==str(bindSlotTypeW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeWhen(self,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeWhen:
            if str(self.boundedSlotTypeWhen[bndsloti][0])==str(bindSlotTypeW0) and str(self.boundedSlotTypeWhen[bndsloti][1])==str(bindSlotTypeW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeWhat(self,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeWhat:
            if str(self.boundedSlotTypeWhat[bndsloti][0])==str(bindSlotTypeW0) and str(self.boundedSlotTypeWhat[bndsloti][1])==str(bindSlotTypeW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotPerson(self,bindSlotP0,bindSlotP1,tk,i):
        Flag=0
        # print "bindSlot has sent is argument :",bindSlotP0,bindSlotP1,self.boundedSlotPerson

        for bndsloti in self.boundedSlotPerson:
            # print "bounded[bndsloti,bndslotj] keys",self.boundedSlotPerson.keys()
            # print "Index bndsloti,bndslotj, for tk,i",bndsloti,tk,i
            if str(self.boundedSlotPerson[bndsloti][0])==str(bindSlotP0) and str(self.boundedSlotPerson[bndsloti][1])==str(bindSlotP1):
                # print "was Found Slot : ", self.boundedSlotPerson[bndsloti][0],self.boundedSlotPerson[bndsloti][1]
                # print "has sent Slot bindSlot: ", str(bindSlotP0),str(bindSlotP1)

                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedSlotTypeHowmuch(self,bindSlotTypeW0,bindSlotTypeW1,tk,i):
        Flag=0
        for bndsloti in self.boundedSlotTypeHowmuch:
            if str(self.boundedSlotTypeHowmuch[bndsloti][0])==str(bindSlotTypeW0) and str(self.boundedSlotTypeHowmuch[bndsloti][1])==str(bindSlotTypeW1):
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedInstance(self,bindInstance,tk,i):
        Flag=0
        # print "bindInstance has sent is argument :",bindInstance,self.boundedInstance

        for bndinstancei,bndinstancej in self.boundedInstance:
            # print "bounded[bndinstancei,bndinstancej] keys",self.boundedInstance.keys()
            # print "Index bndinstancei,bndinstancej, for tk,i",bndinstancei,bndinstancej,tk,i
            if str(self.boundedInstance[bndinstancei,bndinstancej][0])==str(bindInstance[0]) and str(self.boundedInstance[bndinstancei,bndinstancej][1])==str(bindInstance[1]) and str(self.boundedInstance[bndinstancei,bndinstancej][2])==str(bindInstance[2]):
                # print "was Found Instance : ", self.boundedInstance[bndinstancei,bndinstancej][0],self.boundedInstance[bndinstancei,bndinstancej][1],self.boundedInstance[bndinstancei,bndinstancej][2]
                # print "has sent Instance bindInstance: ", str(bindInstance[0]),str(bindInstance[1]),str(bindInstance[2])

                Flag=1

        if Flag==1:
            return True
        else:
            return False



    def existBoundedInstanceAction(self,bindInstanceAction,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceAction:
            if str(self.boundedInstanceAction[bndinstancei,bndinstancej][0])==str(bindInstanceAction[0]) and str(self.boundedInstanceAction[bndinstancei,bndinstancej][1])==str(bindInstanceAction[1]) and str(self.boundedInstanceAction[bndinstancei,bndinstancej][2])==str(bindInstanceAction[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceAnswer(self,bindInstanceAnswer,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceAnswer:
            if str(self.boundedInstanceAnswer[bndinstancei,bndinstancej][0])==str(bindInstanceAnswer[0]) and str(self.boundedInstanceAnswer[bndinstancei,bndinstancej][1])==str(bindInstanceAnswer[1]) and str(self.boundedInstanceAnswer[bndinstancei,bndinstancej][2])==str(bindInstanceAnswer[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedExactInstanceAnswer(self,bindExactInstAnswer,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedExactInstanceAnswer:
            if str(self.boundedExactInstanceAnswer[bndinstancei,bndinstancej][0])==str(bindExactInstAnswer[0]) and str(self.boundedExactInstanceAnswer[bndinstancei,bndinstancej][1])==str(bindExactInstAnswer[1]) and str(self.boundedExactInstanceAnswer[bndinstancei,bndinstancej][2])==str(bindExactInstAnswer[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedExactAnswer(self,bindExactAnswer,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedExactAnswer:
            if str(self.boundedExactAnswer[bndinstancei,bndinstancej][0])==str(bindExactAnswer[0]) and str(self.boundedExactAnswer[bndinstancei,bndinstancej][1])==str(bindExactAnswer[1]) and str(self.boundedExactAnswer[bndinstancei,bndinstancej][2])==str(bindExactAnswer[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceWhere(self,bindInstanceW,tk,i):
        Flag=0
        # print "bindInstance has sent is argument :",bindInstanceW,self.boundedInstanceWhere_in
        for bndinstancei,bndinstancej in self.boundedInstanceWhere:
            # print "bounded[bndinstancei,bndinstancej] keys",self.boundedInstanceWhere_in.keys()
            # print "Index bndinstancei,bndinstancej, for tk,i",bndinstancei,bndinstancej,tk,i
            if str(self.boundedInstanceWhere[bndinstancei,bndinstancej][0])==str(bindInstanceW[0]) and str(self.boundedInstanceWhere[bndinstancei,bndinstancej][1])==str(bindInstanceW[1]) and str(self.boundedInstanceWhere[bndinstancei,bndinstancej][2])==str(bindInstanceW[2]):
                # print "was Found Instance : ", self.boundedInstanceWhere_in[bndinstancei,bndinstancej][0],self.boundedInstanceWhere_in[bndinstancei,bndinstancej][1],self.boundedInstanceWhere_in[bndinstancei,bndinstancej][2]
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedInstanceWho(self,bindInstanceW,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceWho:
            if str(self.boundedInstanceWho[bndinstancei,bndinstancej][0])==str(bindInstanceW[0]) and str(self.boundedInstanceWho[bndinstancei,bndinstancej][1])==str(bindInstanceW[1]) and str(self.boundedInstanceWho[bndinstancei,bndinstancej][2])==str(bindInstanceW[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceWhen(self,bindInstanceW,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceWhen:
            if str(self.boundedInstanceWhen[bndinstancei,bndinstancej][0])==str(bindInstanceW[0]) and str(self.boundedInstanceWhen[bndinstancei,bndinstancej][1])==str(bindInstanceW[1]) and str(self.boundedInstanceWhen[bndinstancei,bndinstancej][2])==str(bindInstanceW[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceWhat(self,bindInstanceW,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceWhat:
            if str(self.boundedInstanceWhat[bndinstancei,bndinstancej][0])==str(bindInstanceW[0]) and str(self.boundedInstanceWhat[bndinstancei,bndinstancej][1])==str(bindInstanceW[1]) and str(self.boundedInstanceWhat[bndinstancei,bndinstancej][2])==str(bindInstanceW[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceMemb(self,bindInstanceMemb,tk,i):
        Flag=0
        # print "bindInstance has sent is argument :",bindInstanceW,self.boundedInstanceWhere_in
        for bndinstancei,bndinstancej in self.boundedInstanceMemb:
            if str(self.boundedInstanceMemb[bndinstancei,bndinstancej][0])==str(bindInstanceMemb[0]) and str(self.boundedInstanceMemb[bndinstancei,bndinstancej][1])==str(bindInstanceMemb[1]) and str(self.boundedInstanceMemb[bndinstancei,bndinstancej][2])==str(bindInstanceMemb[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceStatus(self,bindInstanceStatus,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceStatus:
            if str(self.boundedInstanceStatus[bndinstancei,bndinstancej][0])==str(bindInstanceStatus[0]) and str(self.boundedInstanceStatus[bndinstancei,bndinstancej][1])==str(bindInstanceStatus[1]) and str(self.boundedInstanceStatus[bndinstancei,bndinstancej][2])==str(bindInstanceStatus[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceCmpProp(self,bindInstanceCmpProp,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceCmpProp:
            if str(self.boundedInstanceCmpProp[bndinstancei,bndinstancej][0])==str(bindInstanceCmpProp[0]) and str(self.boundedInstanceCmpProp[bndinstancei,bndinstancej][1])==str(bindInstanceCmpProp[1]) and str(self.boundedInstanceCmpProp[bndinstancei,bndinstancej][2])==str(bindInstanceCmpProp[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def existBoundedInstanceEnt(self,bindInstanceEnt,tk,i):
        Flag=0
        # print "bindInstance has sent is argument :",bindInstanceW,self.boundedInstanceWhere_in
        for bndinstancei,bndinstancej in self.boundedInstanceEnt:
            if str(self.boundedInstanceEnt[bndinstancei,bndinstancej][0])==str(bindInstanceEnt[0]) and str(self.boundedInstanceEnt[bndinstancei,bndinstancej][1])==str(bindInstanceEnt[1]) and str(self.boundedInstanceEnt[bndinstancei,bndinstancej][2])==str(bindInstanceEnt[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False

    def existBoundedInstancePerson(self,bindInstanceP,tk,i):
        Flag=0
        # print "bindInstance has sent is argument :",bindInstanceP,self.boundedInstancePerson

        for bndinstancei,bndinstancej in self.boundedInstancePerson:
            # print "bounded[bndinstancei,bndinstancej] keys",self.boundedInstancePerson.keys()
            # print "Index bndinstancei,bndinstancej, for tk,i",bndinstancei,bndinstancej,tk,i
            if str(self.boundedInstancePerson[bndinstancei,bndinstancej][0])==str(bindInstanceP[0]) and str(self.boundedInstancePerson[bndinstancei,bndinstancej][1])==str(bindInstanceP[1]) and str(self.boundedInstancePerson[bndinstancei,bndinstancej][2])==str(bindInstanceP[2]):
                # print "was Found Instance : ", self.boundedInstancePerson[bndinstancei,bndinstancej][0],self.boundedInstancePerson[bndinstancei,bndinstancej][1],self.boundedInstancePerson[bndinstancei,bndinstancej][2]
                # print "has sent Instance bindInstance: ", str(bindInstanceP[0]),str(bindInstanceP[1]),str(bindInstanceP[2])

                Flag=1
        if Flag==1:
            return True
        else:
            return False

    def existBoundedInstanceHowmuch(self,bindInstanceW,tk,i):
        Flag=0
        for bndinstancei,bndinstancej in self.boundedInstanceHowmuch:
            if str(self.boundedInstanceHowmuch[bndinstancei,bndinstancej][0])==str(bindInstanceW[0]) and str(self.boundedInstanceHowmuch[bndinstancei,bndinstancej][1])==str(bindInstanceW[1]) and str(self.boundedInstanceHowmuch[bndinstancei,bndinstancej][2])==str(bindInstanceW[2]):
                Flag=1

        if Flag==1:
            return True
        else:
            return False


    def executeConditions(self,con1,con2):
        i=0
        for c in self.conds:
            if not c.execute(con1,con2):
                return False

        return True

    def executeActions(self,act1,act2):
        for a in self.actions:
            a.execute(act1,act2)
        return (self.type, self.boundedVars)


    def describe(self):
        print 'ID : ', self.id
        print 'Result', self.type
        print len(self.conds), 'Conditions'
        for c in self.conds:
            c.describe()
        print len(self.a), 'Actions'
        for a in self.actions:
            a.describe()

    def describeBoundedOntology(self):
        print 'ID : ', self.id
        print 'Result', self.type
        print len(self.conds), 'Conditions'
        print "Bounded Class after looking in ontology is:","\n"
        for cls in self.boundedClass:
            print "\t",cls,"\t",self.boundedClass[cls]

        print "Bounded Sub Class after looking in ontology is:","\n"
        for subcls in self.boundedSubClass:
            print "\t",subcls,"\t",self.boundedSubClass[subcls][0],self.boundedSubClass[subcls][1]

        print "Bounded SLOT after looking in ontology is:","\n"
        for slot in self.boundedSlot:
            print "\t",slot,"\t", self.boundedSlot[slot][0],self.boundedSlot[slot][1]

        print "Bounded INSTANCE after looking in ontology is:","\n"
        for ins in self.boundedInstance:
            print "\t",ins,"\t", self.boundedInstance[ins]


        # self.boundedSlotTuple=()
        # self.boundedInstance={}
        # self.boundedClassInstance={}



class QTclasscondition(object):

    def __init__(self, id, condition):
        self._init_vars(id, condition)

    def _init_vars(self, id, condition):
        self.id=id
        self.condition=condition

    def execute(self,s,r):
        return eval(self.condition)

    def describe(self):
        print self.id, '\t',self.condition

class QTclassAction(object):

    def __init__(self, id, action):
        self._init_vars(id, action)

    def _init_vars(self, id, action):
        self.id=id
        self.action=action

    def execute(self,s,r):
        return eval(self.action)

    def describe(self):
        print self.id, '\t',self.action

##functions
# currentRule=QTclassrule('','')

def removeAlphabetfromIdx(alIdx):
    strIdx=str(alIdx)
    itemstrp1=strIdx.strip('C')
    itemstrp1=itemstrp1.strip('C')
    itemstrp1=itemstrp1.strip('S')
    itemstrp1=itemstrp1.strip('C')
    item=itemstrp1.strip('I')
    # print "Remove alphabet :", item
    digItem=int(item)
    return digItem

def removeNumberfromIdx(alIdx):
    strIdx=str(alIdx)
    print "alIdx",alIdx
    numberStrip=""
    itemstrp1=strIdx.strip('C')
    itemstrp1=itemstrp1.strip('C')
    itemstrp1=itemstrp1.strip('S')
    itemstrp1=itemstrp1.strip('C')
    itemstrp1=itemstrp1.strip('I')

    numberStrip=strIdx.rstrip(itemstrp1)

    print "Remove Number from IDX :", numberStrip
    strItem=str(numberStrip)
    return strItem

def removeListA_listB(lista,listb):
    for item in lista:
        while listb.count(item)>0:
            listb.remove(item)
            # print "REmove item from listb is ",item, listb
    return listb

def addListA_listB(lista,listb):
    for item in listb:
        while lista.count(item)==0:
            lista.append(item)
    return lista

def removeListItem(listX):
    # print "Content of List before",listX
    lnIdx=len(listX)
    i=0
    while i<lnIdx:
        listX.pop()
        i=i+1
    # print "Content of List",listX
    return listX

def add_tkType_List(r,tk_list,tk_type,ont_type):
    if len(tk_list)==1:
        tkItem=tk_list.pop()
        r.addBoundedVars(tk_type,tkItem)
        r.addBoundedVars(ont_type,None)
        r.addIndicators_tk(tkItem)
    elif len(tk_list)>1:
        r.addBoundedList_Vars(tk_type,tk_list)
        r.addBoundedVars(ont_type,None)
        lnIdx=len(tk_list)
        i=0
        while i<lnIdx:
            r.addIndicators_tk(tk_list.pop())
            i=i+1

def addtk_Type_Indicators(r,tk_list):
    if len(tk_list)==1:
        tkItem=tk_list.pop()
        # print "len(tk_list)==1: function addtk_Type_List of list is", tkItem
        r.addIndicators_tk(tkItem)
    elif len(tk_list)>1:
        # print "len(objList)>1: function addtk_Type_List of list is", tk_list
        lnIdx=len(tk_list)
        i=0
        while i<lnIdx:
            r.addIndicators_tk(tk_list.pop())
            i=i+1
        # print "after add tk_Type r.boundedVars.values()",r.boundedVars,r.boundedVars.values()

def getObj_of_Sentence(s,r):
    listObject=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="pobj" or str(lst_Dep[2])=="pobjpass" or str(lst_Dep[2])=="dobj"):
            listObject.append(lst_Dep[1])
    return listObject

def getNoun_Obj_of_Sentence(s,r,obj):
    listNounObject=[]
    list_Dep=s.sint._dependencies
    # print "Object[0]",obj
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nn" and  str(lst_Dep[0])==str(obj)):
            listNounObject.append(lst_Dep[1])
    # print "listNounObject is :",listNounObject
    return listNounObject

def getAdj_Obj_of_Sentence(s,r,obj):
    listAdjObject=[]
    list_Dep=s.sint._dependencies
    # print "Subject[0]",obj
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="amod" and str(lst_Dep[0])==str(obj):
            listAdjObject.append(lst_Dep[1])
    # print "listAdjective Object is :",listAdjObject
    return listAdjObject

def getConj_and_Obj_of_Sentence(s,r,listAdjObj):
    listConjObject=[]
    list_Dep=s.sint._dependencies

    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="conj_and":
            for item in listAdjObj:
                print "Okk. loop is AND"
                if str(item)==str(lst_Dep[0]):
                    listConjObject.append(lst_Dep[1])
    # print "listConj and Object is :",listConjObject
    return listConjObject


def getSubj_of_Sentence(s,r):
    listSubject=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="agent") :
            listSubject.append(lst_Dep[1])

    return listSubject

def getNoun_Subj_of_Sentence(s,r,subj):
    listNounSubject=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nn" and  str(lst_Dep[0])==str(subj)):
            listNounSubject.append(lst_Dep[1])

    idx=subj
    while idx>0:
       idx=idx-1
       if isNoun(s,idx):
           listNounSubject.append(idx)
       else:
           break
    # print "listNounSubject with noun is :",listNounSubject
    listNounSubject=list(set(listNounSubject))
    return listNounSubject

def getAdj_Subj_of_Sentence(s,r,subj):
    listAdjSubject=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="amod" and str(lst_Dep[0])==str(subj):
            listAdjSubject.append(lst_Dep[1])
    idx=subj
    while idx>0:
       idx=idx-1
       if isAdjective(s,idx):
           listAdjSubject.append(idx)
       else:
           break

    # print "listAdjective Subject with new Adj is :",listAdjSubject
    listAdjSubject=list(set(listAdjSubject))
    return listAdjSubject

def getConj_and_Subj_of_Sentence(s,r,listAdjSubj):
    listConjSubject=[]
    list_Dep=s.sint._dependencies

    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="conj_and":
            for item in listAdjSubj:
                print "Okk. loop is AND"
                if str(item)==str(lst_Dep[0]):
                    listConjSubject.append(lst_Dep[1])
                elif str(item)==str(lst_Dep[1]):
                    listConjSubject.append(lst_Dep[0])

    # print "listConj and Object is :",listConjSubject
    return listConjSubject


def getDuration_of_TR(s,r,itkDur):
    listDur=[]
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    for itk in range(len(tks)):
        if neofTkIs(s,itk,'DUR'):
            for lst_Dep in list_Dep:
                if str(lst_Dep[0])==str(itkDur) and str(itk)==str(lst_Dep[1]):
                    listDur.append(itk)
    return listDur


def makeSubj_List(s,r,subj0):
    listSubj=[]
    listNounSubj=[]
    listAdjSubj=[]
    listConjSubj=[]
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,subj0)
        # print "listSubj,listNounSubj",listSubj,listNounSubj
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,subj0)
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj))
    return listSubj_itkType


def makeObj_List(s,r,obj0):
    listObj=[]
    listNounObj=[]
    listAdjObj=[]
    listConjObj=[]
    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,obj0)
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,obj0)
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    listObj_itkType=list(set(listObj+listNounObj+listAdjObj+listConjObj))
    return listObj_itkType

def makeDetW_List(s,r,det0):
    listObj=[]
    listNounObj=[]
    listAdjObj=[]
    listConjObj=[]
    listObj.append(det0)
    listNounObj=getNoun_Obj_of_Sentence(s,r,det0)
    if len(listNounObj)>0:
        flagNO=1
    listAdjObj=getAdj_Obj_of_Sentence(s,r,det0)
    if len(listAdjObj)>0:
        flagAO=1
        listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
        if len(listConjObj)>0:
            flagCO=1

    listObj_itkType=list(set(listObj+listNounObj+listAdjObj+listConjObj))
    return listObj_itkType


def getVerb_of_Sentence(s,r):
    listVerb=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if ((str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass") and isVerb(s,lst_Dep[0])):
            listVerb.append(lst_Dep[0])
        elif str(lst_Dep[2])=="xsubj":
            for lst_Dep1 in list_Dep:
                if ((str(lst_Dep1[2])=="xcomp") and isVerb(s,lst_Dep1[0])):
                    listVerb.append(lst_Dep1[0])
                    listVerb.append(lst_Dep[0])
    return listVerb

def getVerbAux_of_Sentence(s,r):
    listVerbAux=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if ((str(lst_Dep[2])=="aux" or str(lst_Dep[2])=="auxpass")) and isVerb(s,lst_Dep[1]):
            listVerbAux.append(lst_Dep[1])
    return listVerbAux

def wordofTkIs(s,t,l):
    return s._get_token(t)._word()==l

def lemmaofTkIs(s,t,l):
    return s._get_token(t)._lemma()==l

def neofTkIs(s,t,ne):
    return s._get_token(t)._ne()==ne

def posofTkIs(s,t,p):
    return re.match(p,s._get_token(t)._pos())

def isVerb(s,t):
    return posofTkIs(s,t,'^V.*$')

def isVerbAux(s,t):
    return  posofTkIs(s,t,'MD')


def isVerbAux_Main(s,t):
    return (lemmaofTkIs(s,t,'be') or lemmaofTkIs(s,t,'have') or lemmaofTkIs(s,t,'has') or lemmaofTkIs(s,t,'do'))

def isBeVerb(s,t):
   tks=s._get_tokens()
   if t=="":
       for itk in range(len(tks)):
           if lemmaofTkIs(s,itk,'be'):
               return True
   else:
       if lemmaofTkIs(s,t,'be'):
           return True

   return False

def isNoun(s,t):
    return posofTkIs(s,t,'^N.*$')

def isAdjective(s,t):
    if lemmaofTkIs(s,t,'run') and wordofTkIs(s,t,'running'):
        return True
    return posofTkIs(s,t,'^J.*$')

def isAdverb(s,t):
    return posofTkIs(s,t,'^R.*$')

def isWhere(s,r,tk):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    listSubjGEO_itkType=[]
    listObjGEO_itkType=[]
    listObj_det_itkType=[]
    listWhereIn_itkType=[]

    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagOd=0
    flagOo=0
    flag_in=0

    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        print "listSubj,listNounSubj",listSubj,listNounSubj
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_in":
            itkLoc=lst_Dep[1]
            flag_in=1
            listWhereIn_itkType=list(set(makeDetW_List(s,r,itkLoc)))
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass") and isGEO_tk(s,r,lst_Dep[1]):
            itkSubj=lst_Dep[1]
            flagSs=1
            listSubjGEO_itkType=list(set(makeSubj_List(s,r,itkSubj)))
        if (str(lst_Dep[2])=="pobj" or str(lst_Dep[2])=="pobjpass") and isGEO_tk(s,r,lst_Dep[1]):
            itkObj=lst_Dep[1]
            flagOo=1
            listObjGEO_itkType=list(set(makeObj_List(s,r,itkObj)))
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and isGEO_tk(s,r,lst_Dep[0]):
            flagOd=1
            itkObjd=lst_Dep[0]
            listObj_det_itkType=list(set(makeDetW_List(s,r,itkObjd)))


    # if flagSs==1:
    #     for lst_Dep in list_Dep:
    #         if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(itkSubj):
    #             print "Prep_of",lst_Dep[1]
    #             listSubjGEO_itkType.append(lst_Dep[1])

    # print "flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj))
    print "isWhat:flagS,flagAS,flagNS,flagCS,flagSs,flag_in, -listSubj_itkType-, -listWhereIn_itkType-: ",flagS,flagAS,flagNS,flagCS,flagSs,flag_in,listSubj_itkType,listWhereIn_itkType
    listObj_itkType=list(str(listObj+listNounObj+listAdjObj+listConjObj))

    if tk!="":
        t=tk
        if isWhere_tk(s,r,t) and flag_in==1:
            addtk_Type_Indicators(r,listWhereIn_itkType)
            return True
        elif isWhere_tk(s,r,t) and flagS==1:
            addtk_Type_Indicators(r,listSubj_itkType)
            return True
        elif posofTkIs(s,t,'DT') and flagSs==1:
            addtk_Type_Indicators(r,listSubjGEO_itkType)
            return True
        elif isInWhich(s,r,t):
            if flagOd==1:
                addtk_Type_Indicators(r,listObj_det_itkType)
                return True
            elif flagSs==1:
                addtk_Type_Indicators(r,listSubj_itkType)
                return True
        elif isWhich(s,r,t):
            if flagOd==1:
                addtk_Type_Indicators(r,listObj_det_itkType)
                return True
            if flagOo==1:
                addtk_Type_Indicators(r,listObjGEO_itkType)
                return True
            if t==0 and flagSs==1:
                addtk_Type_Indicators(r,listSubjGEO_itkType)
                return True
            elif t>1 and flagOd==1:
                addtk_Type_Indicators(r,listObj_det_itkType)
                return True
        elif isWhat_tk(s,r,t) and flagSs==1:
            addtk_Type_Indicators(r,listSubjGEO_itkType)
            return True
        return False

    else:
        tks=s._get_tokens()
        for itk in range(len(tks)):
            if isWhich(s,r,itk):
                return isWhere(s,r,itk)
        return False

def isWhere_tk(s,r,t):
    return lemmaofTkIs(s,t,'where')

def isWho(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_Memb=[]
    list_itkType=[]
    listSubjPER_itkType=[]
    listObjPER_itkType=[]
    listObj_det_itkType=[]
    flagS=0
    flagSs=0
    flagSd=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagOd=0
    flagOo=0
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            if isPerson_tk(s,r,lst_Dep[1]):
                itkSubj=lst_Dep[1]
                flagSs=1
                listSubjPER_itkType=list(set(makeSubj_List(s,r,itkSubj)))
            elif not isVerb(s,lst_Dep[0]):
                if isPerson_tk(s,r,lst_Dep[0]):
                    itkSubj=lst_Dep[0]
                    flagSd=1
                    listSubjPER_itkType=list(set(makeSubj_List(s,r,itkSubj)))

        if (str(lst_Dep[2])=="pobj" or str(lst_Dep[2])=="pobjpass") and isPerson_tk(s,r,lst_Dep[1]):
            itkObj=lst_Dep[1]
            flagOo=1
            listObjPER_itkType=list(set(makeObj_List(s,r,itkObj)))
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and isPerson_tk(s,r,lst_Dep[0]):
            flagOd=1
            itkObjd=lst_Dep[0]
            listObj_det_itkType=list(set(makeDetW_List(s,r,itkObjd)))

    if isWho_tk(s,r,t):
        return True
    elif posofTkIs(s,t,'DT') and (flagSs==1 or flagSd==1):
        addtk_Type_Indicators(r,listSubjPER_itkType)
        return True
    elif posofTkIs(s,t,'DT') and isMember_tk(s,r,t+1):
        list_Memb.append(t+1)
        addtk_Type_Indicators(r,list_Memb)
        return True
    elif isWhich_tk(s,r,t) and flagOd==1:
        addtk_Type_Indicators(r,listObj_det_itkType)
        return True
    return False

def isWho_tk(s,r,t):
    return lemmaofTkIs(s,t,'who')

def isWhen(s,r,t):
    list_itkSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagSw=0
    flagSwn=0
    flagT=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            list_itkSubj.append(lst_Dep[1])
            flagSs=1
            for lst_Dep1 in list_Dep:
                if (str(lst_Dep1[2])=="prep_of" or str(lst_Dep1[2])=="nn") and str(lst_Dep[0])== str(lst_Dep1[0]) :
                    list_itkType.append(lst_Dep[1])
                    flagSw=1
                if str(lst_Dep[2])=="conj_and" and str(lst_Dep[0])== str(lst_Dep1[0]):
                    list_itkType.append(lst_Dep[1])
                    flagSwn=1

    listSubj_itkType=list(set(listSubj+listConjSubj+list_itkType))
    print "Subj list after adding",listSubj_itkType
    print "flagSs, flagS,flagAS,flagNS,flagCS,flagSw, flagSwn: ",flagSs,  flagS,flagAS,flagNS,flagCS,flagSw, flagSwn
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "Obj list after adding",listObj_itkType
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO

    if (isWhen_tk(s,r,t)) and flagSs==1:
        print " isWhen cond1!!"
        addtk_Type_Indicators(r,listSubj_itkType)
        return True
    elif isWhat_tk(s,r,t) and flagSwn==1:
        print "isWhen cond2!!"
        lnIdx=len(list_itkSubj)
        i=0
        while i<lnIdx:
            itkSubj=list_itkSubj.pop()
            i=i+1
            if neofTkIs(s,int(itkSubj),'DUR') or neofTkIs(s,itkSubj,'DAT') or lemmaofTkIs(s,int(itkSubj),'year'):
                addtk_Type_Indicators(r,itkSubj)
                return True
    return False


def isWhen_tk(s,r,t):
    return lemmaofTkIs(s,t,'when')

def isWhat(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagSw=0
    flagSwch=0
    flagT=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass") and (not isGEO_tk(s,r,lst_Dep[1]) and (not isPerson_tk(s,r,lst_Dep[1]))):
            itkSubj=lst_Dep[1]
            flagSs=1
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            for lst_Dep1 in list_Dep:
                if str(lst_Dep1[2])=="prep_in" and  str(lst_Dep[0])== str(lst_Dep1[0]) and (not isGEO_tk(s,r,lst_Dep1[1]) and (not isPerson_tk(s,r,lst_Dep1[1]))):
                    itkSubj=lst_Dep[1]
                    list_itkType.append(lst_Dep[1])
                    flagSw=1
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and (not isGEO_tk(s,r,lst_Dep[0]) and (not isPerson_tk(s,r,lst_Dep[0]))):
            list_itkType.append(lst_Dep[0])
            flagSwch=1

    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj+list_itkType))
    print "Subj list after adding",listSubj_itkType
    print "flagSs, flagS,flagAS,flagNS,flagCS,flagSw, flagSwch: ",flagSs,  flagS,flagAS,flagNS,flagCS,flagSw, flagSwch
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "Obj list after adding",listObj_itkType
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO

    if isWhat_tk(s,r,t) and not isHowmany(s,r,t) and (flagSs==1 or flagS==1):
        print "cond1!!"
        addtk_Type_Indicators(r,listSubj_itkType)
        return True
    elif (isWhich(s,r,t)) and flagSwch==1:
        print "cond2!!"
        # and (flagSw==1 or flagSs==1)
        addtk_Type_Indicators(r,list_itkType)
        return True
    elif posofTkIs(s,t,'DT') and not isHowmany(s,r,t) and not isWho(s,r,t) and flagSs==1:
        print "cond3!!"
        addtk_Type_Indicators(r,listSubj_itkType)
        return True

    return False


def isWhat_tk(s,r,t):
    return lemmaofTkIs(s,t,'what')

def isWhich(s,r,t):
    cmpObj=[]
    objList=[]
    objAdj=[]
    objNoun=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="det":
            if lemmaofTkIs(s,lst_Dep[1],"which"):
                objList.append(lst_Dep[0])
                objAdj=getAdj_Obj_of_Sentence(s,r,lst_Dep[0])
                objNoun=getNoun_Obj_of_Sentence(s,r,lst_Dep[0])
                for lst_Dep1 in list_Dep:
                    if str(lst_Dep1[2])=="dep" and str(lst_Dep1[0])==str(lst_Dep[0]):
                        objList.append(lst_Dep1[1])


    cmpObj=objList+objAdj+objNoun
    cmpObj=list(set(cmpObj))
    print "cmpObj, len(cmpObj) :",cmpObj, len(cmpObj)
    if isWhich_tk(s,r,t):
        if len(cmpObj)==1:
            objItem=cmpObj.pop()
            r.addIndicators_tk(objItem)
            return True
        elif len(cmpObj)>1:
            lncmpObj=len(cmpObj)
            i=0
            while i<lncmpObj:
                r.addIndicators_tk(cmpObj[i])
                i=i+1
            return True
    return False


def isWhich_tk(s,r,t):
    return (lemmaofTkIs(s,t,'which') or isInWhich(s,r,t))

def isInWhich(s,r,t):
    return (lemmaofTkIs(s,t,'in') or lemmaofTkIs(s,t,'through') or lemmaofTkIs(s,t,'to') or lemmaofTkIs(s,t,'for')) and lemmaofTkIs(s,t+1,'which')

def isHowmuch(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagSw=0
    flagWh=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            itkSubj=lst_Dep[1]
            flagS=1
            if (lemmaofTkIs(s,lst_Dep[1],'amount')):
                flagWh=1


    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj))
    # print "isHowmany:Subj list after adding",listSubj_itkType
    # print "isHowmany:flagS,flagAS,flagNS,flagCS,flagSs,flagSw",flagS,flagAS,flagNS,flagCS,flagSs,flagSw
    listObj_itkType=list(set(listObj+listNounObj+listAdjObj+listConjObj))
    # print "isHowmany: Obj list after adding",listObj_itkType
    # print "isHowmany: flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO


    if lemmaofTkIs(s,t,'what'):
        if flagWh==1:
            addtk_Type_Indicators(r,listSubj_itkType)
            return True
        # elif flagCS==1:
        #     print "Is  actually HMany  in What!!!"
        #     addtk_Type_Indicators(r,listConjSubj)
        #
        #     return True

    elif posofTkIs(s,t,'DT') and flagCS==1:
        addtk_Type_Indicators(r,listSubj_itkType)
        return True
    if isHowmuch_tk(s,r,t):
        r.addIndicators_tk(t)
        r.addIndicators_tk(t+1)
        print "iSHowmuch() ...flagO, flagS:", flagO, flagS, r.tk_indicators
        if flagO==1:
            listObj_itkType=removeListA_listB(r.tk_indicators,listObj)
            addtk_Type_Indicators(r,listObj_itkType)
            return True
        elif flagS==1:
            listSubj_itkType=removeListA_listB(r.tk_indicators,listObj)
            addtk_Type_Indicators(r,listSubj_itkType)
            print "r.tk_indicators, flagS:", flagS, r.tk_indicators
            return True
    return False

def isHowmuch_tk(s,r,t):
    return (lemmaofTkIs(s,t,'how') and lemmaofTkIs(s,t+1,'much'))

def isHowmany(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagSw=0
    flagWh=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            itkSubj=lst_Dep[1]
            flagS=1
            if (lemmaofTkIs(s,lst_Dep[1],'amount')):
                flagWh=1


    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj))
    # print "isHowmany:Subj list after adding",listSubj_itkType
    # print "isHowmany:flagS,flagAS,flagNS,flagCS,flagSs,flagSw",flagS,flagAS,flagNS,flagCS,flagSs,flagSw
    listObj_itkType=list(set(listObj+listNounObj+listAdjObj+listConjObj))
    # print "isHowmany: Obj list after adding",listObj_itkType
    # print "isHowmany: flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO


    if lemmaofTkIs(s,t,'what'):
        if flagWh==1:
            addtk_Type_Indicators(r,listSubj_itkType)
            return True
        # elif flagCS==1:
        #     print "Is  actually HMany  in What!!!"
        #     addtk_Type_Indicators(r,listConjSubj)
        #
        #     return True

    elif posofTkIs(s,t,'DT') and flagCS==1:
        addtk_Type_Indicators(r,listSubj_itkType)
        return True
    if isHowmany_tk(s,r,t):
        r.addIndicators_tk(t)
        r.addIndicators_tk(t+1)
        if flagO==1:
            listObj_itkType=removeListA_listB(r.tk_indicators,listObj_itkType)
            addtk_Type_Indicators(r,listObj_itkType)
            return True
        elif flagS==1:
            listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj_itkType)
            addtk_Type_Indicators(r,listSubj_itkType)
            return True
    return False


def isHowmany_tk(s,r,t):
    return (lemmaofTkIs(s,t,'how') and lemmaofTkIs(s,t+1,'many'))

def isHowOften(s,r,t):
    return (lemmaofTkIs(s,t,'how') and lemmaofTkIs(s,t+1,'often'))

def isIsthere(s,r,t):
    return (lemmaofTkIs(s,t,'be') and lemmaofTkIs(s,t+1,'there'))


def isYesNo(s,r,t):
    return (lemmaofTkIs(s,t,'be') or lemmaofTkIs(s,t,'do') or lemmaofTkIs(s,t,'have')or lemmaofTkIs(s,t,'can')) and (not isIsthere(s,r,t))


def isList(s,r,t):
    if (lemmaofTkIs(s,t,'give') or lemmaofTkIs(s,t,'list') or isNoun(s,t) or (posofTkIs(s,t,'DT') and (posofTkIs(s,t+1,'NN') or posofTkIs(s,t+1,'NNS'))) or (posofTkIs(s,t,'DT') and posofTkIs(s,t+1,'JJ'))):
        # print "This is list Q!!"
        return True

def isWhere_in(s,r):
    if isWhere(s,r,0):
        tks=s._get_tokens()
        for itk in range(len(tks)):
            if lemmaofTkIs(s,itk,'in'):
                return True
    return False


def isAtomic_Property(s,r,tk):
    if (isAdjective(s,tk) or isNoun(s,tk)) and not isPerson_tk(s,r,tk):
        if not (isEntity_2tk(s,r,tk)):
            return True
    return False

def isAtomic_CompProperty(s,r,tk):
    if (isAdjective(s,tk) or isNoun(s,tk)):
        if not (isEntity_2tk(s,r,tk)):
            return True
    return False

def isProperties(s,r):
    tks=s._get_tokens()
    listProps=[]
    list_Dep=s.sint._dependencies
    lnItk=len(tks)

    for itk in range(len(tks)):
        if itk+1<=len(tks):
            if isAtomic_Property(s,r,itk) and isAtomic_Property(s,r,itk+1):
                listProps.append(itk)
                # listProps.append(itk+1)

            elif isAdjective(s,itk) or posofTkIs(s,itk,'CD') or posofTkIs(s,itk,'RB') or  neofTkIs(s,itk,'NUM'):
                listProps.append(itk)
            elif posofTkIs(s,itk,'VBG'):
                for lst_Dep in list_Dep:
                    if str(lst_Dep[2])=="amod" and str(lst_Dep[1])==str(itk) and (posofTkIs(s,lst_Dep[0],'NN') or (posofTkIs(s,lst_Dep[0],'NNS'))):
                        listProps.append(itk)



    listProps=sorted(list(set(listProps)))
    print "Content of isProperties  before removing indicator",listProps,r.tk_indicators

    listProps=removeListA_listB(r.tk_indicators,listProps)
    if len (listProps)>0:
        addListA_listB(r.tk_indicators,listProps)
        print "Content of isProperties  before binding call",listProps,r.tk_indicators
        return True
    return False

def isCompound_Properties(s,r):
    tks=s._get_tokens()
    maxLenProp1=0
    maxLenProp2=0
    maxLenProp3=0
    listCmpProps1=[]
    listCmpProps2=[]
    listCmpProps3=[]

    flag1=0
    flag2=0
    flag3=0

    list_Dep=s.sint._dependencies
    for itk in range(len(tks)):
        if isAtomic_CompProperty(s,r,itk) and maxLenProp1==0 and flag1==0 and flag2==0 and flag3==0:
            listCmpProps1.append(itk)
            maxLenProp1=maxLenProp1+1
            flag1=1
            # print "Cond 1 detected!!!",itk

        elif isAtomic_CompProperty(s,r,itk) and maxLenProp1!=0 and  maxLenProp2==0 and flag1==0 and flag2==1 and flag3==0:
            listCmpProps2.append(itk)
            maxLenProp2=maxLenProp2+1
            # print "Cond 2 detected!!!",itk

        elif isAtomic_CompProperty(s,r,itk) and maxLenProp1!=0 and  maxLenProp2!=0 and  maxLenProp3==0 and flag1==0 and flag2==0 and flag3==1 :
            listCmpProps3.append(itk)
            maxLenProp3=maxLenProp3+1
            # print "Cond 3 detected!!!",itk

        elif ( isAtomic_CompProperty(s,r,itk) or posofTkIs(s,itk,'JJR') or posofTkIs(s,itk,'CD') or lemmaofTkIs(s,itk,'than') or neofTkIs(s,itk,'NUM')) and maxLenProp1!=0 and flag1!=0:
            listCmpProps1.append(itk)
            maxLenProp1=maxLenProp1+1
            # print "Cond 4 detected!!!",itk

        elif (isAtomic_CompProperty(s,r,itk) or posofTkIs(s,itk,'JJR') or posofTkIs(s,itk,'CD') or lemmaofTkIs(s,itk,'than') or neofTkIs(s,itk,'NUM')) and maxLenProp2!=0 and flag2!=0:
            listCmpProps2.append(itk)
            maxLenProp2=maxLenProp2+1
            flag2=2
            # print "Cond 5 detected!!!",itk

        elif (isAtomic_CompProperty(s,r,itk) or posofTkIs(s,itk,'JJR') or posofTkIs(s,itk,'CD') or lemmaofTkIs(s,itk,'than') or neofTkIs(s,itk,'NUM')) and maxLenProp3!=0 and flag3!=0:
            listCmpProps2.append(itk)
            maxLenProp3=maxLenProp3+1
            flag3=2
            # print "Cond 6 detected!!!",itk

        elif (lemmaofTkIs(s,itk,'of') or lemmaofTkIs(s,itk,'in') or lemmaofTkIs(s,itk,'with') or lemmaofTkIs(s,itk,'on') or lemmaofTkIs(s,itk,'has') or lemmaofTkIs(s,itk,'have')) and maxLenProp1!=0 and flag1!=0:
            # print "level 2 detected!!!",itk
            flag1=0
            flag2=1
        elif (lemmaofTkIs(s,itk,'of') or lemmaofTkIs(s,itk,'in') or lemmaofTkIs(s,itk,'with') or lemmaofTkIs(s,itk,'on') or lemmaofTkIs(s,itk,'has') or lemmaofTkIs(s,itk,'have')) and maxLenProp2!=0 and flag2!=0:
            # print "level 3 detected!!!",itk
            flag1=0
            flag2=0
            flag3=1
        elif lemmaofTkIs(s,itk,'the') and (maxLenProp1!=0  or maxLenProp2!=0 or maxLenProp3!=0) :
            # print "THE token wirhout chnage, itk,flag1,flag2  ",itk,flag1,flag2
            continue
        elif not (isAtomic_CompProperty(s,r,itk)) and flag1==0 and (flag2>0 or flag3>0):
            break
        elif flag1==1:
            # print "resume level"
            flag1=0
            flag2=0
            flag3=0
            maxLenProp1=0
            maxLenProp2=0
            maxLenProp3=0
            listCmpProps1=removeListItem(listCmpProps1)

    listCmpProps1=removeListA_listB(r.tk_indicators,listCmpProps1)
    listCmpProps2=removeListA_listB(r.tk_indicators,listCmpProps2)
    listCmpProps3=removeListA_listB(r.tk_indicators,listCmpProps3)

    listCmpProps=listCmpProps1+listCmpProps2+listCmpProps3
    # print "Staus of flag1,flag2,falf3, r,indicator",flag1,flag2,flag3,r.tk_indicators
    # print "listCmpProps1,listCmpProps2,listCmpProps3,listCmpProps",listCmpProps1,listCmpProps2,listCmpProps3,listCmpProps

    if flag3==0:
        if flag1==0 and flag2>=1:
            if len (listCmpProps1)>0 or len (listCmpProps2)>0 :
                # print "final 1 isCMP detected!!!"
                for item in listCmpProps:
                    r.addIndicators_tk(item)
                # print "Ok!!Content of listprops and indicate before binding compound call:",listCmpProps1,listCmpProps2,listCmpProps,r.tk_indicators
                return True
    elif flag3>=0:
        if len (listCmpProps1)>0 or len (listCmpProps2)>0 or (len (listCmpProps3)>0):
            # print "final 2 isCMP detected!!!"
            for item in listCmpProps:
                r.addIndicators_tk(item)
            # print "Ok!!Content of listprops and indicate before binding compound call:",listCmpProps1,listCmpProps2,listCmpProps,r.tk_indicators
            return True

    return False

def isMember(s,r):
    tks=s._get_tokens()
    flag=0
    for itk in range(len(tks)):
        if isMember_tk(s,r,itk) and (lemmaofTkIs(s,itk+1,'of') or lemmaofTkIs(s,itk+1,'in') or lemmaofTkIs(s,itk+1,'to')):
            # print "isMember_tk",itk
            r.addIndicators_tk(itk)
            flag=1
    if flag==1:
        return True
    else:
        return False

def isMember_tk(s,r,itk):
    listMember=['member','belong']
    lma_tk=s._get_token(itk)._lemma()
    if lma_tk in listMember :
        return True
    return False

def isPerson(s,r):
    flag=0
    itk=0
    listPerson=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    # for itk in range(len(tks)):
    while itk <lnItk:
        lma_tk=s._get_token(itk)._lemma()
        if not(lma_tk.isdigit()):
            if itk+3<lnItk:
                if isNonPerson_3tk(s,r,itk):
                    itk=itk+3
                    continue

                elif isPerson_3tk(s,r,itk):
                    flag=1
                    listPerson.append(itk)
                    listPerson.append(itk+1)
                    listPerson.append(itk+2)
                    itk=itk+3
                    continue
            if ((isPerson_NonRelative(s,r,itk) or isPerson_tk(s,r,itk)) and flag==0):
                flag=1
                # r.addIndicators_tk(itk)
                listPerson.append(itk)
            elif ((isPerson_NonRelative(s,r,itk) or isPerson_tk(s,r,itk)) and flag!=0):
                # r.addIndicators_tk(itk)
                listPerson.append(itk)
                flag=2
        itk=itk+1

    print "content of listperson before remove",r.tk_indicators,listPerson
    listPerson=removeListA_listB(r.tk_indicators,listPerson)
    # print "content of listperson after remove",r.tk_indicators,listPerson
    lnIdx=len(listPerson)
    if lnIdx>0 and (flag==1 or flag==2):
        listIndicator=addListA_listB(r.tk_indicators,listPerson)
        # print "content of listIndicator after adding",r.tk_indicators,listIndicator,listPerson
        print "after removing repeated person in indicator ISPERSON()", listPerson
        return True
    return False


def isPerson_tk(s,r,itk):
    listNonPerson=['name','date','birth','Uzi','instrument','Berlin','frog','tree','Captain America','creator','Illinois','Minecraft']
    lmaItk=""
    lmaItk1=s._get_token(itk)._lemma()
    if itk>0:
        lmaItk0=s._get_token(itk-1)._lemma()
        lmaItk=lmaItk0 + " " +lmaItk1
        # print "Combined Person",lmaItk
    if isEntity_tk(s,r,itk):
        if (neofTkIs(s,itk,'PER') or isPersonInWN(s,r,itk)) and (not (lmaItk1 in listNonPerson) and not (lmaItk in  listNonPerson)):
            print "isPerson_tk!!!",lmaItk1
            return True

    return False

def isPerson_3tk(s,r,itk):
    cmpPersonName=['Lawrence of Arabia']
    tk_per=itk
    lma_tk1=s._get_token(tk_per)._lemma()
    lma_tk2=s._get_token(tk_per+1)._lemma()
    lma_tk3=s._get_token(tk_per+2)._lemma()
    lma_Cmp=lma_tk1 + " " + lma_tk2 + " " + lma_tk3
    if (lma_Cmp in cmpPersonName):
         return True
    return False

def isNonPerson_3tk(s,r,itk):
    cmpPersonName=['Bay of Pigs']
    tk_per=itk
    lma_tk1=s._get_token(tk_per)._lemma()
    lma_tk2=s._get_token(tk_per+1)._lemma()
    lma_tk3=s._get_token(tk_per+2)._lemma()
    lma_Cmp=lma_tk1 + " " + lma_tk2 + " " + lma_tk3
    if (lma_Cmp in cmpPersonName):
         return True
    return False


def isPerson_Prop(s,r,tk):
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    if tk=='':
        for itk in range(len(tks)):
            print "tk",itk
            if neofTkIs(s,itk,'PER') or isPersonInWN(s,r,itk):
                tk_per=itk
                for lst_Dep in list_Dep:
                    if str(lst_Dep[2])=="prep_of" and str(lst_Dep[1])==str(tk_per) and (posofTkIs(s,lst_Dep[0],'NN') or (posofTkIs(s,lst_Dep[0],'NNS'))):
                        return True
    else:
        if neofTkIs(s,tk,'PER') or isPersonInWN(s,r,tk) :
            tk_per=tk
            for lst_Dep in list_Dep:
                if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(tk_per) and (posofTkIs(s,lst_Dep[0],'NN') or (posofTkIs(s,lst_Dep[0],'NNS'))):
                    return True
    return False


def isPerson_NonRelative(s,r,itk):
    tk_per=itk
    if (isPerson_tk(s,r,tk_per)) and (not(isPerson_Prop(s,r,tk_per))):
        if isPerson_NonRelative(s,r,tk_per+1):
            # print "This token is independent person ",tk_per
            return True
        elif not(isPerson_tk(s,r,tk_per+1)):
            return True

    return False

def isPersonInWN(s,r,itk):
    lsItem1=[]
    lsItem2=[]
    # ls=getSynsets(itk,pos='n')
    # ls=lemmalist(wrd)
    lma_tk=s._get_token(itk)._lemma()
    if isEntity_tk(s,r,itk):
        ls=entityList(lma_tk)
        # print "list in  Synset WN for Person:",lma_tk,ls
        for lsitem in range(len(ls)):
            lsItem1=ls[lsitem]
            lenitem=len(lsItem1)
            for subitem1 in range(len(lsItem1)):
                lsItem2=lsItem1[subitem1]
                for subitem2 in range(len(lsItem2)):
                    if lsItem2[subitem2]=="person" or lma_tk=="people":
                        # print "\n","was found Person in isPersonInWN:",lma_tk,lenitem,lsItem2[subitem2]
                        return True
                    # else:
                        # print "\n","item of list in  Synset WN for Person:",lma_tk,lenitem,lsItem2[subitem2]

    return False

def isAction(s,r):
    nonAction=['belong']
    listAction=[]
    listAction=getVerb_of_Sentence(s,r)
    for vrb in listAction:
        if s._get_token(vrb)._lemma() in nonAction:
            listAction.remove(vrb)
    for vrb in listAction:
        if isVerbAux_Main(s,vrb):
            listAction.remove(vrb)
            # print "isVerbAux_Main"
    print "len of Action", len(listAction),listAction
    # print "isAction: content of listAction before remove",r.tk_indicators,listAction
    listAction=removeListA_listB(r.tk_indicators,listAction)
    # print "isAction: content of listAction after remove",r.tk_indicators,listAction
    lnIdx=len(listAction)
    if lnIdx>0:
        print "find action"
        addtk_Type_Indicators(r,listAction)
        return True
    return False


def isEffect(s,r):
    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>=1:
        return True
    return False


def isStatus(s,r):
    flagS=0
    flagSe=0
    flagT=0
    tks=s._get_tokens()
    for itk in range(len(tks)):
        lma_tk=s._get_token(itk)._lemma()
        lsLemma=entityList("status")
        # print "lsLemma status: ", lma_tk, lsLemma
        for lsitem in range(len(lsLemma)):
            lsItem1=lsLemma[lsitem]
            for subitem1 in range(len(lsItem1)):
                lsItem2=lsItem1[subitem1]
                for subitem2 in range(len(lsItem2)):
                    if lsItem2[subitem2]==lma_tk:
                        print "find lemma list status: ", lma_tk, lsLemma
                        r.addIndicators_tk(itk)
                        flagS=1

    list_Dep=s.sint._dependencies
    for lst_Dep1 in list_Dep:
        if str(lst_Dep1[2])=="cop":
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="root" and isAdjective(s,lst_Dep2[1]) and str(lst_Dep2[1])==str(lst_Dep1[0]):
                    r.addIndicators_tk(lst_Dep2[1])
                    flagS=1

                    # NSubj=getNoun_Subj_of_Sentence(s,r,lst_Dep2[0])
                    # ASubj=getAdj_Subj_of_Sentence(s,r,lst_Dep2[0])
                    # r.addIndicators_tk(lst_Dep2[1])
                    # r.addIndicatorsList_tk(NSubj)
                    # r.addIndicatorsList_tk(ASubj)

    # i=0
    # for tk in s._get_tokens():
    #     if posofTkIs(s,i,'IN')and (lemmaofTkIs(s,i,'in')or lemmaofTkIs(s,i,'at')):
    #         print ("The state word is: ", s._get_token(i)._word())
    #         return True
    #     i=i+1
    if flagS==1:
        # print "This is status!!"
        return True
    return False

def isQuantifier(s,r):
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if(lemmaofTkIs(s,itk,'all')or lemmaofTkIs(s,itk,'any')or lemmaofTkIs(s,itk,'some')or neofTkIs(s,itk,'NUM') or neofTkIs(s,itk,'ORD')):
            return True
    return False


def isQuantifier_tk(s,r,itk):
    flagQ=0
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="advmod" and str(lst_Dep[1])==str(itk):
            for lst_Dep1 in list_Dep:
                if (str(lst_Dep1[2])=="attr" or str(lst_Dep1[2])=="advmod" ) and str(lst_Dep[0])==str(lst_Dep1[1]):
                    flagQ=1


    if lemmaofTkIs(s,itk,'how')and flagQ==1:
        return True
    return False


def isEntity(s,r):
    listEntity=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    itk=0
    print "r.tk_indicators: ", r.tk_indicators
    indicator=r.tk_indicators
    while itk <lnItk:
        r.tk_indicators=indicator
        print "isNoun(s,itk),isGEO_tk(s,r,itk), isPerson_tk(s,r,itk), itk in r.tk_indicators ",itk, indicator, isNoun(s,itk), isGEO_tk(s,r,itk), isPerson_tk(s,r,itk), itk in r.tk_indicators
        if isEntity_3tk(s,r,itk):
            listEntity.append(itk)
            listEntity.append(itk+1)
            listEntity.append(itk+2)
            itk=itk+2
        elif isEntity_2tk(s,r,itk):
            listEntity.append(itk)
            listEntity.append(itk+1)
            itk=itk+1
        elif isNoun(s,itk) and (not isGEO_tk(s,r,itk)) and (not isPerson_tk(s,r,itk)) and not (itk in r.tk_indicators):
            listEntity.append(itk)
        itk=itk+1
    print "listEntity in isEntity!!",listEntity
    listEntity=removeListA_listB(r.tk_indicators,listEntity)
    lnIdx=len(listEntity)
    if lnIdx>0:
        listIndicator=addListA_listB(r.tk_indicators,listEntity)
        print "IsEntity with Indicator: ", listIndicator
        return True

    return False

def isEntity_2tk(s,r,itk):
    listEntity_2tk=['Pilsner Urquell','Hells Angels']
    tks=s._get_tokens()
    lnItk=len(tks)
    lmaItk=""
    lmaItk1=s._get_token(itk)._lemma()
    if itk+1<lnItk:
        lmaItk2=s._get_token(itk+1)._lemma()
        lmaItk=lmaItk1 + " " +lmaItk2
        if lmaItk in listEntity_2tk:
            return True
    if itk-1>=0:
        lmaItk2=s._get_token(itk-1)._lemma()
        lmaItk=lmaItk2 + " " +lmaItk1
        # print "Combined Entity -",lmaItk
        if lmaItk in listEntity_2tk:
            return True

    return False

def isEntity_3tk(s,r,itk):
    listEntity_3tk=['world of Warcraft']
    tks=s._get_tokens()
    lnItk=len(tks)
    lmaItk=""
    lmaItk1=s._get_token(itk)._lemma()
    if itk+2<lnItk:
        lmaItk3=s._get_token(itk+2)._lemma()
        lmaItk2=s._get_token(itk+1)._lemma()
        lmaItk=lmaItk1 + " " + lmaItk2 + " " +lmaItk3
        if lmaItk in listEntity_3tk:
            return True
    if itk-2>=0:
        lmaItk3=s._get_token(itk-2)._lemma()
        lmaItk2=s._get_token(itk-1)._lemma()
        lmaItk=lmaItk3 + " " +lmaItk2 + " " +lmaItk1
        # print "Combined Entity -",lmaItk
        if lmaItk in listEntity_3tk:
            return True
    return False

def isEntity_tk(s,r,itk):
    return isNoun(s,itk)

def isSecond_Entity(s,r):
    flag=0
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if isNoun(s,itk):
            if flag==1:
                return True
            else:
                flag=1
    return False


def isTemp(s,r):
    tks=s._get_tokens()
    flag=0
    for itk in range(len(tks)):
        if (neofTkIs(s,itk,'DUR')or neofTkIs(s,itk,'SET')):
            r.addIndicators_tk(itk)
            flag=1

    if flag==1:
        return True
    else:
        return False

def isORG(s,r):
    flag=0
    itk=0
    listORG=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    while itk<lnItk :
        lma_tk=s._get_token(itk)._lemma()
        if not (itk in r.tk_indicators):
            if (itk+3 <lnItk) and isORG_2tk_3tk(s,r,itk)==3:
                listORG.append(itk)
                listORG.append(itk+1)
                listORG.append(itk+2)
                itk=itk+2
                flag=1
            if (itk+2 <lnItk) and isORG_2tk_3tk(s,r,itk)==2:
                listORG.append(itk)
                listORG.append(itk+1)
                itk=itk+1
                flag=1
            elif isORG_tk(s,r,itk):
                listORG.append(itk)
                # r.addIndicators_tk(itk)
                flag=1
        itk=itk+1
    # print "len of ORG", len(listORG),listORG
    # print "isGEO: content of listORG before remove",r.tk_indicators,listORG
    listORG=removeListA_listB(r.tk_indicators,listORG)
    # print "isORG: content of listORG after remove",r.tk_indicators,listORG
    lnIdx=len(listORG)
    if lnIdx>0:
        listIndicator=addListA_listB(r.tk_indicators,listORG)
        # print "content of r.tk_indicators,listIndicator,listORG  after adding",r.tk_indicators,listIndicator,listORG
        if flag==1:
            return True
    return False

def isORG_tk(s,r,itk):
    listNonORG=['name']
    lmaItk=""
    lmaItk1=s._get_token(itk)._lemma()
    if itk>0:
        lmaItk0=s._get_token(itk-1)._lemma()
        lmaItk=lmaItk0 + " " +lmaItk1
    if (neofTkIs(s,itk,'ORG')) and (not (lmaItk1 in listNonORG) and not (lmaItk in  listNonORG)):
        return True

    return False

def isORG_2tk_3tk(s,r,itk):
    cmpORGName=['Universal Studios']
    tk_ORG=itk
    lma_tk1=s._get_token(tk_ORG)._lemma()
    lma_tk2=s._get_token(tk_ORG+1)._lemma()
    lma_tk3=s._get_token(tk_ORG+2)._lemma()
    lma_Cmp2=lma_tk1 + " " + lma_tk2
    lma_Cmp3=lma_tk1 + " " + lma_tk2 + " " + lma_tk3

    if lma_Cmp2 in cmpORGName:
         return 2
    elif lma_Cmp3 in cmpORGName:
        return 3
    return 0

def isGEO(s,r):
    flag=0
    itk=0
    listGEO=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    while itk<lnItk :
        lma_tk=s._get_token(itk)._lemma()
        if not(lma_tk.isdigit()) and not (itk in r.tk_indicators):
            if (itk+3 <lnItk) and isNonGEO_2tk_3tk(s,r,itk)==3:
                itk=itk+2
            if (itk+2 <lnItk) and isNonGEO_2tk_3tk(s,r,itk)==2:
                itk=itk+1
            elif isGEO_tk(s,r,itk):
                listGEO.append(itk)
                # r.addIndicators_tk(itk)
                flag=1
        itk=itk+1
    # print "len of GEO", len(listGEO),listGEO
    print "isGEO: content of listGEO before remove",r.tk_indicators,listGEO
    listGEO=removeListA_listB(r.tk_indicators,listGEO)
    print "isGEO: content of listGEO after remove",r.tk_indicators,listGEO
    lnIdx=len(listGEO)
    if lnIdx>0:
        listIndicator=addListA_listB(r.tk_indicators,listGEO)
        # print "content of r.tk_indicators,listIndicator,listGEO  after adding",r.tk_indicators,listIndicator,listGEO
        if flag==1:
            return True
    return False

def isGEO_NonRelative(s,r,itk):
    tk_GEO=itk
    if (isGEO_tk(s,r,tk_GEO)) and (not(isGEO_Property(s,r,tk_GEO))):
        if isGEO_NonRelative(s,r,tk_GEO+1):
            # print "This token is independent GEO ",tk_GEO
            return True
        elif not(isGEO_tk(s,r,tk_GEO+1)):
            # print "The next token is not  GEO ",tk_GEO
            return True

    return False

def isGEO_tk(s,r,itk):
    exceptionGEO=['name','goal','responsibility','activity','authority','father','time zone','most','GIMP','Jackson','Michael Jordan','conflict','Lawrence','flow','man','British earl','Hells Angels','viking Press','Captain America']
    combinedGEO=['time zone']
    lmaItk=""
    lmaItk1=s._get_token(itk)._lemma()
    if itk>0:
        lmaItk0=s._get_token(itk-1)._lemma()
        lmaItk=lmaItk0 + " " +lmaItk1
        # print "Combined GEO",lmaItk
    if (neofTkIs(s,itk,'LOC') or isGEOInWN(s,r,itk)) and not isORG_tk(s,r,itk) and (not (lmaItk1 in exceptionGEO) and not (lmaItk in exceptionGEO)) :
        print ("The NE for word as isGEO_tk is: ", s._get_token(itk)._word(),s._get_token(itk)._ne())
        return True
    return False


def isNonGEO_2tk_3tk(s,r,itk):
    cmpGEOName=['cuban Missile Crisis','world of Warcraft']
    tk_GEO=itk
    lma_tk1=s._get_token(tk_GEO)._lemma()
    lma_tk2=s._get_token(tk_GEO+1)._lemma()
    lma_tk3=s._get_token(tk_GEO+2)._lemma()
    lma_Cmp2=lma_tk1 + " " + lma_tk2
    lma_Cmp3=lma_tk1 + " " + lma_tk2 + " " + lma_tk3
    if lma_Cmp2 in cmpGEOName:
        return 2
    elif lma_Cmp3 in cmpGEOName:
        return 3
    return 0

def isGEO_Property(s,r,tk):
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    if tk=='':
        for itk in range(len(tks)):
            print "tk",itk
            if neofTkIs(s,itk,'LOC') or isGEOInWN(s,r,itk):
                tk_GEO=itk
                for lst_Dep in list_Dep:
                    if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(tk_GEO) and (isNoun(s,lst_Dep[0])):
                        return True
    else:
        if neofTkIs(s,tk,'LOC') or isGEOInWN(s,r,tk):
            tk_GEO=tk
            for lst_Dep in list_Dep:
                if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(tk_GEO) and (isNoun(s,lst_Dep[0])):
                    return True
    return False


def isGEOInDBpedia(s,r,itk):
    lma_tk=s._get_token(itk)._lemma()
    return isCity(lma_tk,'en') or isRegion(lma_tk,'en') or isCountry(lma_tk,'en') or isLocation(lma_tk,'en')
           # or isDemonym(lma_tk,'en')

def isGEOInWN(s,r,itk):
    lsItem1=[]
    lsItem2=[]
    location=['city','town','state','capital','country','county','museum','bridge','airport','continent','ocean','location','region','mountain','sea','cave','river','island']
    # ls=getSynsets(itk,pos='n')
    # ls=lemmalist(wrd)
    lma_tk=s._get_token(itk)._lemma()
    if isEntity_tk(s,r,itk):
        ls=entityList(lma_tk)
        # print "list in  Synset WN for Location:",lma_tk,ls
        for lsitem in range(len(ls)):
            lsItem1=ls[lsitem]
            lenitem=len(lsItem1)
            for subitem1 in range(len(lsItem1)):
                lsItem2=lsItem1[subitem1]
                for subitem2 in range(len(lsItem2)):
                    if lsItem2[subitem2]in location:
                        print "\n","was found Location:",lma_tk,lenitem,lsItem2[subitem2]
                        return True
                    # else:
                        # print "\n","item of list in  Synset WN for Person:",lma_tk,lenitem,lsItem2[subitem2]

    return False

def isSynonym(s,r):
    synonymList=['nickname','synonym','call','abbreviation']
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if s._get_token(itk)._lemma() in synonymList:
            r.addIndicators_tk(itk)
            return True
    return False


def isDate(s,r):
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if neofTkIs(s,itk,'DAT'):
            return True
    return False

def isTimeRelation(s,r):
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_after" or str(lst_Dep[2])=="prep_before" or str(lst_Dep[2])=="prep_between" or str(lst_Dep[2])=="prep_within" or str(lst_Dep[2])=="prep_than":
            return True
    return False

def isNumericRelation(s,r):
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if (posofTkIs(s,itk,'JJR') and posofTkIs(s,itk+1,'IN') and (posofTkIs(s,itk+2,'CD') or neofTkIs(s,itk+2,'NUM'))):
            # print ("The Numeric Relation  word is: ", s._get_token(itk)._word())
            return True
    return False

def isEqual(s,r):
    flagS=0
    flagSe=0
    flagT=0
    listEqual=['also']
    list_itkType=[]
    list_Dep=s.sint._dependencies
    for lst_Dep1 in list_Dep:
        if str(lst_Dep1[2])=="cop":
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="prep" and str(lst_Dep1[0])==str(lst_Dep2[0]) and s._get_token(lst_Dep2[1])._lemma() in listEqual:
                    r.addIndicators_tk(lst_Dep2[0])
                    NSubj=getNoun_Subj_of_Sentence(s,r,lst_Dep2[0])
                    ASubj=getAdj_Subj_of_Sentence(s,r,lst_Dep2[0])
                    # r.addIndicators_tk(lst_Dep2[1])
                    r.addIndicatorsList_tk(NSubj)
                    r.addIndicatorsList_tk(ASubj)
                    # print "Was found isEqual:Ent1 indicator",str(lst_Dep2[0]),str(lst_Dep2[1]),r.tk_indicators
                    flagS=1
                    for lst_Dep3 in list_Dep:
                        if str(lst_Dep3[2])=="pobj" and str(lst_Dep3[0])==str(lst_Dep2[1]):
                            r.addIndicators_tk(lst_Dep3[1])
                            NSubj=getNoun_Subj_of_Sentence(s,r,lst_Dep3[1])
                            ASubj=getAdj_Subj_of_Sentence(s,r,lst_Dep3[1])
                            r.addIndicatorsList_tk(NSubj)
                            r.addIndicatorsList_tk(ASubj)
                            flagSe=1
                elif str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
                    r.addIndicators_tk(lst_Dep2[1])


        # elif str(lst_Dep1[2])=="prep_to" and s._get_token(lst_Dep1[0])._lemma() in listEqual:
        #     for lst_Dep2 in list_Dep:
        #         if str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
        #             r.addIndicators_tk(lst_Dep1[1])
        #             r.addIndicators_tk(lst_Dep2[1])
        #             print "Was found subType as belong",str(lst_Dep1[1]),str(lst_Dep2[1])
        #             flagT=1

    if flagSe==1:
        # print "flagSe,tk_indicators ",flagSe,r.tk_indicators
        return True

    return False


def isSubType(s,r):
    flagS=0
    flagT=0
    listSubType=['belong']
    list_itkType=[]
    list_Dep=s.sint._dependencies
    for lst_Dep1 in list_Dep:
        if str(lst_Dep1[2])=="cop":
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
                    r.addIndicators_tk(lst_Dep2[0])
                    r.addIndicators_tk(lst_Dep2[1])
                    flagS=1
        elif str(lst_Dep1[2])=="prep_to" and s._get_token(lst_Dep1[0])._lemma() in listSubType:
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
                    r.addIndicators_tk(lst_Dep1[1])
                    r.addIndicators_tk(lst_Dep2[1])
                    flagT=1

    if flagS==1 or flagT==1:
        lnIndicator=len(r.tk_indicators)
        i=0
        while (i<lnIndicator):
            listNounSubj=getNoun_Subj_of_Sentence(s,r,r.tk_indicators[i])
            listAdjSubj=getAdj_Subj_of_Sentence(s,r,r.tk_indicators[i])
            j=0
            while (j<len(listNounSubj)):
                r.addIndicators_tk(listNounSubj[j])
                j=j+1
            j=0
            while (j<len(listAdjSubj)):
                r.addIndicators_tk(listAdjSubj[j])
                j=j+1
            i=i+1
        return True

    return False


def isSubType_tk(s,r,itk):
    listSubType=['belong']
    lma_tk=s._get_token(itk)._lemma()
    if lma_tk in listSubType :
        return True
    return False


def bindSubType(s,r):
    flagS=0
    flagSW=0
    flagT=0
    listSubType=['belong']
    list_subType=[]
    list_superType=[]
    list_Dep=s.sint._dependencies
    for lst_Dep1 in list_Dep:
        if str(lst_Dep1[2])=="cop":
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
                    # print "Was found subType",str(lst_Dep2[0]),str(lst_Dep2[1])
                    list_subType.append(lst_Dep2[1])
                    list_superType.append(lst_Dep2[0])
                    r.addIndicators_tk(lst_Dep2[0])
                    r.addIndicators_tk(lst_Dep2[1])
                    flagS=1
        elif str(lst_Dep1[2])=="prep_to" and s._get_token(lst_Dep1[0])._lemma() in listSubType:
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
                    list_subType.append(lst_Dep2[1])
                    list_superType.append(lst_Dep1[1])
                    r.addIndicators_tk(lst_Dep1[1])
                    r.addIndicators_tk(lst_Dep2[1])
                    # print "Was found subType as belong",str(lst_Dep1[1]),str(lst_Dep2[1])
                    flagSW=1


    lnSubType=len(list_subType)
    i=0
    while (i<lnSubType):
        listNounSubj=getNoun_Subj_of_Sentence(s,r,list_subType[i])
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,list_subType[i])
        j=0
        while (j<len(listNounSubj)):
            list_subType.append(listNounSubj[j])
            r.addIndicators_tk(listNounSubj[j])
            j=j+1
        j=0
        while (j<len(listAdjSubj)):
            list_subType.append(listAdjSubj[j])
            r.addIndicators_tk(listAdjSubj[j])
            j=j+1
        i=i+1

    lnSuperType=len(list_superType)
    i=0
    while (i<lnSuperType):
        listNounSubj=getNoun_Subj_of_Sentence(s,r,list_superType[i])
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,list_superType[i])
        j=0
        while (j<len(listNounSubj)):
            list_superType.append(listNounSubj[j])
            r.addIndicators_tk(listNounSubj[j])
            j=j+1
        j=0
        while (j<len(listAdjSubj)):
            list_superType.append(listAdjSubj[j])
            r.addIndicators_tk(listAdjSubj[j])
            j=j+1
        i=i+1
    if flagS==1 or flagSW==1:
        r.addBoundedVars('tk_SuperType',list(set(list_superType)))
        r.addBoundedVars('tk_SubType',list(set(list_subType)))

    return True

def bindEqual(s,r):
    flagS=0
    flagSe=0
    flagT=0
    listEqual=['also']
    listEnt1=[]
    listEnt2=[]

    list_itkType=[]
    list_Dep=s.sint._dependencies
    for lst_Dep1 in list_Dep:
        if str(lst_Dep1[2])=="cop":
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="prep" and str(lst_Dep1[0])==str(lst_Dep2[0]) and s._get_token(lst_Dep2[1])._lemma() in listEqual:
                    r.addIndicators_tk(lst_Dep2[0])
                    listEnt1.append(lst_Dep2[0])
                    NSubjEnt1=getNoun_Subj_of_Sentence(s,r,lst_Dep2[0])
                    ASubjEnt1=getAdj_Subj_of_Sentence(s,r,lst_Dep2[0])
                    # r.addIndicators_tk(lst_Dep2[1])
                    r.addIndicatorsList_tk(NSubjEnt1)
                    r.addIndicatorsList_tk(ASubjEnt1)
                    # print "Was found isEqual:Ent1 indicator",str(lst_Dep2[0]),str(lst_Dep2[1]),r.tk_indicators
                    flagS=1
                    for lst_Dep3 in list_Dep:
                        if str(lst_Dep3[2])=="pobj" and str(lst_Dep3[0])==str(lst_Dep2[1]):
                            r.addIndicators_tk(lst_Dep3[1])
                            listEnt2.append(lst_Dep3[1])
                            NSubjEnt2=getNoun_Subj_of_Sentence(s,r,lst_Dep3[1])
                            ASubjEnt2=getAdj_Subj_of_Sentence(s,r,lst_Dep3[1])
                            r.addIndicatorsList_tk(NSubjEnt2)
                            r.addIndicatorsList_tk(ASubjEnt2)
                            flagSe=1

                elif str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
                    r.addIndicators_tk(lst_Dep2[1])
                    listEnt1.append(lst_Dep2[1])


        # elif str(lst_Dep1[2])=="prep_to" and s._get_token(lst_Dep1[0])._lemma() in listEqual:
        #     for lst_Dep2 in list_Dep:
        #         if str(lst_Dep2[2])=="nsubj" and str(lst_Dep1[0])==str(lst_Dep2[0]):
        #             r.addIndicators_tk(lst_Dep1[1])
        #             r.addIndicators_tk(lst_Dep2[1])
        #             print "Was found subType as belong",str(lst_Dep1[1]),str(lst_Dep2[1])
        #             flagT=1

    if flagSe==1:
        NJsubjEnt1=list(set(NSubjEnt1+ASubjEnt1))
        NJsubjEnt2=list(set(NSubjEnt2+ASubjEnt2))
        j=0
        while (j<len(NJsubjEnt1)):
            listEnt1.append(NJsubjEnt1[j])
            j=j+1

        j=0
        while (j<len(NJsubjEnt2)):
            listEnt2.append(NJsubjEnt2[j])
            j=j+1

        print "flagSe,tk_indicators,listEnt1,listEnt2 ",flagSe,r.tk_indicators,listEnt1,listEnt2
        r.addBoundedList_Vars('tk_Ent1',list(set(listEnt1)))
        r.addBoundedList_Vars('tk_Ent2',list(set(listEnt2)))

    return True

def bindStatus(s,r):
    flagS=0
    flagSe=0
    listStatus=[]
    tks=s._get_tokens()
    for itk in range(len(tks)):
        lma_tk=s._get_token(itk)._lemma()
        lsLemma=entityList("status")
        # print "lsLemma status: ", lma_tk, lsLemma
        for lsitem in range(len(lsLemma)):
            lsItem1=lsLemma[lsitem]
            for subitem1 in range(len(lsItem1)):
                lsItem2=lsItem1[subitem1]
                for subitem2 in range(len(lsItem2)):
                    if lsItem2[subitem2]==lma_tk:
                        print "find lemma list status: ", lma_tk, lsLemma
                        r.addIndicators_tk(itk)
                        listStatus.append(itk)
                        flagS=1

    list_Dep=s.sint._dependencies
    for lst_Dep1 in list_Dep:
        if str(lst_Dep1[2])=="cop":
            for lst_Dep2 in list_Dep:
                if str(lst_Dep2[2])=="root" and isAdjective(s,lst_Dep2[1]) and str(lst_Dep2[1])==str(lst_Dep1[0]):
                    r.addIndicators_tk(lst_Dep2[1])
                    listStatus.append(lst_Dep2[1])
                    flagS=1

                    # NSubj=getNoun_Subj_of_Sentence(s,r,lst_Dep2[0])
                    # ASubj=getAdj_Subj_of_Sentence(s,r,lst_Dep2[0])
                    # r.addIndicators_tk(lst_Dep2[1])
                    # r.addIndicatorsList_tk(NSubj)
                    # r.addIndicatorsList_tk(ASubj)

    # i=0
    # for tk in s._get_tokens():
    #     if posofTkIs(s,i,'IN')and (lemmaofTkIs(s,i,'in')or lemmaofTkIs(s,i,'at')):
    #         print ("The state word is: ", s._get_token(i)._word())
    #         return True
    #     i=i+1
    if flagS==1:
        add_tkType_List(r,listStatus, "tk_Status","ont_Status")

    return True

def bindSynonym(s,r):
    synonymList1=['nickname','synonym']
    synonymList2=['call']
    synonymList3=['abbreviation']

    syn_tk=[]
    listSyn=[]
    flag=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if s._get_token(itk)._lemma() in synonymList1:
            r.addIndicators_tk(itk)
            syn_tk.append(itk)
            flag=1
        elif s._get_token(itk)._lemma() in synonymList2:
            r.addIndicators_tk(itk)
            syn_tk.append(itk)
            flag=2
        elif s._get_token(itk)._lemma() in synonymList3:
            r.addIndicators_tk(itk)
            syn_tk.append(itk)
            flag=3

    lnSyn=len(syn_tk)
    i=0
    while i<lnSyn:
        for lst_Dep in list_Dep:
            if flag==1:
                tempSyn="prep_of"
            elif flag==2:
                tempSyn="dobj"
            elif flag==3:
                tempSyn="nn"
            print "syn_tk, Flag,tempSyn",syn_tk[i],flag,tempSyn

            if (str(lst_Dep[2])==str(tempSyn)):
                if (str(lst_Dep[0])==str(syn_tk[i])):
                    print "syn_tk 1 OKKK",tempSyn
                    listSyn.append(lst_Dep[1])
                    tempSyn=lst_Dep[1]
                    for lst_Dep1 in list_Dep:
                        if (str(lst_Dep1[2])=="nn") and (str(lst_Dep1[0])==str(tempSyn)):
                            tempSyn=lst_Dep1[1]
                            listSyn.append(lst_Dep1[1])
                elif (str(lst_Dep[1])==str(syn_tk[i])):
                    print "syn_tk 2 OKKK",tempSyn
                    listSyn.append(lst_Dep[0])
                    tempSyn=lst_Dep[0]
                    for lst_Dep1 in list_Dep:
                        if (str(lst_Dep1[2])=="nn") and (str(lst_Dep1[1])==str(tempSyn)):
                            tempSyn=lst_Dep1[0]
                            listSyn.append(lst_Dep1[0])

        i=i+1
    lnListSyn=len(listSyn)
    if lnListSyn>0:
        r.addBoundedVars('tk_Syn',listSyn)
        r.addBoundedVars('ont_Syn',None)

    return True


def bindMember(s,r):
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    flag=0
    for itk in range(len(tks)):
        if isMember_tk(s,r,itk) and (lemmaofTkIs(s,itk+1,'of') or lemmaofTkIs(s,itk+1,'in') or lemmaofTkIs(s,itk+1,'to')):
            for lst_Dep in list_Dep:
                if (str(lst_Dep[2])=="prep_of" or str(lst_Dep[2])=="prep_in" or str(lst_Dep[2])=="prep_to" ) and (str(lst_Dep[0])==str(itk)):
                    itkMemb=lst_Dep[1]
                    r.addIndicators_tk(itkMemb)
                    flag=1
    if flag==1:
        r.addBoundedVars('tk_Memb',itkMemb)
        r.addBoundedVars('ont_Memb',None)
    return True


def bindPerson(s,r):
    flag=0
    itk=0
    listPerson=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    while  itk <lnItk:
        lma_tk=s._get_token(itk)._lemma()
        if not(lma_tk.isdigit()):
            if itk+3<lnItk:
                if isNonPerson_3tk(s,r,itk):
                    itk=itk+3
                    continue
                elif isPerson_3tk(s,r,itk):
                    flag=1
                    listPerson.append(itk)
                    listPerson.append(itk+1)
                    listPerson.append(itk+2)
                    itk=itk+3
                    continue
            if ((isPerson_NonRelative(s,r,itk) or isPerson_tk(s,r,itk)) and flag==0):
                flag=1
                listPerson.append(itk)
            elif ((isPerson_NonRelative(s,r,itk) or isPerson_tk(s,r,itk)) and flag!=0):
                listPerson.append(itk)
                flag=2
        itk=itk+1
    print "content of listperson before remove",listPerson
    listPerson=removeListA_listB(r.tk_indicators,listPerson)
    print "content of listperson after remove",listPerson
    add_tkType_List(r,listPerson,"tk_PER","ont_PER")
    return True


def bindAction(s,r):
    nonAction=['belong']
    listConjAction=[]
    listAction=[]
    listAction=getVerb_of_Sentence(s,r)
    for vrb in listAction:
        if s._get_token(vrb)._lemma() in nonAction:
            listAction.remove(vrb)
    for vrb in listAction:
        # print "content of isAction:", vrb
        # if isVerbAux(s,vrb):
        #     print "isVerbAux"
        if isVerbAux_Main(s,vrb):
            listAction.remove(vrb)
    # print "len of Action", len(listAction),listAction
    listConjAction=getConj_and_Subj_of_Sentence(s,r,listAction)
    print "isAction: content of listAction before remove",r.tk_indicators,listAction,listConjAction
    addListA_listB(listAction,listConjAction)
    listAction=removeListA_listB(r.tk_indicators,listAction)
    print "isAction: content of listAction after remove",r.tk_indicators,listAction
    add_tkType_List(r,listAction,"tk_ACT","ont_ACT")

    return True

def bindEffect(s,r):
    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>=1:
        r.addBoundedVars('tk_Efect',listObj)
        r.addBoundedVars('ont_Efect',None)

    return True


def bindWhat(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagSw=0
    flagSwch=0
    flagT=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass") and (not isGEO_tk(s,r,lst_Dep[1]) and (not isPerson_tk(s,r,lst_Dep[1]))):
            itkSubj=lst_Dep[1]
            list_itkType.append(lst_Dep[1])
            flagSs=1

        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            for lst_Dep1 in list_Dep:
                if str(lst_Dep1[2])=="prep_in" and  str(lst_Dep[0])== str(lst_Dep1[0]) and (not isGEO_tk(s,r,lst_Dep1[1]) and (not isPerson_tk(s,r,lst_Dep1[1]))):
                    itkSubj=lst_Dep[1]
                    list_itkType.append(lst_Dep[1])
                    flagSw=1
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and (not isGEO_tk(s,r,lst_Dep[0]) and (not isPerson_tk(s,r,lst_Dep[0]))):
            flagSwch=1

    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj+list_itkType))
    print "bindWhat: Subj list after adding, flagSwch: ",listSubj_itkType, flagSwch
    # print "flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "Obj list after adding",listObj_itkType
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO

    if isWhat_tk(s,r,t) and not isHowmany(s,r,t) and (flagSs==1 or flagS==1):
        add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")

    elif (isWhich(s,r,t)) and flagSwch==1 :
        # and (flagSw==1 or flagSs==1)
        add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
        # bindWhich(s,r)
    elif posofTkIs(s,t,'DT') and not isHowmany(s,r,t) and flagSs==1:
        add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")

    return True


def bindWhen(s,r,t):
    list_itkSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagSw=0
    flagSwn=0
    flagT=0
    list_Dep=s.sint._dependencies
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            list_itkSubj.append(lst_Dep[1])
            flagSs=1
            for lst_Dep1 in list_Dep:
                if (str(lst_Dep1[2])=="prep_of" or str(lst_Dep1[2])=="nn") and str(lst_Dep[0])== str(lst_Dep1[0]) :
                    list_itkType.append(lst_Dep[1])
                    flagSw=1
                if str(lst_Dep[2])=="conj_and" and str(lst_Dep[0])== str(lst_Dep1[0]):
                    list_itkType.append(lst_Dep[1])
                    flagSwn=1

    listSubj_itkType=list(set(listSubj+listConjSubj+list_itkType))
    print "Subj list after adding",listSubj_itkType
    print "flagSs, flagS,flagAS,flagNS,flagCS,flagSw, flagSwn: ",flagSs,  flagS,flagAS,flagNS,flagCS,flagSw, flagSwn
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "Obj list after adding",listObj_itkType
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO

    if (isWhen_tk(s,r,t)) and flagSs==1:
        print " bindWhen cond1!!"
        add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
        return True
    elif isWhat_tk(s,r,t) and flagSwn==1:
        print "bindWhen cond2!!"
        lnIdx=len(list_itkSubj)
        i=0
        while i<lnIdx:
            itkSubj=list_itkSubj.pop()
            i=i+1
            if neofTkIs(s,int(itkSubj),'DUR') or neofTkIs(s,itkSubj,'DAT') or lemmaofTkIs(s,int(itkSubj),'year'):
                add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
                return True
    return True

def bindWhere(s,r,tk):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    listSubjGEO_itkType=[]
    listObjGEO_itkType=[]
    listObj_det_itkType=[]
    listWhereIn_itkType=[]

    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagOd=0
    flagOo=0
    flag_in=0

    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_in":
            itkLoc=lst_Dep[1]
            flag_in=1
            listWhereIn_itkType=list(set(makeDetW_List(s,r,itkLoc)))
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass") and isGEO_tk(s,r,lst_Dep[1]):
            itkSubj=lst_Dep[1]
            flagSs=1
            listSubjGEO_itkType=list(set(makeSubj_List(s,r,itkSubj)))
        if (str(lst_Dep[2])=="pobj" or str(lst_Dep[2])=="pobjpass") and isGEO_tk(s,r,lst_Dep[1]):
            itkObj=lst_Dep[1]
            flagOo=1
            listObjGEO_itkType=list(set(makeObj_List(s,r,itkObj)))
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and isGEO_tk(s,r,lst_Dep[0]):
            flagOd=1
            itkObjd=lst_Dep[0]
            listObj_det_itkType=list(set(makeDetW_List(s,r,itkObjd)))


    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj))
    print "bindWhere:flagS,flagAS,flagNS,flagCS,flagSs,flag_in, -listSubj_itkType-, -listWhereIn_itkType-",flagS,flagAS,flagNS,flagCS,flagSs,flag_in,listSubj_itkType, listWhereIn_itkType
    listObj_itkType=list(str(listObj+listNounObj+listAdjObj+listConjObj))

    if tk!="":
        t=tk
        if isWhere_tk(s,r,t) and flag_in==1:
            print "flag_in is OK: ",listWhereIn_itkType
            add_tkType_List(r,listWhereIn_itkType,"tk_Type","ont_Type")
            return True
        elif isWhere_tk(s,r,t) and flagS==1:
            add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
        elif posofTkIs(s,t,'DT') and flagSs==1:
            add_tkType_List(r,listSubjGEO_itkType,"tk_Type","ont_Type")
        elif isInWhich(s,r,t):
            if flagOd==1:
                print "flagOd"
                print "listObj_det_itkType",r.tk_indicators,listObj_det_itkType,r.boundedVars
                add_tkType_List(r,listObj_det_itkType,"tk_Type","ont_Type")
            elif flagSs==1:
                print "flagSs"
                add_tkType_List(r,listSubjGEO_itkType,"tk_Type","ont_Type")
        elif isWhich(s,r,t):
            if flagOd==1:
                print "flagOd isWhich"
                add_tkType_List(r,listObj_det_itkType,"tk_Type","ont_Type")
                return True
            if flagOo==1:
                print "flagOd isWhich"
                add_tkType_List(r,listObjGEO_itkType,"tk_Type","ont_Type")
                return True
            if t==0 and flagSs==1:
                add_tkType_List(r,listSubjGEO_itkType,"tk_Type","ont_Type")
                return True
            elif t>1 and flagOd==1:
                add_tkType_List(r,listSubjGEO_itkType,"tk_Type","ont_Type")
                return True
        elif isWhat_tk(s,r,t) and flagSs==1:
                add_tkType_List(r,listSubjGEO_itkType,"tk_Type","ont_Type")
        return True
    else:
        tks=s._get_tokens()
        for itk in range(len(tks)):
            if isWhich(s,r,itk):
                return bindWhere(s,r,itk)
    return True


def bindWhere_in(s,r):
    # from rule import currentRule

    global currentRule
    Qvar=currentRule
    Flag=0
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_in":
            itk=lst_Dep[1]
            Flag=1

    if Flag==1:
        tks=s._get_tokens()
        tk = tks[itk]
        if tk._ne()=='LOC' or tk._ne()=='LOCATION':
            # print "Was found Location in token as Entity:", itk
            Qvar.boundedVars['tk_WhereIn']=itk
            Qvar.boundedVars['ont_WhereIn']=None
            # print "Was found Location in Token:", itk,Qvar.boundedVars
        else:
            # print "Was Not found Location in token as Entity:", itk
            Qvar.boundedVars['tk_WhereIn']=None
            Qvar.boundedVars['ont_WhereIn']=None
            # print "Was Not found Location in Token as Entity::", itk,Qvar.boundedVars

    return True

def bindWho(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    list_Memb=[]
    listSubjPER_itkType=[]
    listObjPER_itkType=[]
    listObj_det_itkType=[]
    flagS=0
    flagSs=0
    flagSd=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagOd=0
    flagOo=0
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="agent"):
            if isPerson_tk(s,r,lst_Dep[1]):
                itkSubj=lst_Dep[1]
                flagSs=1
                print "itkSubj, listSubjPER_itkType",itkSubj,listSubjPER_itkType
                listSubjPER_itkType=list(set(makeSubj_List(s,r,itkSubj)))
                print "listSubjPER_itkType after return",listSubjPER_itkType
            elif not isVerb(s,lst_Dep[0]):
                if isPerson_tk(s,r,lst_Dep[0]):
                    itkSubj=lst_Dep[0]
                    flagSd=1
                    listSubjPER_itkType=list(set(makeSubj_List(s,r,itkSubj)))
                    print "listSubjPER_itkType for Not isVerb():",listSubjPER_itkType

        if (str(lst_Dep[2])=="pobj" or str(lst_Dep[2])=="pobjpass") and isPerson_tk(s,r,lst_Dep[1]):
            itkObj=lst_Dep[1]
            flagOo=1
            listObjPER_itkType=list(set(makeObj_List(s,r,itkObj)))
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and isPerson_tk(s,r,lst_Dep[0]):
            flagOd=1
            itkObjd=lst_Dep[0]
            listObj_det_itkType=list(set(makeDetW_List(s,r,itkObjd)))

    # print "flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    print "flagOd,flagOo,flagSs",flagOd,flagOo,flagSs

    listSubj_itkType=listSubj+listNounSubj+listAdjSubj+listConjSubj
    # print "bindWho: Subj list after adding",listSubj_itkType
    # print "bindWho:flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "bindWho:Obj list after adding",listObj_itkType
    # print "bindWho: flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    print "listSubjPER_itkType before isWho and isWho_tk(s,r,t): ",listSubjPER_itkType, isWho_tk(s,r,t)
    if isWho_tk(s,r,t):
        print "listSubjPER_itkType",listSubjPER_itkType
        add_tkType_List(r,listSubjPER_itkType,"tk_Type","ont_Type")
        return True
    elif posofTkIs(s,t,'DT') and (flagSs==1 or flagSd==1):
        add_tkType_List(r,listSubjPER_itkType,"tk_Type","ont_Type")
        return True
    elif posofTkIs(s,t,'DT') and isMember_tk(s,r,t+1):
        list_Memb.append(t+1)
        add_tkType_List(r,list_Memb,"tk_Type","ont_Type")
        return True
    elif isWhich_tk(s,r,t):
        if flagOd==1:
            add_tkType_List(r,listObj_det_itkType,"tk_Type","ont_Type")
            return True
    return True

def bindWhich(s,r):
    cmpObj=[]
    objList=[]
    objAdj=[]
    objNoun=[]
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which"):
            objList.append(lst_Dep[0])
            objAdj=getAdj_Obj_of_Sentence(s,r,lst_Dep[0])
            objNoun=getNoun_Obj_of_Sentence(s,r,lst_Dep[0])

            for lst_Dep1 in list_Dep:
                if str(lst_Dep1[2])=="dep" and str(lst_Dep1[0])==str(lst_Dep[0]):
                    objList.append(lst_Dep1[1])


    cmpObj=objList+objAdj+objNoun
    cmpObj=list(set(cmpObj))
    if len(cmpObj)==1:
        objItem=cmpObj.pop()
        # print "len(objList)==1: function Object of list is", objItem
        r.addBoundedVars('tk_Type',objItem)
        r.addBoundedVars('ont_Type',None)
        r.addIndicators_tk(objItem)
    elif len(cmpObj)>1:
        # print "len(objList)>1: function Object of list is", cmpObj
        r.addBoundedVars('tk_Type',cmpObj)
        r.addBoundedVars('ont_Type',None)
        lncmpObj=len(cmpObj)
        i=0
        while i<lncmpObj:
            r.addIndicators_tk(cmpObj[i])
            i=i+1

    return True

def bindQuantifier_tk(s,r,itk):
    flagQ=0
    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="advmod" and str(lst_Dep[1])==str(itk):
            for lst_Dep1 in list_Dep:
                if (str(lst_Dep1[2])=="attr" or str(lst_Dep1[2])=="advmod") and str(lst_Dep[0])==str(lst_Dep1[1]):
                    flagQ=1

    if lemmaofTkIs(s,itk,'how')and flagQ==1:
            r.boundedVars['tk_Type']=itk+1
            r.boundedVars['ont_Type']=None
            r.addIndicators_tk(itk)
    return True

def bindHowmuch(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_Dep=s.sint._dependencies
    flagS=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagWh=0
    flagT=0
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            if (lemmaofTkIs(s,lst_Dep[1],'amount')):
                flagWh=1

    listSubj_itkType=listSubj+listNounSubj+listAdjSubj+listConjSubj
    # print "bindHowmany: Subj list after adding",listSubj_itkType
    # print "bindHowmany:flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "bindHowmany:Obj list after adding",listObj_itkType
    # print "bindHowmany: flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    if lemmaofTkIs(s,t,'what'):
        r.addIndicators_tk(t)
        if flagWh==1:
            listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj_itkType)
            # print "What  matched, after remove: listSubj_itkType,r.tk_indicators ",listSubj_itkType,r.tk_indicators
            add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
            # print "after addtk,listSubj_itkType,r.tk_indicators",listSubj_itkType,r.tk_indicators
            return True
        # elif flagCS==1:
        #     print "Is  actually HMany  in What!!!"
        #     lnIdx=len(listConjSubj)
        #     i=0
        #     while i<lnIdx:
        #         r.addIndicators_tk(listConjSubj.pop())
        #         i=i+1
        #     return True
    elif posofTkIs(s,t,'DT') and flagCS==1:
        listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj_itkType)
        add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
        return True
    if isHowmuch_tk(s,r,t):
        r.addIndicators_tk(t)
        r.addIndicators_tk(t+1)
        if flagO==1:
            listObj_itkType=removeListA_listB(r.tk_indicators,listObj)
            # print "How many matched, after remove: listObj_itkType,r.tk_indicators ",listObj_itkType,r.tk_indicators
            add_tkType_List(r,listObj_itkType,"tk_Type","ont_Type")
            # print "after addtk,listObj_itkType,r.tk_indicators",listObj_itkType,r.tk_indicators
            return True
        elif flagS==1:
            listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj)
            add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
            return True

    return True

def bindHowmany(s,r,t):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_Dep=s.sint._dependencies
    flagS=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagWh=0
    flagT=0
    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass"):
            if (lemmaofTkIs(s,lst_Dep[1],'amount')):
                flagWh=1

    listSubj_itkType=listSubj+listNounSubj+listAdjSubj+listConjSubj
    # print "bindHowmany: Subj list after adding",listSubj_itkType
    # print "bindHowmany:flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    listObj_itkType=listObj+listNounObj+listAdjObj+listConjObj
    # print "bindHowmany:Obj list after adding",listObj_itkType
    # print "bindHowmany: flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    if lemmaofTkIs(s,t,'what'):
        r.addIndicators_tk(t)
        if flagWh==1:
            listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj_itkType)
            # print "What  matched, after remove: listSubj_itkType,r.tk_indicators ",listSubj_itkType,r.tk_indicators
            add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
            # print "after addtk,listSubj_itkType,r.tk_indicators",listSubj_itkType,r.tk_indicators
            return True
        # elif flagCS==1:
        #     print "Is  actually HMany  in What!!!"
        #     lnIdx=len(listConjSubj)
        #     i=0
        #     while i<lnIdx:
        #         r.addIndicators_tk(listConjSubj.pop())
        #         i=i+1
        #     return True
    elif posofTkIs(s,t,'DT') and flagCS==1:
        listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj_itkType)
        add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
        return True
    if isHowmany_tk(s,r,t):
        r.addIndicators_tk(t)
        r.addIndicators_tk(t+1)
        if flagO==1:
            listObj_itkType=removeListA_listB(r.tk_indicators,listObj_itkType)
            # print "How many matched, after remove: listObj_itkType,r.tk_indicators ",listObj_itkType,r.tk_indicators
            add_tkType_List(r,listObj_itkType,"tk_Type","ont_Type")
            # print "after addtk,listObj_itkType,r.tk_indicators",listObj_itkType,r.tk_indicators
            return True
        elif flagS==1:
            listSubj_itkType=removeListA_listB(r.tk_indicators,listSubj_itkType)
            add_tkType_List(r,listSubj_itkType,"tk_Type","ont_Type")
            return True

    return True


def bindEntity(s,r):
    listEnt=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    itk=0
    while itk <lnItk:
        if isEntity_3tk(s,r,itk):
            listEnt.append(itk)
            listEnt.append(itk+1)
            listEnt.append(itk+2)
            itk=itk+2
        elif isEntity_2tk(s,r,itk):
            listEnt.append(itk)
            listEnt.append(itk+1)
            itk=itk+1
        elif isNoun(s,itk) and (not isGEO_tk(s,r,itk)) and (not isPerson_tk(s,r,itk)) and not (itk in r.tk_indicators):
            listEnt.append(itk)
        itk=itk+1

    listEnt=removeListA_listB(r.tk_indicators,listEnt)
    # print "isEntity: content of listEnt after remove",r.tk_indicators,listEnt
    lnIdx=len(listEnt)
    if lnIdx>0:
        addListA_listB(r.tk_indicators,listEnt)
        # print "content of r.tk_indicators after add",r.tk_indicators,listEnt
        r.addBoundedVars('tk_Ent',listEnt)
        r.addBoundedVars('ont_Ent',None)

    return True

def bindSecond_Entity(s,r):
    # from rule import currentRule

    global currentRule
    Qvar=currentRule
    flag=0
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if isNoun(s,itk) and (not (itk in r.tk_indicators)):
            if flag==1:
                Qvar.boundedVars['tk_SecEnt']=itk
                Qvar.boundedVars['ont_SecEnt']=None
                r.addIndicators_tk(itk)
                return True
            else:
                flag=1
    return True


def bindGEO_Property(s,r,tk):

    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    if tk=='':
        for itk in range(len(tks)):
            print "tk",itk
            if neofTkIs(s,itk,'LOC'):
                tk_GEO=itk
                for lst_Dep in list_Dep:
                    if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(tk_GEO) and (isNoun(s,lst_Dep[0])):
                        r.boundedVars['tk_LocProp']=itk
                        r.boundedVars['ont_LocProp']=None
                        return True
    else:
        if neofTkIs(s,tk,'LOC'):
            tk_GEO=tk
            for lst_Dep in list_Dep:
                if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(tk_GEO) and (isNoun(s,lst_Dep[0])):
                    r.boundedVars['tk_GEOProp']=tk_GEO
                    r.boundedVars['ont_GEOProp']=None
                    return True
    return True


def bindGEO(s,r):
    flag=0
    itk=0
    listGEO=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    while itk<lnItk :
        lma_tk=s._get_token(itk)._lemma()
        if not(lma_tk.isdigit()) and not (itk in r.tk_indicators):
            if (itk+3 <lnItk) and isNonGEO_2tk_3tk(s,r,itk)==3:
                itk=itk+2
            if (itk+2 <lnItk) and isNonGEO_2tk_3tk(s,r,itk)==2:
                itk=itk+1
            elif isGEO_tk(s,r,itk):
                listGEO.append(itk)

        itk=itk+1
    # print "len of GEO", len(listGEO),listGEO
    print "bindGEO: content of listGEO before remove",r.tk_indicators,listGEO
    listGEO=removeListA_listB(r.tk_indicators,listGEO)
    print "bindGEO: content of listGEO after remove",r.tk_indicators,listGEO
    add_tkType_List(r,listGEO,"tk_GEO","ont_GEO")
    return True


def bindORG(s,r):
    flag=0
    itk=0
    listORG=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    while itk<lnItk :
        lma_tk=s._get_token(itk)._lemma()
        if not (itk in r.tk_indicators):
            if (itk+3 <lnItk) and isORG_2tk_3tk(s,r,itk)==3:
                listORG.append(itk)
                listORG.append(itk+1)
                listORG.append(itk+2)
                itk=itk+2
                flag=2
            if (itk+2 <lnItk) and isORG_2tk_3tk(s,r,itk)==2:
                listORG.append(itk)
                listORG.append(itk+1)
                itk=itk+1
                flag=2
            elif isORG_tk(s,r,itk) and flag==0:
                tempItk=itk
                listORG.append(itk)
                flag=1
            elif isORG_tk(s,r,itk) and flag!=0:
                listORG.append(itk)
                flag=2

        itk=itk+1
    # print "len of ORG", len(listORG),listORG
    # print "isGEO: content of listORG before remove",r.tk_indicators,listORG
    listORG=removeListA_listB(r.tk_indicators,listORG)
    # print "isORG: content of listORG after remove",r.tk_indicators,listORG
    lnIdx=len(listORG)
    if lnIdx>0:
        listIndicator=addListA_listB(r.tk_indicators,listORG)
        # print "content of r.tk_indicators,listIndicator,listORG  after adding",r.tk_indicators,listIndicator,listORG
        if flag==1:
            r.addBoundedVars('tk_ORG',tempItk)
            r.addBoundedVars('ont_ORG',None)
        elif flag==2:
            r.addBoundedVars('tk_ORG',listORG)
            r.addBoundedVars('ont_ORG',None)
    return True

def bindTimeRelation(s,r):
    listNounDur=[]
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if posofTkIs(s,itk,'IN'):
            if lemmaofTkIs(s,itk,'after'):
                itkAfter=itk
            elif lemmaofTkIs(s,itk,'before'):
                itkBefore=itk
            elif lemmaofTkIs(s,itk,'between'):
                itkBetween=itk
            elif lemmaofTkIs(s,itk,'than'):
                itkThan=itk
            elif lemmaofTkIs(s,itk,'within'):
                itkWithin=itk


    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_after" :
            if neofTkIs(s,lst_Dep[1],'PER'):
                for lst_Dep1 in list_Dep:
                    if str(lst_Dep1[2])=="nsubj" and  str(lst_Dep[0])==str(lst_Dep1[0]) and neofTkIs(s,lst_Dep1[1],'PER'):
                        r.addBoundedVars('tk_FPer',str(lst_Dep1[1]))
                        r.addBoundedVars('tk_SPer',str(lst_Dep[1]))
                        r.addBoundedVars('tk_After',str(itkAfter))
                        r.addIndicators_tk(itkAfter)
                        r.addIndicators_tk(lst_Dep1[1])
                        r.addIndicators_tk(lst_Dep1[1])
            else:
                r.addBoundedVars('tk_FDate',str(lst_Dep[0]))
                r.addBoundedVars('tk_SDate',str(lst_Dep[1]))
                r.addBoundedVars('tk_After',str(itkAfter))
                r.addIndicators_tk(itkAfter)
                r.addIndicators_tk(lst_Dep[0])
                r.addIndicators_tk(lst_Dep[1])


        elif str(lst_Dep[2])=="prep_before":
            return True

        elif str(lst_Dep[2])=="prep_between":
            if neofTkIs(s,lst_Dep[1],'DAT'):
                for lst_Dep1 in list_Dep:
                    if str(lst_Dep1[2])=="conj_and" and  str(lst_Dep[1])==str(lst_Dep1[0]):
                        r.addBoundedVars('tk_FDate',str(lst_Dep1[0]))
                        r.addBoundedVars('tk_SDate',str(lst_Dep1[1]))
                        r.addBoundedVars('tk_Between',str(itkBetween))
                        r.addIndicators_tk(itkBetween)
                        r.addIndicators_tk(lst_Dep1[0])
                        r.addIndicators_tk(lst_Dep1[1])
        elif str(lst_Dep[2])=="prep_than":
            r.addBoundedVars('tk_FMetric',str(lst_Dep[0]))
            r.addBoundedVars('tk_SMetric',str(lst_Dep[1]))
            r.addBoundedVars('tk_Than',str(itkThan))
            r.addIndicators_tk(itkThan)
            r.addIndicators_tk(lst_Dep[0])
            r.addIndicators_tk(lst_Dep[1])

        elif str(lst_Dep[2])=="prep_within":
            if neofTkIs(s,lst_Dep[1],'DUR'):
                print "token for DUR",lst_Dep[1]
                listNounDur=getDuration_of_TR(s,r,lst_Dep[1])
                add_tkType_List(r,listNounDur,"tk_DUR","ont_DUR")
                print "During list",listNounDur
                return True
    return True


def bindDate(s):
    # from rule import currentRule
    global currentRule

    Qvar=currentRule
    tks=s._get_tokens()
    for itk in range(len(tks)):
        if neofTkIs(s,itk,'DAT'):
            Qvar.boundedVars['tk_Date']=itk
            Qvar.boundedVars['ont_Date']=None
            return True
    return True

def bindTemp(s,r):
    tks=s._get_tokens()
    listTemp=[]
    for itk in range(len(tks)):
        if (neofTkIs(s,itk,'DUR')or neofTkIs(s,itk,'SET')):
            listTemp.append(itk)
    listTemp=removeListA_listB(r.tk_indicators,listTemp)
    for item in listTemp:
        r.addIndicators_tk(item)
    if len (listTemp)>0:
        r.addBoundedVars('tk_Temp',listTemp)
        r.addBoundedVars('ont_Temp',None)
    return True

def bindQuantifier(s,r):

    tks=s._get_tokens()
    for itk in range(len(tks)):
        if(lemmaofTkIs(s,itk,'all')or lemmaofTkIs(s,itk,'any')or lemmaofTkIs(s,itk,'some')or neofTkIs(s,itk,'NUM') or neofTkIs(s,itk,'ORD')):
            # print ("The binded tk_Quant Quanifier word is: ", s._get_token(itk)._word())
            r.addBoundedVars('tk_Quant',itk)
            r.addBoundedVars('ont_Quant',None)

            return True
    return True


def bindProperties(s,r):
    tks=s._get_tokens()
    listProps=[]
    flag=0
    list_Dep=s.sint._dependencies
    lnItk=len(tks)
    for itk in range(len(tks)):
        if itk+1<=len(tks):
            if isAtomic_Property(s,r,itk) and isAtomic_Property(s,r,itk+1):
                listProps.append(itk)
                # listProps.append(itk+1)
            elif isAdjective(s,itk) or posofTkIs(s,itk,'CD') or posofTkIs(s,itk,'RB') or neofTkIs(s,itk,'NUM'):
                listProps.append(itk)
            elif posofTkIs(s,itk,'VBG'):
                for lst_Dep in list_Dep:
                    if str(lst_Dep[2])=="amod" and str(lst_Dep[1])==str(itk) and (posofTkIs(s,lst_Dep[0],'NN') or (posofTkIs(s,lst_Dep[0],'NNS'))):
                        listProps.append(itk)

    listProps=sorted(list(set(listProps)))
    listProps=removeListA_listB(r.tk_indicators,listProps)
    add_tkType_List(r,listProps,"tk_Prop","ont_Prop")
    # if len (listProps)==1:
    #     addListA_listB(r.tk_indicators,listProps)
    #     r.addBoundedVars('tk_Prop',listProps[0])
    #     r.addBoundedVars('ont_Props',None)
    #     # print "Content of isProperties  after binding call",listProps,r.tk_indicators
    # elif len (listProps)>1:
    #     addListA_listB(r.tk_indicators,listProps)
    #     r.addBoundedVars('tk_Prop',listProps)
    #     r.addBoundedVars('ont_Props',None)

    return True

def bindCompound_Properties(s,r):
    # from rule import currentRule
    # global currentRule
    # Qvar=currentRule

    tks=s._get_tokens()
    lnItk=len(tks)
    maxLenProp1=0
    maxLenProp2=0
    maxLenProp3=0

    listCmpProps1=[]
    listCmpProps2=[]
    listCmpProps3=[]
    flag1=0
    flag2=0
    flag3=0

    list_Dep=s.sint._dependencies
    for itk in range(len(tks)):
        if isAtomic_CompProperty(s,r,itk)  and maxLenProp1==0 and flag1==0:
            flag1=1
            listCmpProps1.append(itk)
            maxLenProp1=maxLenProp1+1

        elif isAtomic_CompProperty(s,r,itk) and maxLenProp1!=0 and  maxLenProp2==0 and flag1==0 and flag2==1 :
            listCmpProps2.append(itk)
            maxLenProp2=maxLenProp2+1
        elif isAtomic_CompProperty(s,r,itk) and maxLenProp1!=0 and  maxLenProp2!=0 and  maxLenProp3==0 and flag1==0 and flag2==0 and flag3==1 :
            listCmpProps3.append(itk)
            maxLenProp3=maxLenProp3+1

        elif ((isAtomic_CompProperty(s,r,itk)) or posofTkIs(s,itk,'JJR') or posofTkIs(s,itk,'CD') or lemmaofTkIs(s,itk,'than') or neofTkIs(s,itk,'NUM')) and maxLenProp1!=0 and flag1!=0:
            listCmpProps1.append(itk)
            maxLenProp1=maxLenProp1+1
        elif ((isAtomic_CompProperty(s,r,itk) ) or posofTkIs(s,itk,'JJR') or posofTkIs(s,itk,'CD') or lemmaofTkIs(s,itk,'than') or neofTkIs(s,itk,'NUM')) and maxLenProp2!=0 and flag2!=0:
            listCmpProps2.append(itk)
            maxLenProp2=maxLenProp2+1
            flag2=2
        elif ((isAtomic_CompProperty(s,r,itk) ) or posofTkIs(s,itk,'JJR') or posofTkIs(s,itk,'CD') or lemmaofTkIs(s,itk,'than') or neofTkIs(s,itk,'NUM')) and maxLenProp3!=0 and flag3!=0:
            listCmpProps3.append(itk)
            maxLenProp3=maxLenProp3+1
            flag3=2

        elif (lemmaofTkIs(s,itk,'of') or lemmaofTkIs(s,itk,'in') or lemmaofTkIs(s,itk,'with') or lemmaofTkIs(s,itk,'on') or lemmaofTkIs(s,itk,'has') or lemmaofTkIs(s,itk,'have'))and maxLenProp1!=0  and flag1!=0:
            flag1=0
            flag2=1
        elif (lemmaofTkIs(s,itk,'of') or lemmaofTkIs(s,itk,'in') or lemmaofTkIs(s,itk,'with') or lemmaofTkIs(s,itk,'on') or lemmaofTkIs(s,itk,'has') or lemmaofTkIs(s,itk,'have')) and maxLenProp2!=0  and flag2!=0:
            flag1=0
            flag2=0
            flag3=1
        elif lemmaofTkIs(s,itk,'the') and (maxLenProp1!=0  or maxLenProp2!=0 or maxLenProp3!=0) :
            print "The in token",itk,flag1,flag2
            continue
        elif not (isAtomic_CompProperty(s,r,itk)) and flag1==0 and (flag2>0 or flag3>0):
            break
        elif flag1==1:
            flag1=0
            flag2=0
            flag3=0
            maxLenProp1=0
            maxLenProp2=0
            maxLenProp3=0
            listCmpProps1=removeListItem(listCmpProps1)

    listCmpProps1=removeListA_listB(r.tk_indicators,listCmpProps1)
    listCmpProps2=removeListA_listB(r.tk_indicators,listCmpProps2)
    listCmpProps3=removeListA_listB(r.tk_indicators,listCmpProps3)
    listCmpProps=listCmpProps1+listCmpProps2+listCmpProps3

    # print "Staus of flag1,flag2,falf3, r,indicator in BINdComp",flag1,flag2,flag3,r.tk_indicators
    # print "listCmpProps1,listCmpProps2,listCmpProps3,listCmpProps",listCmpProps1,listCmpProps2,listCmpProps3,listCmpProps

    if flag3==0:
        if flag1==0 and flag2>=1:
            if len (listCmpProps1)>0 or len (listCmpProps2)>0 :
                # print "final 1 bindCMP detected!!!"
                if len(listCmpProps) >1:
                    r.addBoundedVars('tk_CmpProp',listCmpProps)
                else:
                    r.addBoundedVars('tk_CmpProp',listCmpProps[0])

                r.addBoundedVars('ont_CmpProp',None)
                for item in listCmpProps:
                    r.addIndicators_tk(item)
                # print "Ok!!Content of listprops and indicate before binding compound call:",listCmpProps1,listCmpProps2,listCmpProps,r.tk_indicators
                return True
    elif flag3>=0:
        if len (listCmpProps1)>0 or len (listCmpProps2)>0 or (len (listCmpProps3)>0):
            print "final 2 bindCMP detected!!!"
            if len(listCmpProps) >1:
                r.addBoundedVars('tk_CmpProp',listCmpProps)
            else:
                r.addBoundedVars('tk_CmpProp',listCmpProps[0])
            r.addBoundedVars('ont_CmpProp',None)
            for item in listCmpProps:
                r.addIndicators_tk(item)
            # print "Ok!!Content of listprops and indicate before binding compound call:",listCmpProps1,listCmpProps2,listCmpProps,r.tk_indicators
            return True

    return True



def bindPers_Property(s,r,tk):
    # from rule import currentRule
    global currentRule
    Qvar=currentRule

    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    if tk=='':
        for itk in range(len(tks)):
            print "tk",itk
            if neofTkIs(s,itk,'PER') or isPersonInWN(s,r,itk):
                tk_per=itk
                for lst_Dep in list_Dep:
                    if str(lst_Dep[2])=="prep_of" and str(lst_Dep[1])==str(tk_per) and (posofTkIs(s,lst_Dep[0],'NN') or (posofTkIs(s,lst_Dep[0],'NNS'))):
                        # print "Binded tk_PersProp for person property: ",lst_Dep
                        currentRule.boundedVars['tk_PersProp']=itk
                        currentRule.boundedVars['ont_PersProp']=None

                        return True
    else:
        if neofTkIs(s,tk,'PER') or isPersonInWN(s,r,tk):
            tk_per=tk
            for lst_Dep in list_Dep:
                if str(lst_Dep[2])=="prep_of" and str(lst_Dep[1])==str(tk_per) and (posofTkIs(s,lst_Dep[0],'NN') or (posofTkIs(s,lst_Dep[0],'NNS'))):
                    # print "Binded tk_PersProp for person property: ",lst_Dep
                    Qvar.boundedVars['tk_PersProp']=tk_per
                    Qvar.boundedVars['ont_PersProp']=None

                    return True
    return True

