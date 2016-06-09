__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        Recursive_SPARQL_Ontology.py
#
# Author:      Majid
#
# Created:     2015/02/07
# Recursive SPARQL managing ontology
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
from rule import *



def retrieveSlotsItem(WorkingDirectory,startClass,itk_slot1,itk_slot2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classItem=str(startClass)
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propItem_List={}
    propItem_Temp={}

    idx=0
    itemdig=""
    seq1=str(itk_slot1),str(itk_slot2),str(idx)
    itemdig=itemdig.join(seq1)
    intitem=str(itemdig)

    qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .
                FILTER (CONTAINS (  str(?varClass), '"""+classItem+"""'))

            }""")

    i=0
    for row in qClass.result:
        propItem_List[intitem,i]=str(row)
        propItem_Temp[intitem,i]=propItem_List[intitem,i].split()
        propItem_Temp[intitem,i][0]=propItem_Temp[intitem,i][0].rsplit('/rdf')[-1]
        propItem_Temp[intitem,i][1]=propItem_Temp[intitem,i][1].rsplit('/rdf')[-1]
        propItem_Temp[intitem,i][0]=propItem_Temp[intitem,i][0].rstrip("'),)")
        propItem_Temp[intitem,i][1]=propItem_Temp[intitem,i][1].rstrip("'),)")
        # pure_SlotAnswer_name=pure_slot_name(propAnswer_Temp[intitem,i][1])
        # print "classAnswer, pure_slot_name How much, lst_Rec[idx]: ",classAnswer, pure_SlotAnswer_name,lst_Rec[idx]
        Qvar.addBoundedSlotItem(propItem_Temp[intitem,i],propItem_Temp[intitem,i][0],propItem_Temp[intitem,i][1],intitem,i)
        Qvar.addBoundedClassItem(propItem_Temp[intitem,i][0],intitem,i)
        i=i+1



def retrieveSlotsPerson(WorkingDirectory,startClass,itk_slot1,itk_slot2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classPerson=str(startClass)
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propItem_List={}
    propItem_Temp={}

    idx=0
    itemdig=""
    seq1=str(itk_slot1),str(itk_slot2),str(idx)
    itemdig=itemdig.join(seq1)
    intitem=str(itemdig)

    qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .
                FILTER (CONTAINS (  str(?varClass), '"""+classPerson+"""'))

            }""")

    i=0
    for row in qClass.result:
        propItem_List[intitem,i]=str(row)
        print "retrieveSlotsPerson in row: ",str(row)
        propItem_Temp[intitem,i]=propItem_List[intitem,i].split()
        propItem_Temp[intitem,i][0]=propItem_Temp[intitem,i][0].rsplit('/rdf')[-1]
        propItem_Temp[intitem,i][1]=propItem_Temp[intitem,i][1].rsplit('/rdf')[-1]
        propItem_Temp[intitem,i][0]=propItem_Temp[intitem,i][0].rstrip("'),)")
        propItem_Temp[intitem,i][1]=propItem_Temp[intitem,i][1].rstrip("'),)")
        Qvar.addBoundedSlotPerson(propItem_Temp[intitem,i],propItem_Temp[intitem,i][0],propItem_Temp[intitem,i][1],intitem,i)
        if i==0:
            Qvar.addBoundedClassPerson(propItem_Temp[intitem,i][0],intitem,i)
        i=i+1


def retrieveSlotsAnswer(WorkingDirectory,slotType,itk_slot1,itk_slot2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classAnswer_Temp=slotType
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propAnswer_List={}
    propAnswer_Temp={}

    idx=0
    itemdig=""
    seq1=str(itk_slot1),str(itk_slot2),str(idx)
    itemdig=itemdig.join(seq1)
    intitem=str(itemdig)
    classAnswer=str(classAnswer_Temp)

    qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .
                FILTER (CONTAINS (  str(?varClass), '"""+classAnswer+"""'))

            }""")

    i=0
    for row in qClass.result:
        propAnswer_List[intitem,i]=str(row)
        propAnswer_Temp[intitem,i]=propAnswer_List[intitem,i].split()
        propAnswer_Temp[intitem,i][0]=propAnswer_Temp[intitem,i][0].rsplit('/rdf')[-1]
        propAnswer_Temp[intitem,i][1]=propAnswer_Temp[intitem,i][1].rsplit('/rdf')[-1]
        propAnswer_Temp[intitem,i][0]=propAnswer_Temp[intitem,i][0].rstrip("'),)")
        propAnswer_Temp[intitem,i][1]=propAnswer_Temp[intitem,i][1].rstrip("'),)")
        # pure_SlotAnswer_name=pure_slot_name(propAnswer_Temp[intitem,i][1])
        # print "classAnswer, pure_slot_name How much, lst_Rec[idx]: ",classAnswer, pure_SlotAnswer_name,lst_Rec[idx]
        Qvar.addBoundedSlotAnswer(propAnswer_Temp[intitem,i],propAnswer_Temp[intitem,i][0],propAnswer_Temp[intitem,i][1],intitem,i)
        Qvar.addBoundedClassAnswer(propAnswer_Temp[intitem,i][0],intitem,i)
        i=i+1


def retrieveDataTypeAction(WorkingDirectory,StartClass,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClass+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeAction is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeAction(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveDataTypeAnswer(WorkingDirectory,StartClass,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClass+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeAnswer is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeAnswer(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False




def retrieveInstanceAnswer(WorkingDirectory,StartClassAnswer,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?instanceLabel
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdfs:label ?instanceLabel ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassAnswer+"""'))

            }""")
     # ?varSlot  ^^xsd:type ?type.
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "InstanceAnswer for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        instanceTemp[itk,i][3]=instanceTemp[itk,i][3].rsplit("(u'")[-1]
        instanceTemp[itk,i][3]=instanceTemp[itk,i][3].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        instanceTemp[itk,i][3]=instanceTemp[itk,i][3].rstrip("'),)")

        InstHowmuch_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceAnswer(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    # print "NO. of INSTANCES for Token Person:",itk,"is:", i
    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveExactInstanceAnswer(WorkingDirectory,SlottypeAnswer,idxInst1,exactInstanceAnswer):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    itk=idxInst1
    print "SlottypeAnswer[0], SlottypeAnswer[1], exactInstanceAnswer: ", SlottypeAnswer[0],SlottypeAnswer[1], exactInstanceAnswer
    classType=str(SlottypeAnswer[0])
    slotType=str(SlottypeAnswer[1])
    instTypeAnswer=str(exactInstanceAnswer)

    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varClass ?varSlot  ?varInstance ?instanceLabel
                WHERE  {
                    ?a ?varSlot   ?varInstance ;
                       rdfs:label ?instanceLabel ;
                       rdf:type ?varClass.

                    FILTER (CONTAINS (  str(?varClass), '"""+classType+"""') && CONTAINS (  str(?varSlot), '"""+slotType+"""') )
                }""")


                # ?a ?varSlotProp   ?varInstanceProp ;
                #    rdf:type ?varClassProp.
                # ?varInstanceProp rdfs:label ?Slotlbl ;
                #        rdf:type  rdf_:"""+tempCls+""" ;
                #        rdf_:"""+tempSlot+"""  ?varmatchInst.

    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Exact answer query for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        if Qvar.addBoundedExactAnswer(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveClassWhere_in(WorkingDirectory,startLOC,lma_Loc,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule

    classList={}
    classTemp={}

    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    inttk=int(tk)
    sLOC=str(startLOC)
    print "Location class started", sLOC
    qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .

                FILTER (CONTAINS ( str(?varClass), '"""+sLOC+"""'))

            }""")


    i=0
    for row in qClass.result:
        if i==0:
            print "The result of CLASS for Startclass:",sLOC, ") are:----------------","\n"
        classTemp[inttk,i]=str(row)
        classTemp[inttk,i]=classTemp[inttk,i].split()
        classTemp[inttk,i][0]=classTemp[inttk,i][0].rsplit('/rdf')[-1]
        classTemp[inttk,i][1]=classTemp[inttk,i][1].rsplit('/rdf')[-1]

        classTemp[inttk,i][0]=classTemp[inttk,i][0].rstrip("'),)")
        classTemp[inttk,i][1]=classTemp[inttk,i][1].rstrip("'),)")

        pure_name=pure_class_name(classTemp[inttk,i][0])
        print "Before separation",classTemp[inttk,i][0]
        print "Pure name class",pure_name

        if Qvar.addBoundedClassWhere_in(classList[inttk,i],i):
            retrieveSubclassesWhere_in(WorkingDirectory,classTemp[inttk,i][0],lma_Loc,tk)
        i=i+1

    print "NO. of Classes for start class:",sLOC,"is:", i




def retrieveSubclassesWhere_in(WorkingDirectory,subClassWhere_in,subLOC,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassList={}
    classListTemp={}
    subClassTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    recLOC=str(subLOC)
    itemdig=""
    itemdig=str(tk)
    intitem=int(itemdig)
    classt=string.lower(subClassWhere_in)
    lenclasst=len(classt)

    print "Location class started for retrieve SubclassesWhere_in", recLOC,classt,subClassWhere_in,lenclasst
    Flag=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?subclass
            WHERE  {
                ?subclass  rdfs:subClassOf ?varClass.
                FILTER ( CONTAINS( LCASE( str(?varClass)), '"""+classt+"""'))

            }""")

    i=0
    for row in qSubClass:
        subClassList[intitem,i]=str(row)
        subClassTemp[intitem,i]=subClassList[intitem,i].split()

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rsplit('/rdf')[-1]
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rsplit('/rdf')[-1]

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rstrip("'),)")
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rstrip("'),)")
        if (string.find(pure_class_name(subClassTemp[intitem,i][1]),subLOC)==0):
            if Qvar.addBoundedSubClassWhere_in(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i):
                print "OK!!,  FOUND  Class[",intitem,"][",i,"]",subClassTemp[intitem,i][0],subClassTemp[intitem,i],"has Subclass:",subClassTemp[intitem,i][1]
                Qvar.addBoundedClassWhere_in(subClassTemp[intitem,i][1],intitem,i)
                Qvar.addBoundedSlotTypeWhere_in(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i)
            Flag=1

        else:
            subitemdig=""
            seq1=str(intitem),str(i)
            subitemdig=subitemdig.join(seq1)
            subitemdig=int(subitemdig)
            if retrieveSubclassesWhere_in(WorkingDirectory,subClassTemp[intitem,i][1],recLOC,subitemdig):
                Flag=1
        i=i+1
    print "NO. of SUBCLASSES for Start Class:",intitem,"is:", i

    if Flag==1:
        return True
    else:
        return False

def retrieveSubclassesDataType(WorkingDirectory,subClassDataType,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassList={}
    classListTemp={}
    subClassTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    itemdig=""
    itemdig=str(tk)
    intitem=int(itemdig)
    classt=string.lower(subClassDataType)
    lenclasst=len(classt)

    print "Location class started for retrieve SubclassesDataType", classt,subClassDataType,lenclasst
    Flag=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?subclass
            WHERE  {
                ?subclass  rdfs:subClassOf ?varClass.
                FILTER ( CONTAINS( LCASE( str(?varClass)), '"""+classt+"""'))

            }""")

    i=0
    for row in qSubClass:
        subClassList[intitem,i]=str(row)
        subClassTemp[intitem,i]=subClassList[intitem,i].split()

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rsplit('/rdf')[-1]
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rsplit('/rdf')[-1]

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rstrip("'),)")
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rstrip("'),)")
        if Qvar.addBoundedSubClassWhere_in(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i):
            subitemdig=""
            seq1=str(intitem),str(i)
            subitemdig=subitemdig.join(seq1)
            subitemdig=int(subitemdig)
            if retrieveSubclassesDataType(WorkingDirectory,subClassTemp[intitem,i][1],subitemdig):
                Flag=1
        i=i+1

    # print "NO. of SUBCLASSES for retrieve SubclassesWhere_in:",intitem,"is:", i

    if Flag==1:
        return True
    else:
        return False


def retrieveSlotsWhere(WorkingDirectory,slotLOC,itk_loc1,itk_loc2,loc,f):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}
    classWhere_Temp=slotLOC
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propWhere_List={}
    propWhere_Temp={}
    classWhere_ListTemp={}
    if f==1:
        lmalistWhere=['part']
        lnlistWhere=len(lmalistWhere)
        locationList =lemmalist(lmalistWhere[0])
        ln=len(locationList)
        i=0
        while i != ln:
            locationList[i]=Literal(locationList[i], datatype=XSD.string)
            locationList[i]=locationList[i].value
            locationList[i]=str(locationList[i])
            i=i+1
        lst_Loc=list(set(locationList))
        ln=len(lst_Loc)
        # print "retrieveSlotsWhere_in !!!  lemmalist is StartClass,locName,lst_loc ",slotLOC,lmalistWhere,lst_Loc
    else:
        lst_Loc1=[loc]
        seq=(loc)
        # lst_Loc2=lst_Loc1.join(seq)
        lst_Loc=list(set(lst_Loc1))
        ln=len(lst_Loc)

    idx=0
    while idx!=ln:
        Flag=0
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(idx)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        classWr=str(classWhere_Temp)
        # print "SLOT for item in synset for classItem",classWr,itk_loc1,itk_loc2

        qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .
                    FILTER (CONTAINS (  str(?varClass), '"""+classWr+"""'))

                }""")

        i=0
        for row in qClass.result:
            # if i==0:
            #     print "The result of SLOTS for location :",lst_Loc[idx],  " are:----------------","\n"

            propWhere_List[intitem,i]=str(row)
            propWhere_Temp[intitem,i]=propWhere_List[intitem,i].split()

            propWhere_Temp[intitem,i][0]=propWhere_Temp[intitem,i][0].rsplit('/rdf')[-1]
            propWhere_Temp[intitem,i][1]=propWhere_Temp[intitem,i][1].rsplit('/rdf')[-1]

            propWhere_Temp[intitem,i][0]=propWhere_Temp[intitem,i][0].rstrip("'),)")
            propWhere_Temp[intitem,i][1]=propWhere_Temp[intitem,i][1].rstrip("'),)")

            pure_SlotWhere_name=pure_slot_name(propWhere_Temp[intitem,i][1])

            if (string.find(pure_SlotWhere_name,lst_Loc[idx])!=-1):
                # print "OKK!!, pure_slot_name Where_in",pure_SlotWhere_name,lst_Loc[idx]
                Qvar.addBoundedSlotWhere(propWhere_Temp[intitem,i],propWhere_Temp[intitem,i][0],propWhere_Temp[intitem,i][1],intitem,i)
                classWhere_ListTemp[i]=propWhere_Temp[intitem,i]
                Qvar.addBoundedClassWhere(propWhere_Temp[intitem,i][0],intitem,i)

            i=i+1
        qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classWr+"""'))

                            }""")
        j=0
        for row in qSubClassSlot:
            subClassListSlot[intitem,j]=str(row)
            subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
            retrieveSlotsWhere(WorkingDirectory,subClassTempSlot[intitem,j][1],intitem,j,lst_Loc[idx],0)
        idx=idx+1


def retrieveDataTypeWhere(WorkingDirectory,StartClass,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClass+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeWhere is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeWhere(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveInstanceWhere(WorkingDirectory,StartClassWhere,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    print " Sent Classes to retrive Where instances: " , StartClassWhere
    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassWhere+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Where for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstWr_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceWhere(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveClassWho(WorkingDirectory,startLOC,lma_Loc,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule

    classList={}
    classTemp={}

    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    inttk=int(tk)
    sLOC=str(startLOC)
    print "Location class started", sLOC
    qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .

                FILTER (CONTAINS ( str(?varClass), '"""+sLOC+"""'))

            }""")


    i=0
    for row in qClass.result:
        if i==0:
            print "The result of CLASS for Startclass:",sLOC, ") are:----------------","\n"
        classTemp[inttk,i]=str(row)
        classTemp[inttk,i]=classTemp[inttk,i].split()
        classTemp[inttk,i][0]=classTemp[inttk,i][0].rsplit('/rdf')[-1]
        classTemp[inttk,i][1]=classTemp[inttk,i][1].rsplit('/rdf')[-1]

        classTemp[inttk,i][0]=classTemp[inttk,i][0].rstrip("'),)")
        classTemp[inttk,i][1]=classTemp[inttk,i][1].rstrip("'),)")

        pure_name=pure_class_name(classTemp[inttk,i][0])
        print "Before separation",classTemp[inttk,i][0]
        print "Pure name class",pure_name

        if Qvar.addBoundedClassWho(classList[inttk,i],i):
            retrieveSubclassesWho(WorkingDirectory,classTemp[inttk,i][0],lma_Loc,tk)
        i=i+1

    print "NO. of Classes for start class:",sLOC,"is:", i


def retrieveSubclassesWho(WorkingDirectory,subClassWho,subLOC,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassList={}
    classListTemp={}
    subClassTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    recLOC=str(subLOC)
    itemdig=""
    itemdig=str(tk)
    intitem=int(itemdig)
    classt=string.lower(subClassWho)
    lenclasst=len(classt)

    print "Location class started for retrieve SubclassesWhere_in", recLOC,classt,subClassWho,lenclasst
    Flag=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?subclass
            WHERE  {
                ?subclass  rdfs:subClassOf ?varClass.
                FILTER ( CONTAINS( LCASE( str(?varClass)), '"""+classt+"""'))

            }""")

    i=0
    for row in qSubClass:
        subClassList[intitem,i]=str(row)
        subClassTemp[intitem,i]=subClassList[intitem,i].split()

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rsplit('/rdf')[-1]
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rsplit('/rdf')[-1]

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rstrip("'),)")
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rstrip("'),)")
        if (string.find(pure_class_name(subClassTemp[intitem,i][1]),subLOC)==0):
            if Qvar.addBoundedSubClassWho(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i):
                print "OK!!,  FOUND  Class[",intitem,"][",i,"]",subClassTemp[intitem,i][0],subClassTemp[intitem,i],"has Subclass:",subClassTemp[intitem,i][1]
                Qvar.addBoundedClassWho(subClassTemp[intitem,i][1],intitem,i)
                Qvar.addBoundedSlotTypeWho(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i)
            Flag=1

        else:
            subitemdig=""
            seq1=str(intitem),str(i)
            subitemdig=subitemdig.join(seq1)
            subitemdig=int(subitemdig)
            if retrieveSubclassesWho(WorkingDirectory,subClassTemp[intitem,i][1],recLOC,subitemdig):
                Flag=1
        i=i+1
    print "NO. of SUBCLASSES for Start Class:",intitem,"is:", i

    if Flag==1:
        return True
    else:
        return False


def retrieveSubclassesDataType_Who(WorkingDirectory,subClassDataType,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassList={}
    classListTemp={}
    subClassTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    itemdig=""
    itemdig=str(tk)
    intitem=int(itemdig)
    classt=string.lower(subClassDataType)
    lenclasst=len(classt)

    print "Location class started for retrieve SubclassesDataType", classt,subClassDataType,lenclasst
    Flag=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?subclass
            WHERE  {
                ?subclass  rdfs:subClassOf ?varClass.
                FILTER ( CONTAINS( LCASE( str(?varClass)), '"""+classt+"""'))

            }""")

    i=0
    for row in qSubClass:
        subClassList[intitem,i]=str(row)
        subClassTemp[intitem,i]=subClassList[intitem,i].split()

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rsplit('/rdf')[-1]
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rsplit('/rdf')[-1]

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rstrip("'),)")
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rstrip("'),)")
        if Qvar.addBoundedSubClassWho(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i):
            subitemdig=""
            seq1=str(intitem),str(i)
            subitemdig=subitemdig.join(seq1)
            subitemdig=int(subitemdig)
            if retrieveSubclassesDataType_Who(WorkingDirectory,subClassTemp[intitem,i][1],subitemdig):
                Flag=1
        i=i+1

    # print "NO. of SUBCLASSES for retrieve SubclassesWhere_in:",intitem,"is:", i

    if Flag==1:
        return True
    else:
        return False


def retrieveSlotsWho(WorkingDirectory,slotPer,itk_per1,itk_per2,per,f):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classWho_Temp=slotPer
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propWho_List={}
    propWho_Temp={}
    if f==1:
        # lmalistWho=['record']
        # lnlistWho=len(lmalistWho)
        recordList =lemmalist(classWho_Temp)
        ln=len(recordList)
        i=0
        while i != ln:
            recordList[i]=Literal(recordList[i], datatype=XSD.string)
            recordList[i]=recordList[i].value
            recordList[i]=str(recordList[i])
            i=i+1
        lst_Rec=list(set(recordList))
        ln=len(lst_Rec)
        print "retrieveSlotsWho !!!  lemmalist is StartClass,lst_loc, ln: ",lst_Rec,ln
    else:
        lst_Rec1=[per]
        lst_Rec=list(set(lst_Rec1))
        ln=len(lst_Rec)
        print "list(Person)",ln,lst_Rec

    idx=0
    while idx!=ln:
        itemdig=""
        seq1=str(itk_per1),str(itk_per2),str(idx)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        classWho=str(classWho_Temp)
        # print "SLOT for item in synset for classItem, itk_per1, itk_per1 :",classWho,itk_per1,itk_per2

        qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .
                    FILTER (CONTAINS (  str(?varClass), '"""+classWho+"""'))

                }""")

        i=0
        for row in qClass.result:
            propWho_List[intitem,i]=str(row)
            propWho_Temp[intitem,i]=propWho_List[intitem,i].split()
            propWho_Temp[intitem,i][0]=propWho_Temp[intitem,i][0].rsplit('/rdf')[-1]
            propWho_Temp[intitem,i][1]=propWho_Temp[intitem,i][1].rsplit('/rdf')[-1]
            propWho_Temp[intitem,i][0]=propWho_Temp[intitem,i][0].rstrip("'),)")
            propWho_Temp[intitem,i][1]=propWho_Temp[intitem,i][1].rstrip("'),)")
            pure_SlotWho_name=pure_slot_name(propWho_Temp[intitem,i][1])
            print "classWho, pure_slot_name Who, lst_Rec[idx]: ",classWho, pure_SlotWho_name,lst_Rec[idx]

            if f==1 :
                if (string.find(pure_SlotWho_name,lst_Rec[idx])!=-1):
                    print "OKK!!, pure_slot_name Who",pure_SlotWho_name,lst_Rec[idx]
                    Qvar.addBoundedSlotWho(propWho_Temp[intitem,i],propWho_Temp[intitem,i][0],propWho_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWho(propWho_Temp[intitem,i][0],intitem,i)
            else:
                    Qvar.addBoundedSlotWho(propWho_Temp[intitem,i],propWho_Temp[intitem,i][0],propWho_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWho(propWho_Temp[intitem,i][0],intitem,i)

            i=i+1
        # print "NO. of Properties for classWr_in , i for location:",classWr_in,"is:", i,lst_Loc[idx]
        # print "Recursive  for class slot Where_in ,  for step i:",i, Qvar.boundedClassWhere_in,Qvar.boundedSlotWhere_in
        qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classWho+"""'))

                            }""")
        j=0
        for row in qSubClassSlot:
            subClassListSlot[intitem,j]=str(row)
            subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
            retrieveSlotsWho(WorkingDirectory,subClassTempSlot[intitem,j][1],intitem,j,lst_Rec[idx],0)

        idx=idx+1


def retrieveSlotsWhat(WorkingDirectory,slotPer,itk_per1,itk_per2,per,f):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classWhat_Temp=slotPer
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propWhat_List={}
    propWhat_Temp={}
    if f==1:
        # lmalistWho=['record']
        # lnlistWho=len(lmalistWho)
        recordList =lemmalist(classWhat_Temp)
        ln=len(recordList)
        i=0
        while i != ln:
            recordList[i]=Literal(recordList[i], datatype=XSD.string)
            recordList[i]=recordList[i].value
            recordList[i]=str(recordList[i])
            i=i+1
        lst_Rec=list(set(recordList))
        ln=len(lst_Rec)
        print "retrieveSlotsWhat !!!  lemmalist is StartClass,lst_loc, ln: ",lst_Rec,ln
    else:
        lst_Rec1=[per]
        lst_Rec=list(set(lst_Rec1))
        ln=len(lst_Rec)
        print "list(Person)",ln,lst_Rec

    idx=0
    while idx!=ln:
        itemdig=""
        seq1=str(itk_per1),str(itk_per2),str(idx)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        classWhat=str(classWhat_Temp)
        # print "SLOT for item in synset for classItem, itk_per1, itk_per1 :",classWho,itk_per1,itk_per2

        qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .
                    FILTER (CONTAINS (  str(?varClass), '"""+classWhat+"""'))

                }""")

        i=0
        for row in qClass.result:
            propWhat_List[intitem,i]=str(row)
            propWhat_Temp[intitem,i]=propWhat_List[intitem,i].split()
            propWhat_Temp[intitem,i][0]=propWhat_Temp[intitem,i][0].rsplit('/rdf')[-1]
            propWhat_Temp[intitem,i][1]=propWhat_Temp[intitem,i][1].rsplit('/rdf')[-1]
            propWhat_Temp[intitem,i][0]=propWhat_Temp[intitem,i][0].rstrip("'),)")
            propWhat_Temp[intitem,i][1]=propWhat_Temp[intitem,i][1].rstrip("'),)")
            pure_SlotWhat_name=pure_slot_name(propWhat_Temp[intitem,i][1])
            print "classWhat, pure_slot_name What, lst_Rec[idx]: ",classWhat, pure_SlotWhat_name,lst_Rec[idx]

            if f==1 :
                if (string.find(pure_SlotWhat_name,lst_Rec[idx])!=-1):
                    print "OKK!!, pure_slot_name What",pure_SlotWhat_name,lst_Rec[idx]
                    Qvar.addBoundedSlotWhat(propWhat_Temp[intitem,i],propWhat_Temp[intitem,i][0],propWhat_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWhat(propWhat_Temp[intitem,i][0],intitem,i)
            else:
                    Qvar.addBoundedSlotWhat(propWhat_Temp[intitem,i],propWhat_Temp[intitem,i][0],propWhat_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWhat(propWhat_Temp[intitem,i][0],intitem,i)

            i=i+1
        # print "NO. of Properties for classWr_in , i for location:",classWr_in,"is:", i,lst_Loc[idx]
        # print "Recursive  for class slot Where_in ,  for step i:",i, Qvar.boundedClassWhere_in,Qvar.boundedSlotWhere_in
        qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classWhat+"""'))

                            }""")
        j=0
        for row in qSubClassSlot:
            subClassListSlot[intitem,j]=str(row)
            subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
            retrieveSlotsWhat(WorkingDirectory,subClassTempSlot[intitem,j][1],intitem,j,lst_Rec[idx],0)

        idx=idx+1

def retrieveSlotsHowmuch(WorkingDirectory,slotHowmuch,itk_slot1,itk_slot2,slot,f):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classHowmuch_Temp=slotHowmuch
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propHowmuch_List={}
    propHowmuch_Temp={}
    if f==1:
        # lmalistWho=['record']
        # lnlistWho=len(lmalistWho)
        recordList =lemmalist(classHowmuch_Temp)
        ln=len(recordList)
        i=0
        while i != ln:
            recordList[i]=Literal(recordList[i], datatype=XSD.string)
            recordList[i]=recordList[i].value
            recordList[i]=str(recordList[i])
            i=i+1
        lst_Rec=list(set(recordList))
        ln=len(lst_Rec)
        print "retrieveSlotsHow much !!!  lemmalist is StartClass,lst_loc, ln: ",lst_Rec,ln
    else:
        lst_Rec1=[slot]
        lst_Rec=list(set(lst_Rec1))
        ln=len(lst_Rec)
        print "list(Person)",ln,lst_Rec

    idx=0
    while idx!=ln:
        itemdig=""
        seq1=str(itk_slot1),str(itk_slot2),str(idx)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        classHowmuch=str(classHowmuch_Temp)
        # print "SLOT for item in synset for classItem, itk_per1, itk_per1 :",classWho,itk_per1,itk_per2

        qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .
                    FILTER (CONTAINS (  str(?varClass), '"""+classHowmuch+"""'))

                }""")

        i=0
        for row in qClass.result:
            propHowmuch_List[intitem,i]=str(row)
            propHowmuch_Temp[intitem,i]=propHowmuch_List[intitem,i].split()
            propHowmuch_Temp[intitem,i][0]=propHowmuch_Temp[intitem,i][0].rsplit('/rdf')[-1]
            propHowmuch_Temp[intitem,i][1]=propHowmuch_Temp[intitem,i][1].rsplit('/rdf')[-1]
            propHowmuch_Temp[intitem,i][0]=propHowmuch_Temp[intitem,i][0].rstrip("'),)")
            propHowmuch_Temp[intitem,i][1]=propHowmuch_Temp[intitem,i][1].rstrip("'),)")
            pure_SlotHowmuch_name=pure_slot_name(propHowmuch_Temp[intitem,i][1])
            print "classHowmuch, pure_slot_name How much, lst_Rec[idx]: ",classHowmuch, pure_SlotHowmuch_name,lst_Rec[idx]

            if f==1 :
                if (string.find(pure_SlotHowmuch_name,lst_Rec[idx])!=-1):
                    print "OKK!!, pure_slot_name Howmuch",pure_SlotHowmuch_name,lst_Rec[idx]
                    Qvar.addBoundedSlotHowmuch(propHowmuch_Temp[intitem,i],propHowmuch_Temp[intitem,i][0],propHowmuch_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassHowmuch(propHowmuch_Temp[intitem,i][0],intitem,i)
            else:
                    Qvar.addBoundedSlotHowmuch(propHowmuch_Temp[intitem,i],propHowmuch_Temp[intitem,i][0],propHowmuch_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassHowmuch(propHowmuch_Temp[intitem,i][0],intitem,i)

            i=i+1
        qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classHowmuch+"""'))

                            }""")
        j=0
        for row in qSubClassSlot:
            subClassListSlot[intitem,j]=str(row)
            subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
            retrieveSlotsHowmuch(WorkingDirectory,subClassTempSlot[intitem,j][1],intitem,j,lst_Rec[idx],0)

        idx=idx+1

def retrieveSlotsEntity(WorkingDirectory,slotEnt,itk_Ent1,itk_Ent2,Entity,f):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}
    classEnt_Temp=slotEnt
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propEnt_List={}
    propEnt_Temp={}
    if f==1:
        recordList =lemmalist(classEnt_Temp)
        ln=len(recordList)
        i=0
        while i != ln:
            recordList[i]=Literal(recordList[i], datatype=XSD.string)
            recordList[i]=recordList[i].value
            recordList[i]=str(recordList[i])
            i=i+1
        lst_Rec=list(set(recordList))
        ln=len(lst_Rec)
        print "retrieveSlotsEntity !!!  lemmalist is StartClass,lst_loc, ln: ",lst_Rec,ln
    else:
        lst_Rec1=[Entity]
        lst_Rec=list(set(lst_Rec1))
        ln=len(lst_Rec)
        print "list(Entity)",ln,lst_Rec

    idx=0
    while idx!=ln:
        itemdig=""
        seq1=str(itk_Ent1),str(itk_Ent2),str(idx)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        classEnt=str(classEnt_Temp)
        # print "SLOT for item in synset for classItem, itk_per1, itk_per1 :",classWho,itk_per1,itk_per2
        qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .
                    FILTER (CONTAINS (  str(?varClass), '"""+classEnt+"""'))

                }""")

        i=0
        for row in qClass.result:
            propEnt_List[intitem,i]=str(row)
            propEnt_Temp[intitem,i]=propEnt_List[intitem,i].split()
            propEnt_Temp[intitem,i][0]=propEnt_Temp[intitem,i][0].rsplit('/rdf')[-1]
            propEnt_Temp[intitem,i][1]=propEnt_Temp[intitem,i][1].rsplit('/rdf')[-1]
            propEnt_Temp[intitem,i][0]=propEnt_Temp[intitem,i][0].rstrip("'),)")
            propEnt_Temp[intitem,i][1]=propEnt_Temp[intitem,i][1].rstrip("'),)")

            pure_SlotEnt_name=pure_slot_name(propEnt_Temp[intitem,i][1])
            print "classEntity, pure_slot_name , lst_Rec[idx]: ",classEnt, pure_SlotEnt_name,lst_Rec[idx]

            if f==1 :
                if (string.find(pure_SlotEnt_name,lst_Rec[idx])!=-1):
                    print "OKK!!, pure_slot_name Who",pure_SlotEnt_name,lst_Rec[idx]
                    Qvar.addBoundedSlotWhat(propEnt_Temp[intitem,i],propEnt_Temp[intitem,i][0],propEnt_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWhat(propEnt_Temp[intitem,i][0],intitem,i)
            else:
                    Qvar.addBoundedSlotWhat(propEnt_Temp[intitem,i],propEnt_Temp[intitem,i][0],propEnt_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWhat(propEnt_Temp[intitem,i][0],intitem,i)

            i=i+1
        # print "NO. of Properties for classWr_in , i for location:",classWr_in,"is:", i,lst_Loc[idx]
        # print "Recursive  for class slot Where_in ,  for step i:",i, Qvar.boundedClassWhere_in,Qvar.boundedSlotWhere_in
        qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classEnt+"""'))

                            }""")
        j=0
        for row in qSubClassSlot:
            subClassListSlot[intitem,j]=str(row)
            subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
            retrieveSlotsEntity(WorkingDirectory,subClassTempSlot[intitem,j][1],intitem,j,lst_Rec[idx],0)
        idx=idx+1



def retrieveSlotsMemb(WorkingDirectory,slotMemb,itk_Memb1,itk_Memb2,Memb,f):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}
    classMemb_Temp=slotMemb
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propMemb_List={}
    propMemb_Temp={}
    if f==1:
        recordList =lemmalist(classMemb_Temp)
        ln=len(recordList)
        i=0
        while i != ln:
            recordList[i]=Literal(recordList[i], datatype=XSD.string)
            recordList[i]=recordList[i].value
            recordList[i]=str(recordList[i])
            i=i+1
        lst_Rec=list(set(recordList))
        ln=len(lst_Rec)
        print "retrieveSlotsMember !!!  lemmalist is StartClass,lst_loc, ln: ",lst_Rec,ln
    else:
        lst_Rec1=[Memb]
        lst_Rec=list(set(lst_Rec1))
        ln=len(lst_Rec)
        print "list(Member)",ln,lst_Rec

    idx=0
    while idx!=ln:
        itemdig=""
        seq1=str(itk_Memb1),str(itk_Memb2),str(idx)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        classMemb=str(classMemb_Temp)
        # print "SLOT for item in synset for classItem, itk_per1, itk_per1 :",classWho,itk_per1,itk_per2
        qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .
                    FILTER (CONTAINS (  str(?varClass), '"""+classMemb+"""'))

                }""")

        i=0
        for row in qClass.result:
            propMemb_List[intitem,i]=str(row)
            propMemb_Temp[intitem,i]=propMemb_List[intitem,i].split()
            propMemb_Temp[intitem,i][0]=propMemb_Temp[intitem,i][0].rsplit('/rdf')[-1]
            propMemb_Temp[intitem,i][1]=propMemb_Temp[intitem,i][1].rsplit('/rdf')[-1]
            propMemb_Temp[intitem,i][0]=propMemb_Temp[intitem,i][0].rstrip("'),)")
            propMemb_Temp[intitem,i][1]=propMemb_Temp[intitem,i][1].rstrip("'),)")

            pure_SlotMemb_name=pure_slot_name(propMemb_Temp[intitem,i][1])
            print "classMemb, pure_slot_name Who, lst_Rec[idx]: ",classMemb, pure_SlotMemb_name,lst_Rec[idx]

            if f==1 :
                if (string.find(pure_SlotMemb_name,lst_Rec[idx])!=-1):
                    print "OKK!!, pure_slot_name Who",pure_SlotMemb_name,lst_Rec[idx]
                    Qvar.addBoundedSlotWho(propMemb_Temp[intitem,i],propMemb_Temp[intitem,i][0],propMemb_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWho(propMemb_Temp[intitem,i][0],intitem,i)
            else:
                    Qvar.addBoundedSlotWho(propMemb_Temp[intitem,i],propMemb_Temp[intitem,i][0],propMemb_Temp[intitem,i][1],intitem,i)
                    Qvar.addBoundedClassWho(propMemb_Temp[intitem,i][0],intitem,i)

            i=i+1
        # print "NO. of Properties for classWr_in , i for location:",classWr_in,"is:", i,lst_Loc[idx]
        # print "Recursive  for class slot Where_in ,  for step i:",i, Qvar.boundedClassWhere_in,Qvar.boundedSlotWhere_in
        qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classMemb+"""'))

                            }""")
        j=0
        for row in qSubClassSlot:
            subClassListSlot[intitem,j]=str(row)
            subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]
            subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
            subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
            retrieveSlotsWho(WorkingDirectory,subClassTempSlot[intitem,j][1],intitem,j,lst_Rec[idx],0)
        idx=idx+1



def retrieveDataTypeHowmuch(WorkingDirectory,StartClass,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClass+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)
        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeHowmuch is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeHowmuch(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveDataTypeWho(WorkingDirectory,StartClassPerson,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClassPerson+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeWho is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeWho(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveDataTypeWhen(WorkingDirectory,StartClass,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClass+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeWhen is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeWhen(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False




def retrieveDataTypeWhat(WorkingDirectory,StartClass,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClass+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeWhat is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeWhat(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveDataTypeMemb(WorkingDirectory,StartClassMemb,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClassMemb+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeWho is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeMemb(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveDataTypeStatus(WorkingDirectory,StartClassStatus,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClassStatus+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeStatus is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeStatus(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveDataTypeCmpProp(WorkingDirectory,StartClassCmpProp,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_DataType=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClassCmpProp+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeCmpProp is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeCmpProp(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_DataType=1

    if (Flag_DataType==1):
        return True
    else:
        return False


def retrieveDataTypeEntity(WorkingDirectory,StartClassEnt,propName,itk_loc1,itk_loc2):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    slotTypeList={}
    slotTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    Flag_Ins=0
    qSubClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  Distinct ?varProperty ?varTypeslot
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass ;
                                 rdfs:range ?varTypeslot .
                    FILTER (CONTAINS (  str(?varClass), '"""+StartClassEnt+"""') && CONTAINS (  str(?varProperty), '"""+propName+"""'))
                }""")
    i=0
    for row in qSubClass:
        itemdig=""
        seq1=str(itk_loc1),str(itk_loc2),str(i)
        itemdig=itemdig.join(seq1)
        intitem=str(itemdig)

        slotTypeList[i]=str(row)
        print "Data Type in retrieveDataTypeEntity is:",slotTypeList[i]
        slotTemp[i]=slotTypeList[i].split('),')
        SlotTypeTemp=str(slotTemp[i])
        if (SlotTypeTemp.find("rdf-schema#label")!=-1) or (SlotTypeTemp.find("#type")!=-1) or (SlotTypeTemp.find("rdf-schema#Literal")!=-1) or (SlotTypeTemp.find("rdf-schema#Resource")!=-1) :
            continue
        slotTemp[i][0]=slotTemp[i][0].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit('/rdf')[-1]
        slotTemp[i][1]=slotTemp[i][1].rsplit("rdf-schema#")[-1]
        # instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]
        slotTemp[i][0]=slotTemp[i][0].rstrip("'),)")
        slotTemp[i][1]=slotTemp[i][1].rstrip("'),)")

        Qvar.addBoundedSlotTypeEnt(slotTemp[i],slotTemp[i][0],slotTemp[i][1],intitem,i)
        i=i+1
        Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveInstanceHowmuch(WorkingDirectory,StartClassHowmuch,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassHowmuch+"""'))

            }""")
     # ?varSlot  ^^xsd:type ?type.
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "InstanceHowmuch for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstHowmuch_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceHowmuch(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    # print "NO. of INSTANCES for Token Person:",itk,"is:", i
    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveInstanceWho(WorkingDirectory,StartClassWho,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassWho+"""'))

            }""")
     # ?varSlot  ^^xsd:type ?type.
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Who for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstWho_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceWho(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    # print "NO. of INSTANCES for Token Person:",itk,"is:", i
    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveInstanceWhen(WorkingDirectory,StartClassWhen,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?instanceLabel
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdfs:label ?instanceLabel ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassWhen+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "When for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT When:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        if Qvar.addBoundedInstanceWhen(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveInstanceWhat(WorkingDirectory,StartClassWhat,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassWhat+"""'))

            }""")

    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "What for retrieveInstanceWhat   are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstWhat_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceWhat(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    # print "NO. of INSTANCES for Token Person:",itk,"is:", i
    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveInstanceMemb(WorkingDirectory,StartClassMemb,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassMemb+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Memb for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstWho_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceMemb(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveInstanceStatus(WorkingDirectory,StartClassStatus,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassStatus+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Status for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstWho_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceStatus(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False




def retrieveInstanceCmpProp(WorkingDirectory,StartClassCmpProp,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassCmpProp+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "CmpProp for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        if Qvar.addBoundedInstanceCmpProp(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveInstanceEntity(WorkingDirectory,StartClassEnt,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassEnt+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Entity for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstEnt_name=string.lower(instanceTemp[itk,i][2])
        if Qvar.addBoundedInstanceEnt(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False



def retrieveInstancePerson(WorkingDirectory,StartClassPer,StartSlotPer,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp=str(StartClassPer)
    slotTemp=str(StartSlotPer)
    print "classTemp,slotTemp: ",classTemp,slotTemp
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?instanceLabel
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdfs:label ?instanceLabel ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+classTemp+"""') && CONTAINS (  str(?varSlot), '"""+slotTemp+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Person for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        if Qvar.addBoundedInstancePerson(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveInstanceAction(WorkingDirectory,StartClassAction,StartSlotAction,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?instanceLabel
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdfs:label ?instanceLabel ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClassAction+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print "Action for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        # if i==0:
        #     print "The result of INSTANCES  for EAT Where_in:",itk,  "are: *****************","\n"

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        if Qvar.addBoundedInstanceAction(instanceTemp[itk,i],itk,i):
            i=i+1
            Flag_Ins=1

    if (Flag_Ins==1):
        return True
    else:
        return False


def retrieveAllInstance(WorkingDirectory,StartClassType,StartClass,StartSlot,tkItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    itk=tkItem
    Flag_Ins=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?varClass ?varSlot ?varInstance ?type
            WHERE  {
                ?a ?varSlot   ?varInstance ;
                   rdf:type ?varClass.
                FILTER (CONTAINS ( str(?varClass), '"""+StartClass+"""') && CONTAINS( str(?varSlot), '"""+StartSlot+"""'))

            }""")
    i=0
    for row in qSubClass:
        instanceList[itk,i]=str(row)
        print StartClassType, " for EAT instances are:",instanceList[itk,i]
        instanceTemp[itk,i]=instanceList[itk,i].split('),')
        strTemp=str(instanceTemp[itk,i])
        if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
            continue
        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

        instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
        instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
        instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
        InstWhat_name=string.lower(instanceTemp[itk,i][2])
        addboundedInstanceTemp="addBoundedInstance" + StartClassType + "(instanceTemp[itk,i],itk,i)"
        # print "addboundedInstanceTemp: ", addboundedInstanceTemp
        addInstance="Qvar." + str(addboundedInstanceTemp)
        exec(addInstance)
        i=i+1


def isWhere_in_Ont(s,WorkingDirectory,whereSC):
    from rule import  isWhere
    from rule import currentRule
    Qvar=currentRule
    tks=s._get_tokens()
    flag=0
    if isWhere(s,Qvar,0):
        list_Dep=s.sint._dependencies
        for lst_Dep in list_Dep:
            if str(lst_Dep[2])=="prep_in":
                itkW=lst_Dep[1]
                flag=1
    if flag==1:
        tks=s._get_tokens()
        tk = tks[itkW]
        if tk._ne()=='LOC' or tk._ne()=='LOCATION':
            return False
    else:
        return False
    print "Was  not found Location in token as Entity in isWhere_in_ont!! looking to ontology...:", itkW
    wrd_loc=tk._word()
    wrds_loc=string.lower(wrd_loc)
    lma_loc=tk._lemma()
    lmas_loc=string.lower(lma_loc)
    pos_loc=tk._pos()
    tempBoundedClass=Qvar.boundedClass
    i=0
    for item0,item1 in tempBoundedClass.keys():
        itemstrp1=item0.strip('S')
        item=itemstrp1.strip('I')
        intitem=int(item)
        print "item0,intitem, class", item0,item1,intitem, tempBoundedClass.values()
        if (intitem==itkW):
            return True

    tempBoundedSlot=Qvar.boundedSlot
    i=0
    for item0,item1 in tempBoundedSlot.keys():
        intitem=int(item0)
        print "item0,, class", item0, tempBoundedSlot.values()
        if (intitem==itkW):
            return True

    tempBoundedInstance=Qvar.boundedInstance
    i=0
    for item0,item1 in tempBoundedInstance.keys():
        intitem=int(item0)
        print "item0, Instance", item0, tempBoundedInstance.values()
        if (intitem==itkW):
            return True

    return False


def bindWhere_in_Ont(s,WorkingDirectory,itkW):
    global currentRuleS
    from rule import currentRule
    Qvar=currentRule
    Flag=0

    tks=s._get_tokens()
    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_in":
            itkW=lst_Dep[1]
            Qvar.addBoundedVars('tk_WhereIn',itkW)
            Flag=1


    if Flag==1:
        return True
    else:
        return False


