__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        SOP_managingOntology.py
#
# Author:      Majid
#
# Created:     2014/06/06
# Subject Object  Predicate managing ontology
#-----------------------------------------------------------------------------

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


def isInClass(s,WorkingDirectory):
    infile = open(WorkingDirectory + "/class.txt", 'r')
    tks=s._get_tokens()
    Flag=0
    for tk in tks:
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB":
            continue
        infile.seek(0, 0)
        while True:
            text = infile.readline()
            texts=string.lower(text)
            if len(texts) == 0:
                break
            lstclass=normalizeName(text)
            #print "Normalized:",lst
            ln=len(lstclass)
            i=0
            while i != ln:
                #print "lstclass{i}:", lstclass[i], "is:", len(lstclass[i])
                if ((wrds in lstclass[i]) and (len(wrds)==len(lstclass[i])-1)) or ((lmas in lstclass[i]) and (len(lmas)==len(lstclass[i])-1)):
                    print ("Was found class name in class.txt file :", texts, "for Word:" , wrd, "and its lema is : ", lma)
                    Flag=1
                else:
                    if isInClassSynset(lma,lstclass[i]):
                        print ("Was found class name in Synset WordNet :", text, "for Word:" , wrd, "and its lema is : ", lma)
                        Flag=1

                i=i+1

    infile.close()
    if Flag==1:
        return True
    else:
        return False


def isInClassSynset(lm,txt):

    lma=lm
    text=txt
    Flag=0
    nrmwrdlist=normalizeName(lma)
    for wrds in nrmwrdlist:
        #lmasynset1= getSynsets(wrds,None)
        #print ("Synsets Was found Synonym of  class name in WordNet file :",  "for Word:" , wrd, "and its lema is : ", lmasynset1)
        #ln=lmasynset1.__len__()
        lst=lemmalist(wrds)
        ln=len(lst)
        i=0
        while i != ln:
            if (lst[i] in text) and (len(lst[i])==len(text)):
                #print ("Successfully found Synonym of class name in Synset :", text, "for Word:" , wrd, "and its lema is : ", lst[i])
                Flag=1
            i+=1
    if Flag==1:
        return True
    else:
        return False


def isInProperty(s,WorkingDirectory):
    infile = open(WorkingDirectory + "/property.txt", 'r')
#    global sentences
  #  sl=sentences[s]
    tks=s._get_tokens()
    Flag=0
    for tk in tks:
        ln=1
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if lmas=="s" or lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB":
            continue

        lstproperty=normalizeName(lma)
        #print "Normalized:",lstproperty
        ln=len(lstproperty)
        i=0
        while i != ln:
            if (isInPropertySynset(WorkingDirectory,'.*$',lstproperty[i])):
                Flag=1
            #    if isInPropertySynset(WorkingDirectory,wrd,lma,texts,ln):
            #        Flag=1
            i=i+1
    infile.close()
    if Flag==1:
        return True
    else:
        return False



def isInPropertySynset(WorkingDirectory,StartClass,prop):
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
            lstproperty=lemmalist(StrLower)
            ln=len(lstproperty)
            i=0
            while i != ln:
                if lstproperty[i] in prop:
                    print (idx,":",SubPropList[idx]," was found property in subclass: ", obj.rsplit('/rdf')[-1])
                    #retrievingInstance(WorkingDirectory,SubclassList[idx],persName)
                    Flag=1
                i=i+1
            idx=idx+1
        #
        if (subj, pred, obj) not in gProp:
            raise Exception("It better be!")
    #j=0
    #print ("All of the Properties for Class:", StartClass, "are:")
    #
    #while j<idx:
    #    print (SubPropList[j])
    #    j=j+1
    if (Flag==1):
        print ("Token was find in property Synset list in the sub class:", StartClass, "for token:",prop)
        return True
    else:
        return False

#-------  Searching in Instance of Enterprise ontology--------------------------

def isInInstance(s,WorkingDirectory):
   # infile = open(WorkingDirectory + "/instance.txt", 'r')
    tks=s._get_tokens()
    Flag=0
    for tk in tks:
        ln=1
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if lmas=="s" or lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB":
            continue

        lstinstance=normalizeName(lma)
        ln=len(lstinstance)
        i=0
        while i != ln:
            if (isInInstanceSynset(WorkingDirectory,'*','.*$',lstinstance[i])):
                Flag=1
            i=i+1

    #infile.close()
    if Flag==1:
        return True
    else:
        return False



def isInInstanceSynset(WorkingDirectory,StartClass,propName,persName):
    g = rdflib.Graph()
    g.parse(WorkingDirectory + "QA-Enterprise.rdf")
    InstanceName={}
    idxInst=0
    flagProp=0
    #if (StartClass=='*' and propName=='*'):
    #    propName='^.*$'
    lstInst=lemmalist(persName)
    ln=len(lstInst)
    for subj, pred, obj in g:

        StrInst=Literal(obj)
        StrInst=StrInst.value
        StrInst=StrInst.encode('utf-8')
        StrTemp=str(StrInst)
        #print ("Value of object is:")
        #print StrTemp

        i=0
        while i != ln:
            if (re.match(propName,pred.rsplit('/rdf')[-1]))and (persName in lstInst[i]):
                #print ("Instance No.",idxInst,"for PropName with Instance:",propName,"for token",persName,lstInst[i],"in class:",StartClass,pred,"subject is:", subj, " and object is :", obj)
                InstanceName[idxInst]=subj.rsplit('/rdf')[-1]
            if (string.find(lstInst[i],persName)==0):
                #print (persName, " was found  as an Instance:...",lstInst[i], "for:", InstanceName[idxInst])
                flagProp=1
            idxInst=idxInst+1

            if (subj, pred, obj) not in g:
                raise Exception("It better be!")
            i=i+1

    if (flagProp==1):
        return True
    else:
        if idxInst>0:
            print ("Note2: Was found similar Instance in ontology")
            return True
    return False






def isTokensInClass(s,WorkingDirectory):
    tokenBoundedClass={}
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue
        tempClass=lookAllSubclass(WorkingDirectory,lmas)
        if tempClass!=-1:
            tokenBoundedClass[itk]=tempClass


    for bClass in tokenBoundedClass:
        print "Returned class for token",bClass,"are:","\n","\t",tokenBoundedClass[bClass],"\n"






def lookAllSubclass(WorkingDirectory,Name):
    g = rdflib.Graph()
    g.parse(WorkingDirectory + "QA-Enterprise.rdfs")
    SubclassList={}
    SubclassListT={}
    Strtemp={}
    idx=0
    idy=0
    Flag=0

    for subj, pred, obj in g:
        if (pred.rsplit('#')[-1]=="subClassOf"):
            SubclassListT[idx]=subj.rsplit('/rdf')[-1]
            SubclassListT[idx]=Literal(SubclassListT[idx], datatype=XSD.string)
            SubclassListT[idx]=SubclassListT[idx].value
            SubclassListT[idx]=str(SubclassListT[idx])
            Strtemp[idx]=SubclassListT[idx]
            StrLower=string.lower(Strtemp[idx])
            if (string.find(StrLower,Name)==0):
                SubclassList[idx]=SubclassListT[idx]
                idx=idx+1
                Flag=1

            idy=idy+1

        if (subj, pred, obj) not in g:
            raise Exception("It better be!")
    if Flag !=0:
        return SubclassList
    else:
        return -1



def isTokensInSlot(s,WorkingDirectory):
    tokenBoundedSlot={}
    tokenBoundedSlot4Class={}
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue
        tempClass=lookAllSlot(WorkingDirectory,lmas)
        if tempClass!=-1:
            tokenBoundedSlot[itk]=tempClass[0]
            tokenBoundedSlot4Class[itk]=tempClass[1]


    for bSlot in tokenBoundedSlot:
        print "Returned Slot for token",bSlot,"are:","\n","\t",tokenBoundedSlot[bSlot], "------------SLOT------>",tokenBoundedSlot4Class[bSlot],"\n"

    # for bClass in tokenBoundedSlot4Class:
    #     print "\t","Return Slot_for_ Class for token",bClass,"are:","\n",tokenBoundedSlot4Class[bClass]




def lookAllSlot(WorkingDirectory,slotName):
    gProp = rdflib.Graph()
    gProp.parse(WorkingDirectory + "QA-Enterprise.rdfs")
    slotList={}
    slotListT={}
    slot4Class={}
    Strtemp={}
    idx=0
    idy=0
    Flag=0

    for subj, pred, obj in gProp:
        if pred.rsplit('#')[-1]=="domain":
            slotListT[idx]=subj.rsplit('/rdf')[-1]
            slotListT[idx]=Literal(slotListT[idx], datatype=XSD.string)
            slotListT[idx]=slotListT[idx].value
            slotListT[idx]=str(slotListT[idx])
            Strtemp[idx]=slotListT[idx]
            StrLower=string.lower(slotListT[idx])
            if (string.find(StrLower,slotName)==0):
                # print (idx,":",slotListT[idx]," was found property in subclass: ", obj.rsplit('/rdf')[-1])
                slotList[idx]=slotListT[idx]
                slot4Class[idx]=obj.rsplit('/rdf')[-1]
                idx=idx+1
                Flag=1
            idy=idy+1
        #
        if (subj, pred, obj) not in gProp:
            raise Exception("It better be!")

    if Flag !=0:
        return slotList,slot4Class
    else:
        return -1


def isTokensInInstance(s,WorkingDirectory):
    tokenBoundedInstance={}
    tokenBoundedInstance4Slot={}
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue
        tempInstance=lookAllInstance(WorkingDirectory,lmas)
        if tempInstance!=-1:
            tokenBoundedInstance[itk]=tempInstance[0]
            tokenBoundedInstance4Slot[itk]=tempInstance[1]


    for bInstance in tokenBoundedInstance:
        print "Returned Instance for token",bInstance,"are:","\n"
        print "\t",tokenBoundedInstance[bInstance],"\n"
        print "------------ With Related SLOT Orderly----->"
        print "\t",tokenBoundedInstance4Slot[bInstance],"\n"

    # for bSlot in tokenBoundedInstance4Slot:
    #     print "\t","Returned Instance_for_ Slot for token",bSlot,"are:","\n",tokenBoundedInstance4Slot[bSlot]




def lookAllInstance(WorkingDirectory,instanceName):
    listInstance={}
    listInstanceT={}
    listInstance4Slot={}
    path=WorkingDirectory + "enterprise.rdf"
    uri=URIRef(path)

    g = rdflib.Graph()
    g.parse(path)
    idx=0
    idy=0
    Flag=0

    for subj, pred, obj in g:

        StrInst=Literal(obj)
        StrInst=StrInst.value
        StrInst=StrInst.encode('utf-8')
        StrTemp=str(string.lower(StrInst))

        if instanceName in StrTemp:
            listInstanceT[idx]=subj.rsplit('/rdf')[-1]
            # print (instanceName, " was found  as an Instance:...", StrTemp, "for Slot :",pred.rsplit('/rdf')[-1], "and subject is:", listInstanceT[idx])
            listInstance[idx]=StrInst
            if pred.rsplit('/rdf')[-1]=="-schema#label":
                uri=URIRef(listInstanceT[idx])
                # print "is Schema!!!!!!!!",  pred.rsplit('&rdf_;')[-1], g.resource(uri)
                resource = g.resource(uri)
                # assert isinstance(resource, Resource)
                # print "is Instance:", isinstance(resource, Resource),resource
                # assert resource.identifier is uri
                # print "is uri:", resource.identifier is uri
                # assert resource.graph is g
                # # print "new resource value:",resource.identifier
                listInstance4Slot[idx]=resource.identifier

            else:
                listInstance4Slot[idx]=pred.rsplit('/rdf')[-1]
            idx=idx+1
            Flag=1
            idy=idy+1

        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    if Flag !=0:
        return listInstance,listInstance4Slot
    else:
        return -1
