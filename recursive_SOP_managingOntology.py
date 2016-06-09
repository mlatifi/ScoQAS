__author__ = 'majid'

import string
import re
import rdflib
import rdfextras
from rdflib import Literal,XSD,plugin,BNode, URIRef
from rdflib import Namespace
from rdflib.namespace import RDF, FOAF,RDFS
import tempfile
from tempfile import mkdtemp
from rdflib.collection import Collection
from pprint import pprint
from rdflib.plugins import sparql
from rdflib.util import check_predicate, check_subject, check_object
from rdflib.store import Store, NO_STORE, VALID_STORE
from auxiliarWN import *
from rdflib.resource import Resource
from rdflib.term import Node, URIRef, Genid
from SPARQLWrapper import SPARQLWrapper, JSON
from urlparse import urlparse
import os
from graphSentence import *
from graphviz import Digraph,Graph
import networkx as nx
import matplotlib.pyplot as plt
from managingOntology import *




def retrievingSubclass(WorkingDirectory,StartClass,persName):
    global currentRule
    from rule import currentRule
    Qvar=currentRule

    g = rdflib.Graph()
    g.parse(WorkingDirectory + "QA-Enterprise.rdfs")
    SubclassList={}
    Strtemp={}
    idx=0
    Flag=0

    for subj, pred, obj in g:
        pure_obj=obj
        pure_StartClass=StartClass
        try:
            pure_obj=pure_class_name(obj)
            pure_StartClass=pure_class_name(StartClass)

        except:
            # print "Pur name Passed!!!e"
            pass

        # else:
        #     print "Is not alpha numeric",idx
        if (pure_StartClass in pure_obj) and (pred.rsplit('#')[-1]=="subClassOf"):
            # print (pred,"subject is:", subj, " and object is :", obj)
            #print ("Person class found:...", subj.rsplit('/rdf')[-1])
            SubclassList[idx]=subj.rsplit('/rdf')[-1]
            #Strtemp[idx]=SubclassList[idx]
            SubclassList[idx]=Literal(SubclassList[idx], datatype=XSD.string)
            SubclassList[idx]=SubclassList[idx].value
            SubclassList[idx]=str(SubclassList[idx])
            Strtemp[idx]=SubclassList[idx]
            StrLower=string.lower(Strtemp[idx])
            if (string.find(StrLower,persName)==0):
                print (persName, "token in sentence was found in sub class:", SubclassList[idx])
                Qvar.boundedClassPerson[idx]=SubclassList[idx]
                Flag=1
            if retrievingSlot(WorkingDirectory,Strtemp[idx],persName):

                Flag=1
            idx=idx+1

        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    if (idx>0 and Flag==0):
        j=0
        #print ("All of the subclass for Class:", StartClass, "are:")

        while j<idx:
            #print ("No.",j+1,":",Strtemp[j])
            if retrievingSubclass(WorkingDirectory,SubclassList[j],persName):
                return True
            j=j+1
    else:
        if Flag==1:
           return True
    return False





def retrieveClassesWhere_in(WorkingDirectory,StartClassWhere,locName):
    global currentRule
    from rule import currentRule

    Qvar=currentRule

    g = rdflib.Graph()
    g.parse(WorkingDirectory + "QA-Enterprise.rdfs")
    SubclassList={}
    Strtemp={}
    idx=0
    Flag=0
    lst_Loc=str(locName)

    for subj, pred, obj in g:
        pure_StartClassWhere=StartClassWhere
        pure_obj=obj
        # try:
        #     pure_obj=pure_class_name(obj)
        #     pure_StartClassWhere=pure_class_name(StartClassWhere)
        #
        # except:
        #     pass

        if (pure_StartClassWhere in pure_obj) and (pred.rsplit('#')[-1]=="subClassOf"):
            print ("pure_StartClassWhere,pure_obj",pure_StartClassWhere,"\t","obj:",obj)
            print ("subject:","\t",subj)
            print ("OKKK!!, predicate, Location",lst_Loc, pred)
            # print ("Person class found:...", subj.rsplit('/rdf')[-1])
            SubclassList[idx]=subj.rsplit('/rdf')[-1]
            #Strtemp[idx]=SubclassList[idx]
            SubclassList[idx]=Literal(SubclassList[idx], datatype=XSD.string)
            SubclassList[idx]=SubclassList[idx].value
            SubclassList[idx]=str(SubclassList[idx])
            Strtemp[idx]=SubclassList[idx]
            StrLower=string.lower(Strtemp[idx])
            if (string.find(StrLower,lst_Loc)==0):
                print "Start_Class was find in Object for subject",pure_StartClassWhere, StrLower,lst_Loc
                print (locName, "token in sentence for location was found in sub class, lst_Loc[i]:", SubclassList[idx],lst_Loc)
                Qvar.boundedClassWhere_in[idx]=SubclassList[idx]
                Flag=1

    #         if retrievingSlotWhere_in(WorkingDirectory,Strtemp[idx],locName):
    #             Flag=1
            idx=idx+1
    #
    #     if (subj, pred, obj) not in g:
    #         raise Exception("It better be!")
    #
    #
    if (idx>0 and Flag==0):
        j=0
        while j<idx:
            if retrieveClassesWhere_in(WorkingDirectory,SubclassList[j],lst_Loc):
                return True
            j=j+1
    else:
        if Flag==1:
            return True
            # i=i+1

    return False

    # if (idx>0 and Flag==0):
    #     return idx,SubclassList
    # elif Flag==1:
    #         return 0,0
    #
    # return -1,-1

    # return idx,Flag

def retrievingSlot(WorkingDirectory,StartClass,persName):
    global currentRule
    from rule import currentRule
    Qvar=currentRule


    gProp = rdflib.Graph()
    gProp.parse(WorkingDirectory + "QA-Enterprise.rdfs")

    SubPropList={}
    Strtemp={}
    idx=0
    Flag=0

    for subj, pred, obj in gProp:
        #print ("All search for  :",StartClass, pred,"subject is:", subj, " and object is :", obj)
        if (pred.rsplit('#')[-1]=="domain") and (re.match(StartClass,obj.rsplit('/rdf')[-1])):
            SubPropList[idx]=subj.rsplit('/rdf')[-1]
            SubPropList[idx]=Literal(SubPropList[idx], datatype=XSD.string)
            SubPropList[idx]=SubPropList[idx].value
            SubPropList[idx]=str(SubPropList[idx])
            Strtemp[idx]=SubPropList[idx]
            StrLower=string.lower(SubPropList[idx])
            if (string.find(StrLower,persName)==0):
                print (idx,":",SubPropList[idx]," was found property in subclass: ", obj.rsplit('/rdf')[-1])
                Qvar.boundedSlotPerson[idx]=SubPropList[idx]
                Flag=1
            if (StartClass!='.*$') and (retrievingInstance(WorkingDirectory,StartClass,Strtemp[idx],persName)):
                Flag=1
            idx=idx+1
        #
        if (subj, pred, obj) not in gProp:
            raise Exception("It better be!")

    if (Flag==1):
        print ("Note: Token was find in property list in the sub class:", StartClass, "for token:",persName)
        return True
    else:
        return False



def retrievingSlotWhere_in(WorkingDirectory,StartClassWhere,locName):
    global currentRule
    from rule import currentRule
    Qvar=currentRule


    gProp = rdflib.Graph()
    gProp.parse(WorkingDirectory + "QA-Enterprise.rdfs")

    SubPropList={}
    Strtemp={}
    idx=0
    Flag=0

    for subj, pred, obj in gProp:
        #print ("All search for  :",StartClass, pred,"subject is:", subj, " and object is :", obj)
        if (pred.rsplit('#')[-1]=="domain") and (re.match(StartClassWhere,obj.rsplit('/rdf')[-1])):
            SubPropList[idx]=subj.rsplit('/rdf')[-1]
            SubPropList[idx]=Literal(SubPropList[idx], datatype=XSD.string)
            SubPropList[idx]=SubPropList[idx].value
            SubPropList[idx]=str(SubPropList[idx])
            Strtemp[idx]=SubPropList[idx]
            StrLower=string.lower(SubPropList[idx])
            if (string.find(StrLower,locName)==0):
                print (idx,":",SubPropList[idx]," was found property in subclass for Where_in: ", obj.rsplit('/rdf')[-1])
                Qvar.boundedSlotWhere_in[idx]=SubPropList[idx]
                Flag=1
            if (StartClassWhere!='.*$') and (retrievingInstanceWhere_in(WorkingDirectory,StartClassWhere,Strtemp[idx],locName)):
                Flag=1
            idx=idx+1
        #
        if (subj, pred, obj) not in gProp:
            raise Exception("It better be!")

    if (Flag==1):
        print ("Note: Token was find in property list in the sub class for Where_in:", StartClassWhere, "for token:",locName)
        return True
    else:
        return False


def retrievingInstance(WorkingDirectory,StartClass,propName,persName):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    g = rdflib.Graph()
    g.parse(WorkingDirectory + "QA-Enterprise.rdf")
    InstanceName={}
    idxInst=0
    flagProp=0
    #if (StartClass=='*' and propName=='*'):
    #    propName='^.*$'

    for subj, pred, obj in g:

        StrInst=Literal(obj)
        StrInst=StrInst.value
        StrInst=StrInst.encode('utf-8')
        StrTemp=str(StrInst)
        if (re.match(propName,pred.rsplit('/rdf')[-1]))and (persName in StrTemp):
            print ("Instance No.",idxInst,"for PropName with Instance:",propName,"for token",persName,StrTemp,"in class:",StartClass,pred,"subject is:", subj, " and object is :", obj)
            InstanceName[idxInst]=subj.rsplit('/rdf')[-1]
            Qvar.boundedInstancePerson[InstanceName[idxInst]]=StrTemp
            flagProp=1
            idxInst=idxInst+1

        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    if (flagProp==1):
        return True
    else:
        return False


def retrievingInstanceWhere_in(WorkingDirectory,StartClassWhere,propName,locName):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    g = rdflib.Graph()
    g.parse(WorkingDirectory + "QA-Enterprise.rdf")
    InstanceName={}
    idxInst=0
    flagProp=0
    #if (StartClass=='*' and propName=='*'):
    #    propName='^.*$'

    for subj, pred, obj in g:

        StrInst=Literal(obj)
        StrInst=StrInst.value
        StrInst=StrInst.encode('utf-8')
        StrTemp=str(StrInst)
        if (re.match(propName,pred.rsplit('/rdf')[-1]))and (locName in StrTemp):
            print ("Instance No.",idxInst,"for PropName with Instance:",propName,"for token",locName,StrTemp,"in class:",StartClassWhere,pred,"subject is:", subj, " and object is :", obj)
            InstanceName[idxInst]=subj.rsplit('/rdf')[-1]
            Qvar.boundedInstanceWhere_in[InstanceName[idxInst]]=StrTemp
            flagProp=1
            idxInst=idxInst+1

        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    if (flagProp==1):
        return True
    else:
        return False



def isPersonInOntology(s,WorkingDirectory,personSC):
    from rule import isVerb,isAdjective,isAdverb,isVerbAux,isNoun
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if isVerb(s,itk) or isVerbAux(s,itk) or isAdjective(s,itk) or isAdverb(s,itk) or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue

        if retrievingSubclass(WorkingDirectory,personSC,lmas)!=-1 :
            print ("The Class or subclass or Instance of Person Was found in the ontology to detect person:" , personSC, "and its lema is : ", lmas)
            Flag=1

    if Flag==1:
        return True
    else:
        return False


def bindPersonOnt(s,WorkingDirectory,personSC):
    global currentRule
    from rule import currentRule
    from rule import isVerb,isAdjective,isAdverb,isVerbAux,isNoun
    Qvar=currentRule
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if isVerb(s,itk) or isVerbAux(s,itk) or isAdjective(s,itk) or isAdverb(s,itk) or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos=="." :
            continue

        if retrievingSubclass(WorkingDirectory,personSC,lmas):
            print "bindPersonOnt, is verb , pos", isVerb(s,itk),isVerbAux(s,itk),isNoun(s,itk),isAdjective(s,itk),isAdverb(s,itk),pos

            print ("The Class or subclass or Instance of Person Was found in the ontology to detect person:" , personSC, "and its lema is : ", lmas)
            Flag=1
            Qvar.boundedVars['tk_PER']=itk
            Qvar.boundedVars['ont_PER']=lmas



    if Flag==1:
        return True
    else:
        return False



def isActionInOntology(s,WorkingDirectory,personSC):
    from rule import isVerb,isAdjective,isAdverb,isVerbAux,isNoun
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if  isVerbAux(s,itk) or isNoun(s,itk) or isAdjective(s,itk) or isAdverb(s,itk) or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or pos=="TO" or\
                        pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue

        if retrievingSubclass(WorkingDirectory,personSC,lmas) :
            print "isActionInOntology, is verb , pos", isVerb(s,itk),isVerbAux(s,itk),isNoun(s,itk),isAdjective(s,itk),isAdverb(s,itk),pos

            print ("The Class or subclass or Instance of Person Was found in the ontology to detect person:" , personSC, "and its lema is : ", lmas)
            Flag=1

    if Flag==1:
        return True
    else:
        return False

def bindActionOnt(s,WorkingDirectory,actionSC):
    global currentRule
    from rule import currentRule
    from rule import isVerb,isAdjective,isAdverb,isVerbAux,isNoun

    Qvar=currentRule
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        # print "itk,tk", itk, tk
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if  isVerbAux(s,itk) or isNoun(s,itk) or isAdjective(s,itk) or isAdverb(s,itk) or pos=="DT" or pos=="IN" or pos=="CC" or pos=="EX" or\
                        pos=="CD" or pos=="MD" or pos=="PRP" or pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="IN" or pos==".":
            continue

        if retrievingSubclass(WorkingDirectory,actionSC,lmas):
            print "bindActionOnt, is verb , pos", isVerb(s,itk),isVerbAux(s,itk),isNoun(s,itk),isAdjective(s,itk),isAdverb(s,itk),pos
            print ("The Class or subclass or Instance of Action Was found in the ontology to detect action:" , actionSC, "and its lema is : ", lmas)
            Flag=1
            Qvar.boundedVars['tk_ACT']=itk
            Qvar.boundedVars['ont_ACT']=lmas



    if Flag==1:
        return True
    else:
        return False



