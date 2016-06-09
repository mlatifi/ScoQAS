__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        ExpectedAnswerTypes.py
#
# Author:      Majid
#
# Created:     2015/01/29
# Functions to Find Answer Type for QAS



import string
import re
from logilab import *
from managingOntology import *
from auxiliar import SINT
from representingSentences import *
from Recursive_SPARQL_Ontology import *
from rule import *


def addEAT2prolog_Class(r,s):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    # print "EAT for Prolog", text2Prolog
    graph2prologfile = open(path + "mergePrologGraph.txt", 'a+')
    Const_EAT=s._constraints.getConstraints()
    VArg_EAT=s._constraints.getVars()
    for VArg in VArg_EAT:
        print "str(VArg._argument), VArg._var", str(VArg._argument),VArg._var
    i=0
    j=0
    instText="EAT_instance" + "\t"
    classText="EAT_class" + "\t"
    exactAnswer="Exact_Answer" + "\t"
    for c in Const_EAT:
        strPred=str(c._predicate)
        if strPred.startswith("EAT_inst_"):
            print '\t', c._predicate+'('+ str(map(str,c._arguments)) +')', 'involving variables', c._vars
            instText= instText + str(c._arguments[0]) + "," + "\t"
            i=i+1
        elif strPred.startswith("EAT_class_"):
            print '\t', c._predicate+'('+ str(map(str,c._arguments)) +')', 'involving variables', c._vars
            classText= classText + str(c._arguments[0]) + "," + "\t"
            j=j+1

    print "NO of EAT-Inst is:", i
    print "NO of EAT-Class is:", j

    # EATClass2Prolog=Qvar.boundedClassWhat
    # classText="EAT" + "\t"
    # for item in Qvar.boundedClassWhat:
    #     classText= classText + str(EATClass2Prolog[item]) + "," + "\t"
    # text2Prolog=Qvar.boundedSlotTypeWhat
    # for item0, item1 in Qvar.boundedSlotTypeWhat:
    #     classText= classText + str(text2Prolog[item0,item1][1]) + "," + "\t"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.write(instText)
    graph2prologfile.write("\n")
    graph2prologfile.close()


def combine_tk_sequence(s,itkList,lenType):
    seqWord=""
    tks=s._get_tokens()
    for itk in range(len(tks)):
        Flag=0
    j=0
    while(j<lenType):
        typeIdx=isinstance(itkList[j],list)
        print "type of tk_sequence is:",itkList[j],typeIdx
        if typeIdx==True:
            ln=len(itkList[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkList[j]
            else:
                itkW=itkList[j][i]
            tk = tks[itkW]
            wrd=tk._word()
            seqWord=seqWord + " " + wrd
            i=i+1
        j=j+1

    print "sequence of word is :", seqWord
    return seqWord


def obtainEATsWhere_Person_Action(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagPer=0
    flagAct=0
    itkType=[]
    itkAct=[]
    itkPer=[]

    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values):
                print "tk_Type valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_PER" and r.boundedVars['tk_PER']==values):
                itkPer.append(values)
                flagPer=1
            elif (BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values):
                itkAct.append(values)
                flagAct=1

    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of Where Type:",itkType, lnType
        combWord=combine_tk_sequence(s,itkType,lnType)
        findWhereType_in_GeneralOntology(WDirectory,lnType,itkType,combWord)
    if flagPer==1:
        lnPer=len(itkPer)
        print "Len of Person:",itkPer, lnPer
        findItem_in_GeneralOntology(WDirectory,lnPer,itkPer,"Person")
    if flagAct==1:
        lnAct=len(itkAct)
        print "Len of Action:",itkAct, lnAct
        findItem_in_GeneralOntology(WDirectory,lnAct,itkAct,"Action")


def obtainEATsWho_Properties_Person(r,s,WDirectory):

    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    stritem={}
    intitem={}

    Flag=0
    itkW=0
    list_Cls_Who=[]
    list_Slot_Who=[]
    list_Inst_Who=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                print "tk_Type valuse",values
                itkType=values
                Flag=1

    if Flag==0:
        return True
    typeIdx=isinstance(itkType,list)
    print "type of Who_Properties_Person is:",itkType,typeIdx
    if typeIdx==True:
        ln=len(itkType)
        print "Len of itkType: ", ln
    else:
        ln=1
    i=0
    while (i< ln):
        if ln==1:
            itkW=itkType
        else:
            itkW=itkType[i]
        lstitkWClass.clear()
        tk_whoType=str(itkW)
        tempBoundedClass=Qvar.boundedClass
        j=0
        for item0,item1 in tempBoundedClass.keys():
            intItemType=removeAlphabetfromIdx(item0)
            print "r.boundedVars['tk_PER']", r.boundedVars['tk_PER']
            if (str(intitem)==str(itkW)) and (str(itkW) ==str(r.boundedVars['tk_PER'])):
                lstitkWClass[item0,item1]=tempBoundedClass[item0,item1]
                stritem[item0,item1]=removeNumberfromIdx(item0)
                intitem[item0,item1]=intItemType
                j=j+1

        print "Class Who Retrieved in bindWho in :itkW", itkW,lstitkWClass
        if len(lstitkWClass)==0:
            i=i+1
            continue

        bindingEATs_Ontology(WDirectory,lstitkWClass,stritem,intitem,tk_whoType)
        classWTemp=Qvar.boundedClassWho
        print "Checking boundedClassWho", Qvar.boundedClassWho
        slotWTemp=Qvar.boundedSlotWho
        for itemSlot0,itemSlot1 in Qvar.boundedSlotWho:
            slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
            DTWho=retrieveDataTypeWho(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
            if DTWho==True:
                list_Slot_Who.append(slotArg)
        tempBoundedSlottype=Qvar.boundedSlotTypeWho
        print "Index of Qvar.boundedSlotTypeWho", Qvar.boundedSlotTypeWho
        for item0,item1 in Qvar.boundedSlotTypeWho:
            intitem=removeAlphabetfromIdx(item0)
            print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeWho",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
            retrieveInstanceWho(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)
        i=i+1

    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedClassWho,",tk_whoType,Qvar.boundedClassWho,"\n"
    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotWho,",Qvar.boundedSlotWho,"\n"
    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedInstanceWho,",Qvar.boundedInstanceWho,"\n"
    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotTypeWho,",Qvar.boundedSlotTypeWho,"\n"



def obtainEATsWho_CompoundProperties_Person_Action(r,s,WDirectory):

    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    stritem={}
    intitem={}
    Flag=0
    itkW=0
    list_Cls_Who=[]
    list_Slot_Who=[]
    list_Inst_Who=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                print "tk_Type valuse",values
                itkType=values
                Flag=1

    if Flag==0:
        return True
    typeIdx=isinstance(itkType,list)
    print "type of Who_CompoundProperties_Person_Action is:",itkType,typeIdx
    if typeIdx==True:
        ln=len(itkType)
    else:
        ln=1
    i=0
    while (i< ln):
        if ln==1:
            itkW=itkType
        else:
            itkW=itkType[i]
        lstitkWClass.clear()
        tk_whoType=str(itkW)
        tempBoundedClass=Qvar.boundedClass
        j=0
        for item0,item1 in tempBoundedClass.keys():
            intItemType=removeAlphabetfromIdx(item0)
            if str(intItemType)==tk_whoType:
                print "Result : Founded bounded person, tk_whoType: tempBoundedClass[item0,item1] : ", str(itkW),tk_whoType, tempBoundedClass[item0,item1]
                lstitkWClass[item0,item1]=tempBoundedClass[item0,item1]
                stritem[item0,item1]=removeNumberfromIdx(item0)
                intitem[item0,item1]=intItemType
                j=j+1

        print "Class Who Retrieved in bindWho in :itkW", itkW,lstitkWClass
        if len(lstitkWClass)==0:
            i=i+1
            continue

        bindingEATsWho_Ontology(WDirectory,lstitkWClass,stritem,intitem,tk_whoType)

        classWTemp=Qvar.boundedClassWho
        print "Checking boundedClassWho", Qvar.boundedClassWho
        slotWTemp=Qvar.boundedSlotWho
        for itemSlot0,itemSlot1 in Qvar.boundedSlotWho:
            slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
            DTWho=retrieveDataTypeWho(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
            if DTWho==True:
                list_Slot_Who.append(slotArg)

        tempBoundedSlottype=Qvar.boundedSlotTypeWho
        print "Index of Qvar.boundedSlotTypeWho", Qvar.boundedSlotTypeWho
        for item0,item1 in Qvar.boundedSlotTypeWho:
            intitem=removeAlphabetfromIdx(item0)
            print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeWho",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
            retrieveInstanceWho(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)
        i=i+1

    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedClassWho,",tk_whoType,Qvar.boundedClassWho,"\n"
    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotWho,",Qvar.boundedSlotWho,"\n"
    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedInstanceWho,",Qvar.boundedInstanceWho,"\n"
    print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotTypeWho,",Qvar.boundedSlotTypeWho,"\n"


def obtainEATsWho_Member_CompoundProperties(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagMemb=0
    itkType=[]
    itkMemb=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values) :
                print "tk_Type valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_Memb" and r.boundedVars['tk_Memb']==values):
                print "just tk_membs"
                itkMemb.append(values)
                flagMemb=1

    if flagType==0 and flagMemb==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of Type:",itkType, lnType
        findWhoType_in_GeneralOntology(WDirectory,lnType,itkType)
    if flagMemb==1:
        lnMemb=len(itkMemb)
        print "Len of Memb:",itkMemb, lnMemb
        findMemb_in_GeneralOntology(WDirectory,lnMemb,itkMemb)


def obtainEATsWhat_Action_Properties_Status(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagStatus=0
    itkType=[]
    itkStatus=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values)or ((BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values) and r.boundedVars['tk_Prop']< r.boundedVars['tk_Type']):
                print "tk_Type valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_Status" and r.boundedVars['tk_Status']==values)or ((BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values) and r.boundedVars['tk_Prop']< r.boundedVars['tk_Status'] and r.boundedVars['tk_Prop']> r.boundedVars['tk_ACT']):
                print "tk_Status with Properties valuse",values
                itkStatus.append(values)
                flagStatus=1

    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of What Type:",itkType, lnType
        findWhatType_in_GeneralOntology(WDirectory,lnType,itkType)
    if flagStatus==1:
        lnStatus=len(itkStatus)
        print "Len of Status:",itkStatus, lnStatus
        findItem_in_GeneralOntology(WDirectory,lnStatus,itkStatus,"Status")



def obtainEATsWhat_CompoundProperties(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagCmpProp=0
    itkType=[]
    itkCmpProp=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values):
                print "tk_Type for What values: ",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values):
                valuesType=isinstance(values,list)
                if valuesType==True:
                    lnValues=len(values)
                    for item in values:
                        itkCmpProp.append(item)
                else:
                    itkCmpProp.append(values)
                flagCmpProp=1

    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of What Type:",itkType, lnType
        combWord=combine_tk_sequence(s,itkType,lnType)
        findWhatType_in_GeneralOntology(WDirectory,lnType,itkType,combWord)
    if flagCmpProp==1:
        lnCmpProp=len(itkCmpProp)
        print "Len of CmpProp:",itkCmpProp, lnCmpProp
        findItem_in_GeneralOntology(WDirectory,lnCmpProp,itkCmpProp,"CmpProp")


def obtainEATsWhat_CompoundProperties_Entity(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagMemb=0
    itkType=[]
    itkMemb=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values)  or ((BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values) and r.boundedVars['tk_CmpProp']< r.boundedVars['tk_Type']):
                print "tk_Type for What values: ",values
                itkType.append(values)
                flagType=1

    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of What Type:",lnType,itkType,
        findWhatType_in_GeneralOntology(WDirectory,lnType,itkType)


def obtainEATsWhat_Properties_Entity(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagEnt=0
    itkType=[]
    itkEnt=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values) :
                print "tk_Type for What values: ",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values):
                print "just tk_Entity"
                itkEnt.append(values)
                flagEnt=1

    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of What Type:",lnType,itkType,
        findWhatType_in_GeneralOntology(WDirectory,lnType,itkType)
    if flagEnt==1:
        lnEnt=len(itkEnt)
        print "Len of Entity:",itkEnt, lnEnt
        findEntity_in_GeneralOntology(WDirectory,lnEnt,itkEnt)


def obtainEATsHowmuch_Properties_Person(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagPer=0
    itkType=[]
    itkPer=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values) :
                print "tk_Type valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_PER" and r.boundedVars['tk_PER']==values):
                print "just tk_PER"
                itkPer.append(values)
                flagPer=1
    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of Howmuch Type:",itkType, lnType
        findHowmuchType_in_GeneralOntology(WDirectory,lnType,itkType)
    if flagPer==1:
        lnPer=len(itkPer)
        print "Len of Person:",itkPer, lnPer
        findPer_in_GeneralOntology(WDirectory,lnPer,itkPer)


def obtainEATsHowmuch_CompoundProperties(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagCmpProp=0
    itkType=[]
    itkCmpProp=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values):
                print "tk_Type valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values):
                itkCmpProp.append(values)
                flagCmpProp=1
    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of Howmuch Type:",itkType, lnType
        combWord=combine_tk_sequence(s,itkType,lnType)
        findHowmuchType_in_GeneralOntology(WDirectory,lnType,itkType,combWord)
    if flagCmpProp==1:
        lnCmpProp=len(itkCmpProp)
        print "Len of CmpProp:",itkCmpProp, lnCmpProp
        findItem_in_GeneralOntology(WDirectory,lnCmpProp,itkCmpProp,"CmpProp")



def findWhereType_in_GeneralOntology(WDirectory,lenType,itkType,combineWords):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    strInsitem={}
    strClsitem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    flagCls=0
    flagIns=0
    itkW=0
    list_Cls_Where=[]
    list_Slot_Where=[]
    list_Inst_Where=[]
    j=0
    while(j<lenType):
        typeIdx=isinstance(itkType[j],list)
        print "type of WhereType is:",itkType[j],typeIdx
        if typeIdx==True:
            ln=len(itkType[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkType[j]
            else:
                itkW=itkType[j][i]
            lstitkWClass.clear()
            tk_WhereType=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemType=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_WhereType", intItemType, tk_WhereType
                if str(intItemType)==tk_WhereType:
                    print "Class type(item0),type(item1), str(itkW),tk_WhereType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_WhereType, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    strClsitem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemType
                    flagCls=1

            print "Class Where Retrieved in bindWhere in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_WhereType in instance", intItemType, tk_WhereType
                    if str(intItemType)==tk_WhereType:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        strInsitem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1
            i=i+1
        j=j+1

    if flagCls==1:
        print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
        bindingEATsWhere_Ontology(WDirectory,lstitkWClass,strClsitem,intClsitem)
    elif flagIns==1:
        print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass
        bindingEATsWhere_Ontology(WDirectory,lstitkWClass,strInsitem,intInsitem)
    classWTemp=Qvar.boundedClassWhere
    slotWTemp=Qvar.boundedSlotWhere
    for item0,item1 in Qvar.boundedSlotWhere:
        print "itkW, item0,item1 : boundedSlotWhere",itkW, item0,item1,slotWTemp[item0,item1]
        # slot_Threshold=percent_diff(slotWTemp[item0,item1][1],combineWords)
        # print "test threshold: ", slot_Threshold
        # if slot_Threshold>0.7:
        #     print "slotWTemp[item0,item1][1] is OK:", slotWTemp[item0,item1][1]
        retrieveAllInstance(WDirectory,"Where",slotWTemp[item0,item1][0],slotWTemp[item0,item1][1],item0)
    for itemSlot0,itemSlot1 in Qvar.boundedSlotWhere:
        slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
        # slot_Threshold=percent_diff(slotArg,combineWords)
        # print "test threshold for data type ", slot_Threshold
        # if slot_Threshold>0.7:
        #     print "slot_Threshold for data type when slotWTemp[item0,item1][1] is OK:", slotWTemp[itemSlot0,itemSlot1][1]
        DTWhere=retrieveDataTypeWhere(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
        if DTWhere==True:
            list_Slot_Where.append(slotArg)
    tempBoundedSlottype=Qvar.boundedSlotTypeWhere
    print "Index of Qvar.boundedSlotTypeWhere: ", Qvar.boundedSlotTypeWhere
    for item0,item1 in Qvar.boundedSlotTypeWhere:
        intitem=removeAlphabetfromIdx(item0)
        print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeWhere",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
        retrieveInstanceWhere(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)

    print "\n","NOTE:    WhereType was found in Ontology, Qvar.boundedClassWhere,",Qvar.boundedClassWhere,"\n"
    print "\n","NOTE:    WhereType was found in Ontology, Qvar.boundedSlotWhere,",Qvar.boundedSlotWhere,"\n"
    print "\n","NOTE:    WhereType was found in Ontology, Qvar.boundedInstanceWhere,",Qvar.boundedInstanceWhere,"\n"
    print "\n","NOTE:    WhereType was found in Ontology, Qvar.boundedSlotTypeWhere,",Qvar.boundedSlotTypeWhere,"\n"


def findHowmuchType_in_GeneralOntology(WDirectory,lenType,itkType,combineWords):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    strInsitem={}
    strClsitem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    flagCls=0
    flagIns=0
    itkW=0
    list_Cls_Howmuch=[]
    list_Slot_Howmuch=[]
    list_Inst_Howmuch=[]
    j=0
    while(j<lenType):
        typeIdx=isinstance(itkType[j],list)
        print "type of HowmuchType is:",itkType[j],typeIdx
        if typeIdx==True:
            ln=len(itkType[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkType[j]
            else:
                itkW=itkType[j][i]
            lstitkWClass.clear()
            tk_HowmuchType=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemType=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_HowmuchType", intItemType, tk_HowmuchType
                if str(intItemType)==tk_HowmuchType:
                    print "Class type(item0),type(item1), str(itkW),tk_HowmuchType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_HowmuchType, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    strClsitem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemType
                    flagCls=1

            print "Class Howmuch Retrieved in bindHowmuch in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_HowmuchType in instance", intItemType, tk_HowmuchType
                    if str(intItemType)==tk_HowmuchType:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        strInsitem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1
            i=i+1
        j=j+1

    if flagCls==1:
        print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
        bindingEATsHowmuch_Ontology(WDirectory,lstitkWClass,strClsitem,intClsitem)
    elif flagIns==1:
        print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass
        bindingEATsHowmuch_Ontology(WDirectory,lstitkWClass,strInsitem,intInsitem)
    classWTemp=Qvar.boundedClassHowmuch
    slotWTemp=Qvar.boundedSlotHowmuch
    for item0,item1 in Qvar.boundedSlotHowmuch:
        print "itkW, item0,item1 : boundedSlotHowmuch",itkW, item0,item1,slotWTemp[item0,item1]
        slot_Threshold=percent_diff(slotWTemp[item0,item1][1],combineWords)
        print "test threshold: ", slot_Threshold
        if slot_Threshold>0.7:
            print "slotWTemp[item0,item1][1] is OK:", slotWTemp[item0,item1][1]
            retrieveAllInstance(WDirectory,"Howmuch",slotWTemp[item0,item1][0],slotWTemp[item0,item1][1],item0)
    for itemSlot0,itemSlot1 in Qvar.boundedSlotHowmuch:
        slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
        slot_Threshold=percent_diff(slotArg,combineWords)
        print "test threshold for data type ", slot_Threshold
        if slot_Threshold>0.7:
            print "slot_Threshold for data type when slotWTemp[item0,item1][1] is OK:", slotWTemp[itemSlot0,itemSlot1][1]
            DTHowmuch=retrieveDataTypeHowmuch(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
            if DTHowmuch==True:
                list_Slot_Howmuch.append(slotArg)
    tempBoundedSlottype=Qvar.boundedSlotTypeHowmuch
    print "Index of Qvar.boundedSlotTypeHowmuch", Qvar.boundedSlotTypeHowmuch
    for item0,item1 in Qvar.boundedSlotTypeHowmuch:
        intitem=removeAlphabetfromIdx(item0)
        print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeHowmuch",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
        retrieveInstanceHowmuch(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)

    print "\n","NOTE:    HowmuchType was found in Ontology, Qvar.boundedClassHowmuch,",Qvar.boundedClassHowmuch,"\n"
    print "\n","NOTE:    HowmuchType was found in Ontology, Qvar.boundedSlotHowmuch,",Qvar.boundedSlotHowmuch,"\n"
    print "\n","NOTE:    HowmuchType was found in Ontology, Qvar.boundedInstanceHowmuch,",Qvar.boundedInstanceHowmuch,"\n"
    print "\n","NOTE:    HowmuchType was found in Ontology, Qvar.boundedSlotTypeHowmuch,",Qvar.boundedSlotTypeHowmuch,"\n"


def obtainEATsWhen_Person(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagPer=0
    itkType=[]
    itkPer=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if (BVars=="tk_Type" and r.boundedVars['tk_Type']==values) :
                print "tk_Type valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_PER" and r.boundedVars['tk_PER']==values):
                print "just tk_PER"
                itkPer.append(values)
                flagPer=1
    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of When Type:",itkType, lnType
        findWhenType_in_GeneralOntology(WDirectory,lnType,itkType)
    if flagPer==1:
        lnPer=len(itkPer)
        print "Len of Person:",itkPer, lnPer
        findPer_in_GeneralOntology(WDirectory,lnPer,itkPer)


def obtainEATsWhen_Person_Properties(r,s,WDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    flagType=0
    flagPer=0
    itkType=[]
    itkPer=[]
    boundedValues=sorted(r.boundedVars.values())
    for values in boundedValues:
        for BVars in r.boundedVars:
            if ((BVars=="tk_Type" and r.boundedVars['tk_Type']==values)) or ((BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values) and r.boundedVars['tk_Prop']< r.boundedVars['tk_Type']):
                print "tk_Type or tk_Prop valuse",values
                itkType.append(values)
                flagType=1
            elif (BVars=="tk_PER" and r.boundedVars['tk_PER']==values):
                print "just tk_PER"
                itkPer.append(values)
                flagPer=1
    if flagType==0:
        return True
    if flagType==1:
        lnType=len(itkType)
        print "Len of When Type:",itkType, lnType
        combWord=combine_tk_sequence(s,itkType,lnType)
        findWhenType_in_GeneralOntology(WDirectory,lnType,itkType,combWord)
    if flagPer==1:
        lnPer=len(itkPer)
        print "Len of Person:",itkPer, lnPer
        findPer_in_GeneralOntology(WDirectory,lnPer,itkPer)


def findItem_in_GeneralOntology(WDirectory,lenItem,itkItem,Item):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    strInsitem={}
    strClsitem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    flagCls=0
    flagIns=0
    itkW=0
    list_Cls_Item=[]
    list_Slot_Item=[]
    list_Inst_Item=[]
    j=0
    while(j<lenItem):
        flagCls=0
        flagIns=0
        typeIdx=isinstance(itkItem[j],list)
        print "type of itkItem is:",itkItem[j],typeIdx
        if typeIdx==True:
            ln=len(itkItem[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkItem[j]
            else:
                itkW=itkItem[j][i]
            lstitkWClass.clear()
            tk_Item=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intClsItem0=removeAlphabetfromIdx(strItem0)
                intClsItem1=removeAlphabetfromIdx(strItem1)
                # print "intItemType,tk_Item", intClsItem0, tk_Item
                if str(intClsItem0)==tk_Item:
                    print "Class type(item0),type(item1), str(itkW),tk_Item, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_Item, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    strClsitem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intClsItem0,intClsItem1
                    flagCls=1

            print "Class Item Retrieved in bindItem in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intInstItem0=removeAlphabetfromIdx(strItem0)
                    print "intInstItem0,tk_Item in instance", intInstItem0, tk_Item
                    if str(intInstItem0)==tk_Item:
                        print "Instance strItem0, item[1], tempBoundedInst[item]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        strInsitem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intInstItem0
                        flagIns=1
            i=i+1
        j=j+1

    if flagCls==1:
        print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
        bindingEATsItem_Ontology="bindingEATs" + Item + "_Ontology(WDirectory,lstitkWClass,strClsitem,intClsitem)"
        eval(bindingEATsItem_Ontology)

    elif flagIns==1:
        print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass
        bindingEATsItem_Ontology="bindingEATs" + Item + "_Ontology(WDirectory,lstitkWClass,strInsitem,intInsitem)"
        eval(bindingEATsItem_Ontology)
    boundedClassItem="Qvar.boundedClass" + Item
    classItemTemp=eval(boundedClassItem)
    boundedSlotItem="Qvar.boundedSlot" + Item
    slotItemTemp=eval(boundedSlotItem)
    print "slotItemTemp before retrive datatype ", Item, slotItemTemp
    for itemSlot0,itemSlot1 in slotItemTemp:
        slotArg=str(slotItemTemp[itemSlot0,itemSlot1][1])
        retrieveDataTypeItem="retrieveDataType" + Item + "(WDirectory,slotItemTemp[itemSlot0,itemSlot1][0],slotItemTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)"
        DTItem=eval(retrieveDataTypeItem)
        if DTItem==True:
            list_Slot_Item.append(slotArg)

    print "list_Slot_Item for ", Item, list_Slot_Item
    boundedSlotTypeItem="Qvar.boundedSlotType" + Item
    tempBoundedSlotItem=eval(boundedSlotTypeItem)
    print "Index of Qvar.boundedSlotTypeItem", tempBoundedSlotItem
    for item0,item1 in tempBoundedSlotItem:
        intitem=removeAlphabetfromIdx(item0)
        print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeItem",intitem,itkW, item0,item1,tempBoundedSlotItem[item0,item1], tempBoundedSlotItem[item0,item1][0],tempBoundedSlotItem[item0,item1][1]
        retrieveInstanceItem="retrieveInstance" + Item + "(WDirectory,tempBoundedSlotItem[item0,item1][0],tempBoundedSlotItem[item0,item1][1],intitem)"
        eval(retrieveInstanceItem)

    boundedClassItem="Qvar.boundedClass" + Item
    boundedSlotItem="Qvar.boundedSlot" + Item
    boundedSlotTypeItem="Qvar.boundedSlotType" + Item
    boundedInstanceItem="Qvar.boundedInstance" + Item
    print "\n","NOTE:    It was found in Ontology, Qvar.boundedClassItem,",eval(boundedClassItem),"\n"
    print "\n","NOTE:    It was found in Ontology, Qvar.boundedSlotItem,",eval(boundedSlotItem),"\n"
    print "\n","NOTE:    It was found in Ontology, Qvar.boundedInstanceItem,",eval(boundedInstanceItem),"\n"
    print "\n","NOTE:    It was found in Ontology, Qvar.boundedSlotTypeItem,",eval(boundedSlotTypeItem),"\n"


def findWhenType_in_GeneralOntology(WDirectory,lenType,itkType,combineWords):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    strClsitem={}
    strInsitem={}
    intClsitem={}
    intInsitem={}
    Flag=0
    itkW=0
    list_Cls_When=[]
    list_Slot_When=[]
    list_Inst_When=[]
    flagCls=0
    flagIns=0

    j=0
    while(j<lenType):
        # flagCls=0
        # flagIns=0
        typeIdx=isinstance(itkType[j],list)
        print "type of WhenType is:",itkType[j],typeIdx
        if typeIdx==True:
            ln=len(itkType[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkType[j]
            else:
                itkW=itkType[j][i]

            # lstitkWClass.clear()
            tk_whenType=str(itkW)
            # flagCls=0
            # flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemType=removeAlphabetfromIdx(strItem0)
                strItemType=removeNumberfromIdx(strItem0)
                print "intItemType,tk_whenType", intItemType, tk_whenType
                if str(intItemType)==tk_whenType:
                    print "Class type(item0),type(item1), str(itkW),tk_whenType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_whenType, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    strClsitem[strItem0,strItem1]=strItemType
                    intClsitem[strItem0,strItem1]=intItemType
                    flagCls=1

            print "Class When Retrieved in bindWhen in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_whenType in instance", intItemType, tk_whenType
                    if str(intItemType)==tk_whenType:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        strInsitem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1

            i=i+1
        j=j+1
    if flagCls==1:
        # intitem=intClsitem
        print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
        bindingEATsWhen_Ontology(WDirectory,lstitkWClass,strClsitem,intClsitem)
    if flagIns==1:
        # intitem=intInsitem
        print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass
        bindingEATsWhen_Ontology(WDirectory,lstitkWClass,strInsitem,intInsitem)
    classWTemp=Qvar.boundedClassWhen
    slotWTemp=Qvar.boundedSlotWhen
    print "Checking boundedClassWhen and boundedSlotWhen in findWhenType", Qvar.boundedClassWhen,Qvar.boundedSlotWhen
    for item0,item1 in Qvar.boundedSlotWhen:
        print "itkW, item0,item1 : boundedSlotWhen",itkW, item0,item1,slotWTemp[item0,item1]
        slot_Threshold=percent_diff(slotWTemp[item0,item1][1],combineWords)
        print "test threshold: ", slot_Threshold
        if slot_Threshold>0.4:
            print "slotWTemp[item0,item1][1] is OK:", slotWTemp[item0,item1][1]
            retrieveAllInstance(WDirectory,"When",slotWTemp[item0,item1][0],slotWTemp[item0,item1][1],item0)
    for itemSlot0,itemSlot1 in Qvar.boundedSlotWhen:
        slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
        slot_Threshold=percent_diff(slotArg,combineWords)
        print "test threshold for data type ", slot_Threshold
        if slot_Threshold>0.4:
            print "slot_Threshold for data type when slotWTemp[item0,item1][1] is OK:", slotWTemp[itemSlot0,itemSlot1][1]
            DTWhen=retrieveDataTypeWhen(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
            if DTWhen==True:
                list_Slot_When.append(slotArg)
    tempBoundedSlottype=Qvar.boundedSlotTypeWhen
    print "Index of Qvar.boundedSlotTypeWhen", Qvar.boundedSlotTypeWhen
    for item0,item1 in Qvar.boundedSlotTypeWhen:
        intitem=removeAlphabetfromIdx(item0)
        print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeWhen",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
        retrieveInstanceWhen(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)

    print "\n","NOTE:    When was found in Ontology, Qvar.boundedClassWhen,",Qvar.boundedClassWhen,"\n"
    print "\n","NOTE:    When was found in Ontology, Qvar.boundedSlotWhen,",Qvar.boundedSlotWhen,"\n"
    print "\n","NOTE:    When was found in Ontology, Qvar.boundedInstanceWhen,",Qvar.boundedInstanceWhen,"\n"
    print "\n","NOTE:    When was found in Ontology, Qvar.boundedSlotTypeWhen,",Qvar.boundedSlotTypeWhen,"\n"


def findWhatType_in_GeneralOntology(WDirectory,lenType,itkType,combineWords):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    stritem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    strClsitem={}
    strInsitem={}
    Flag=0
    itkW=0
    list_Cls_What=[]
    list_Slot_What=[]
    list_Inst_What=[]
    flagCls=0
    flagIns=0
    j=0
    while(j<lenType):
        typeIdx=isinstance(itkType[j],list)
        print "type of WhatType is:",itkType[j],typeIdx
        if typeIdx==True:
            ln=len(itkType[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkType[j]
            else:
                itkW=itkType[j][i]
            lstitkWClass.clear()
            tk_WhatType=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemType=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_WhatType", intItemType, tk_WhatType
                if str(intItemType)==tk_WhatType:
                    print "Class type(item0),type(item1), str(itkW),tk_WhatType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_WhatType, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    strClsitem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemType
                    flagCls=1

            print "Class What Retrieved in bindWhat in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_WhatType in instance", intItemType, tk_WhatType
                    if str(intItemType)==tk_WhatType:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        strInsitem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1
            i=i+1
        j=j+1

    if flagCls==1:
        print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
        bindingEATsWhat_Ontology(WDirectory,lstitkWClass,strClsitem,intClsitem)
    elif flagIns==1:
        print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass
        bindingEATsWhat_Ontology(WDirectory,lstitkWClass,strInsitem,intInsitem)
    classWTemp=Qvar.boundedClassWhat
    slotWTemp=Qvar.boundedSlotWhat
    for item0,item1 in Qvar.boundedSlotWhat:
        print "itkW, item0,item1, combineWords, slotWTemp[item0,item1] : boundedSlotWhat",itkW, item0,item1,combineWords, slotWTemp[item0,item1]
        slot_Threshold=percent_diff(slotWTemp[item0,item1][1],combineWords)
        print "test threshold: ", slot_Threshold
        if slot_Threshold>0.4:
            print "", slotWTemp[item0,item1][1]
            retrieveAllInstance(WDirectory,"What",slotWTemp[item0,item1][0],slotWTemp[item0,item1][1],item0)
    for itemSlot0,itemSlot1 in Qvar.boundedSlotWhat:
        slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
        slot_Threshold=percent_diff(slotArg,combineWords)
        print "test threshold for data type, combineWords ", slot_Threshold, combineWords
        if slot_Threshold>0.4:
            print "slot_Threshold for data type when slotWTemp[item0,item1][1] is OK:", slotWTemp[itemSlot0,itemSlot1][1]
            DTWhat=retrieveDataTypeWhat(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
            if DTWhat==True:
                list_Slot_What.append(slotArg)
    print "\n","NOTE1:  --->   Qvar.boundedInstanceWhat,",Qvar.boundedInstanceWhat,"\n"
    tempBoundedSlottype=Qvar.boundedSlotTypeWhat
    print "Index of Qvar.boundedSlotTypeWhat", Qvar.boundedSlotTypeWhat
    for item0,item1 in Qvar.boundedSlotTypeWhat:
        intitem=removeAlphabetfromIdx(item0)
        print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeWhat",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
        retrieveInstanceWhat(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)

    print "\n","NOTE:    What was found in Ontology, Qvar.boundedClassWhat,",Qvar.boundedClassWhat,"\n"
    print "\n","NOTE:    What was found in Ontology, Qvar.boundedSlotWhat,",Qvar.boundedSlotWhat,"\n"
    print "\n","NOTE2:    What was found in Ontology, Qvar.boundedInstanceWhat,",Qvar.boundedInstanceWhat,"\n"
    print "\n","NOTE:    What was found in Ontology, Qvar.boundedSlotTypeWhat,",Qvar.boundedSlotTypeWhat,"\n"





def findWhoType_in_GeneralOntology(WDirectory,lenType,itkType):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    stritem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    Flag=0
    itkW=0
    list_Cls_Who=[]
    list_Slot_Who=[]
    list_Inst_Who=[]
    j=0
    while(j<lenType):
        flagCls=0
        flagIns=0
        typeIdx=isinstance(itkType[j],list)
        print "type of WhoType is:",itkType[j],typeIdx
        if typeIdx==True:
            ln=len(itkType[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkType[j]
            else:
                itkW=itkType[j][i]
            lstitkWClass.clear()
            tk_whoType=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemType=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_whoType", intItemType, tk_whoType
                if str(intItemType)==tk_whoType:
                    print "Class type(item0),type(item1), str(itkW),tk_whoType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_whoType, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    stritem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemType
                    flagCls=1

            print "Class Who Retrieved in bindWho in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_whoType in instance", intItemType, tk_whoType
                    if str(intItemType)==tk_whoType:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        stritem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1

            if len(lstitkWClass)==0:
                i=i+1
                continue
            if flagCls==1:
                intitem=intClsitem
                print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
            elif flagIns==1:
                intitem=intInsitem
                print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass

            bindingEATsWho_Ontology(WDirectory,lstitkWClass,stritem,intitem,tk_whoType)

            classWTemp=Qvar.boundedClassWho
            print "Checking boundedClassWho", Qvar.boundedClassWho
            slotWTemp=Qvar.boundedSlotWho
            for itemSlot0,itemSlot1 in Qvar.boundedSlotWho:
                slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
                DTWho=retrieveDataTypeWho(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
                if DTWho==True:
                    list_Slot_Who.append(slotArg)
            tempBoundedSlottype=Qvar.boundedSlotTypeWho
            print "Index of Qvar.boundedSlotTypeWho", Qvar.boundedSlotTypeWho
            for item0,item1 in Qvar.boundedSlotTypeWho:
                intitem=removeAlphabetfromIdx(item0)
                print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeWho",intitem,itkW, item0,item1,tempBoundedSlottype[item0,item1], tempBoundedSlottype[item0,item1][0],tempBoundedSlottype[item0,item1][1]
                retrieveInstanceWho(WDirectory,tempBoundedSlottype[item0,item1][1],intitem)
            i=i+1

        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedClassWho,",Qvar.boundedClassWho,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotWho,",Qvar.boundedSlotWho,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedInstanceWho,",Qvar.boundedInstanceWho,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotTypeWho,",Qvar.boundedSlotTypeWho,"\n"
        j=j+1


def findEntity_in_GeneralOntology(WDirectory,lenEnt,itkEnt):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    stritem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    Flag=0
    itkW=0
    list_Cls_Ent=[]
    list_Slot_Ent=[]
    list_Inst_Ent=[]
    j=0
    while(j<lenEnt):
        flagCls=0
        flagIns=0
        typeIdx=isinstance(itkEnt[j],list)
        print "type of EntityType is:",itkEnt[j],typeIdx
        if typeIdx==True:
            ln=len(itkEnt[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkEnt[j]
            else:
                itkW=itkEnt[j][i]
            lstitkWClass.clear()
            tk_Ent=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemEnt=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_Ent", intItemEnt, tk_Ent
                if str(intItemEnt)==tk_Ent:
                    print "Class type(item0),type(item1), str(itkW),tk_Entity, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_Ent, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    stritem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemEnt
                    flagCls=1

            print "Class Entity Retrieved in findEntity in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_Entity in instance", intItemType, tk_Ent
                    if str(intItemType)==tk_Ent:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        stritem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1

            if len(lstitkWClass)==0:
                i=i+1
                continue
            if flagCls==1:
                intitem=intClsitem
                print "findEntity: intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
            elif flagIns==1:
                intitem=intInsitem
                print "findEntity: intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass

            bindingEATsEntity_Ontology(WDirectory,lstitkWClass,stritem,intitem,tk_Ent)

            classWTemp=Qvar.boundedClassEnt
            print "Checking boundedClassEnt", Qvar.boundedClassEnt
            slotWTemp=Qvar.boundedSlotEnt
            for itemSlot0,itemSlot1 in Qvar.boundedSlotEnt:
                slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
                DTEnt=retrieveDataTypeEntity(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
                if DTEnt==True:
                    list_Slot_Ent.append(slotArg)

            tempBoundedSlotEnt=Qvar.boundedSlotTypeEnt
            print "Index of Qvar.boundedSlotTypeEnt", Qvar.boundedSlotTypeEnt
            for item0,item1 in Qvar.boundedSlotTypeEnt:
                intitem=removeAlphabetfromIdx(item0)
                print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeEnt",intitem,itkW, item0,item1,tempBoundedSlotEnt[item0,item1], tempBoundedSlotEnt[item0,item1][0],tempBoundedSlotEnt[item0,item1][1]
                retrieveInstanceEntity(WDirectory,tempBoundedSlotEnt[item0,item1][1],intitem)
            i=i+1
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedClassEnt,",Qvar.boundedClassEnt,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotEnt,",Qvar.boundedSlotEnt,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedInstanceEnt,",Qvar.boundedInstanceEnt,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotTypeEnt,",Qvar.boundedSlotTypeEnt,"\n"
        j=j+1


def findMemb_in_GeneralOntology(WDirectory,lenMemb,itkMemb):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    stritem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    Flag=0
    itkW=0
    list_Cls_Memb=[]
    list_Slot_Memb=[]
    list_Inst_Memb=[]
    j=0
    while(j<lenMemb):
        flagCls=0
        flagIns=0
        typeIdx=isinstance(itkMemb[j],list)
        print "type of MembType is:",itkMemb[j],typeIdx
        if typeIdx==True:
            ln=len(itkMemb[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkMemb[j]
            else:
                itkW=itkMemb[j][i]
            lstitkWClass.clear()
            tk_Memb=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemMemb=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_Memb", intItemMemb, tk_Memb
                if str(intItemMemb)==tk_Memb:
                    print "Class type(item0),type(item1), str(itkW),tk_whoType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_Memb, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    stritem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemMemb
                    flagCls=1

            print "Class Who Retrieved in bindWho in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_whoType in instance", intItemType, tk_Memb
                    if str(intItemType)==tk_Memb:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        stritem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1

            if len(lstitkWClass)==0:
                i=i+1
                continue
            if flagCls==1:
                intitem=intClsitem
                print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
            elif flagIns==1:
                intitem=intInsitem
                print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass

            bindingEATsMemb_Ontology(WDirectory,lstitkWClass,stritem,intitem,tk_Memb)

            classWTemp=Qvar.boundedClassMemb
            print "Checking boundedClassMemb", Qvar.boundedClassMemb
            slotWTemp=Qvar.boundedSlotMemb
            for itemSlot0,itemSlot1 in Qvar.boundedSlotMemb:
                slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
                DTMemb=retrieveDataTypeMemb(WDirectory,slotWTemp[itemSlot0,itemSlot1][0],slotWTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
                if DTMemb==True:
                    list_Slot_Memb.append(slotArg)

            tempBoundedSlotMemb=Qvar.boundedSlotTypeMemb
            print "Index of Qvar.boundedSlotTypeMemb", Qvar.boundedSlotTypeMemb
            for item0,item1 in Qvar.boundedSlotTypeMemb:
                intitem=removeAlphabetfromIdx(item0)
                print "intitem,itkW, item0,item1, Instance,: boundedSlotTypeMemb",intitem,itkW, item0,item1,tempBoundedSlotMemb[item0,item1], tempBoundedSlotMemb[item0,item1][0],tempBoundedSlotMemb[item0,item1][1]
                retrieveInstanceMemb(WDirectory,tempBoundedSlotMemb[item0,item1][1],intitem)
            i=i+1

        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedClassMemb,",Qvar.boundedClassMemb,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotMemb,",Qvar.boundedSlotMemb,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedInstanceMemb,",Qvar.boundedInstanceMemb,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotTypeMemb,",Qvar.boundedSlotTypeMemb,"\n"
        j=j+1


def findPer_in_GeneralOntology(WDirectory,lenPer,itkPer):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    lstitkW={}
    lstitkWClass={}
    lstitkWIns={}
    stritem={}
    intitem={}
    intClsitem={}
    intInsitem={}
    Flag=0
    itkW=0
    list_Cls_Per=[]
    list_Slot_Per=[]
    list_Inst_Per=[]
    j=0
    while(j<lenPer):
        flagCls=0
        flagIns=0
        typeIdx=isinstance(itkPer[j],list)
        print "type of PersonType is:",itkPer[j],typeIdx
        if typeIdx==True:
            ln=len(itkPer[j])
        else:
            ln=1
        i=0
        while (i< ln):
            if ln==1:
                itkW=itkPer[j]
            else:
                itkW=itkPer[j][i]
            lstitkWClass.clear()
            tk_Per=str(itkW)
            flagCls=0
            flagIns=0
            tempBoundedClass=Qvar.boundedClass
            for item in tempBoundedClass.keys():
                strItem0=str(item[0])
                strItem1=str(item[1])
                intItemPer=removeAlphabetfromIdx(strItem0)
                print "intItemType,tk_Person", intItemPer, tk_Per
                if str(intItemPer)==tk_Per:
                    print "Class type(item0),type(item1), str(itkW),tk_whoType, tempBoundedClass[item0,item1]: ",type(item[0]),type(item[1]), str(itkW),tk_Per, tempBoundedClass[item]
                    lstitkWClass[strItem0,strItem1]=tempBoundedClass[item]
                    stritem[strItem0,strItem1]=removeNumberfromIdx(item[0])
                    intClsitem[strItem0,strItem1]=intItemPer
                    flagCls=1

            print "Class Who Retrieved in bindWho in :itkW", itkW,lstitkWClass
            if flagCls==0:
                tempBoundedInst=Qvar.boundedInstance
                for item in tempBoundedInst.keys():
                    strItem0=str(item[0])
                    strItem1=str(item[1])
                    intItemType=removeAlphabetfromIdx(strItem0)
                    print "intItemType,tk_whoType in instance", intItemType, tk_Per
                    if str(intItemType)==tk_Per:
                        print "Instance strItem0, item1, tempBoundedInst[item0,item1]: ",strItem0, item[1],tempBoundedInst[item]
                        lstitkWClass[strItem0,strItem1]=tempBoundedInst[item][0]
                        stritem[strItem0,strItem1]=""
                        intInsitem[strItem0,strItem1]=intItemType
                        flagIns=1

            if len(lstitkWClass)==0:
                i=i+1
                continue
            if flagCls==1:
                intitem=intClsitem
                print "intClsitem, lstitkWClass  for Cls:",intClsitem, lstitkWClass
            elif flagIns==1:
                intitem=intInsitem
                print "intInsitem, lstitkWClass  for Ins:",intInsitem, lstitkWClass

            bindingEATsPer_Ontology(WDirectory,lstitkWClass,stritem,intitem,tk_Per)

            classWTemp=Qvar.boundedClassPerson
            print "Checking boundedClassPerson", Qvar.boundedClassPerson
            slotWTemp=Qvar.boundedSlotPerson
            for itemSlot in Qvar.boundedSlotPerson:
                slotArg=str(slotWTemp[itemSlot][1])
                DTPer=retrieveDataTypePerson(WDirectory,slotWTemp[itemSlot][0],slotWTemp[itemSlot][1],itemSlot)
                if DTPer==True:
                    list_Slot_Per.append(slotArg)
            tempBoundedSlotPerson=Qvar.boundedSlotTypePerson
            print "Index of Qvar.boundedSlotTypePerson", Qvar.boundedSlotTypePerson
            for item0,item1 in Qvar.boundedSlotTypePerson:
                intitem=removeAlphabetfromIdx(item0)
                print "intitem,itkW, item0,item1, Instance,: boundedSlotTypePerson",intitem,itkW, item0,item1,tempBoundedSlotPerson[item0,item1], tempBoundedSlotPerson[item0,item1][0],tempBoundedSlotPerson[item0,item1][1]
                # retrieveInstancePerson(WDirectory,tempBoundedSlotPerson[item0,item1][1],intitem)
            i=i+1
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedClassPerson,",Qvar.boundedClassPerson,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotPerson,",Qvar.boundedSlotPerson,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedInstancePerson,",Qvar.boundedInstancePerson,"\n"
        print "\n","NOTE:    Who was found in Ontology, Qvar.boundedSlotTypePerson,",Qvar.boundedSlotTypePerson,"\n"
        j=j+1


def bindingEATsWho_Ontology(WDirectory,listClass,strItem,intItem,tk_Type):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    for item in classWTemp.keys():
        print "class Who Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item]:
                print "That is Who Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceWho(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedClassWho(Qvar.boundedInstance[instItem][0],instItem[0],instItem[1])
                flagIns=1

        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item]:
                print "That is Who Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotWho(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassWho(Qvar.boundedSlot[slotItem][0],slotItem[0],slotItem[1])
                flagSlot=1
            # retrieveInstanceWho(WDirectory,classWTemp[item],item)
        print "strItem,flagIns: ", strItem, flagIns
        if str(strItem[item]=="I") and flagIns!=1:
            print "Look for class...."
            retrieveSlotsWho(WDirectory,classWTemp[item],item[0],item[1],tk_Type,1)


def bindingEATsWhere_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    print "listClass, etc: ", listClass
    print "strItem: ",strItem
    print "intItem: ", intItem
    for item in classWTemp.keys():
        print "class Where Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item] and strItem[item]=="I" :
                print "That is Where Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceWhere(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedClassWhere(Qvar.boundedInstance[instItem][0],strItem[item] + str(instItem[0]),instItem[1])
                flagIns=1
        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item] and strItem[item]=="S":
                print "That is Where Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotWhere(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassWhere(Qvar.boundedSlot[slotItem][0],strItem[item] + str(slotItem[0]),slotItem[1])
                flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1, ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is Where Class!!",clsItem,Qvar.boundedClass[clsItem], Qvar.boundedClass[clsItem][0]
                    if Qvar.addBoundedClassWhere(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to Where",Qvar.boundedClass[clsItem]
                        retrieveSlotsWhere(WDirectory,Qvar.boundedClass[clsItem],clsItem[0],clsItem[1],classWTemp[item],1)
                        # retrieveInstanceWhere(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])
                        flagClass=1
        print "strItem,intItem[item],item, flagIns, flagClass: ", strItem[item],intItem[item], item, flagIns, flagClass
    # if flagClass==1:
    #     for slotWhere in Qvar.boundedSlotWhere:
    #     retrieveInstanceWhere(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])


def bindingEATsHowmuch_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    print "listClass, etc: ", listClass
    print "strItem: ",strItem
    print "intItem: ", intItem
    for item in classWTemp.keys():
        print "class howmuch Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item] and strItem[item]=="I" :
                print "That is howmuch Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceHowmuch(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedClassHowmuch(Qvar.boundedInstance[instItem][0],strItem[item] + str(instItem[0]),instItem[1])
                flagIns=1
        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item] and strItem[item]=="S":
                print "That is howmuch Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotHowmuch(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassHowmuch(Qvar.boundedSlot[slotItem][0],strItem[item] + str(slotItem[0]),slotItem[1])
                flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1, ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is howmuch Class!!",clsItem,Qvar.boundedClass[clsItem], Qvar.boundedClass[clsItem][0]
                    if Qvar.addBoundedClassHowmuch(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to howmuch",Qvar.boundedClass[clsItem]
                        retrieveInstanceHowmuch(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])
                        flagClass=1
        print "strItem,intItem[item],item, flagIns, flagClass: ", strItem[item],intItem[item], item, flagIns, flagClass


def bindingEATsWhen_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    print "listClass, etc: ", listClass
    print "strItem: ",strItem
    print "intItem: ", intItem
    # print "tk_Type", tk_Type
    for item in classWTemp.keys():
        print "class When Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item] and strItem[item]=="I" :
                print "That is When Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceWhen(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedClassWhen(Qvar.boundedInstance[instItem][0],strItem[item] + str(instItem[0]),instItem[1])
                flagIns=1
        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item] and strItem[item]=="S":
                print "That is When Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotWhen(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassWhen(Qvar.boundedSlot[slotItem][0],strItem[item] + str(slotItem[0]),slotItem[1])
                flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1, ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is When Class!!",clsItem,Qvar.boundedClass[clsItem], Qvar.boundedClass[clsItem][0]
                    if Qvar.addBoundedClassWhen(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to When",Qvar.boundedClass[clsItem]
                        retrieveInstanceWhen(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])
                        flagClass=1

        print "strItem,intItem[item],item, flagIns, flagClass: ", strItem[item],intItem[item], item, flagIns, flagClass


def bindingEATsWhat_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    print "listClass, etc: ", listClass
    print "strItem: ",strItem
    print "intItem: ", intItem
    for item in classWTemp.keys():
        print "class What Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item] and strItem[item]=="I" :
                print "That is What Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceWhat(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedClassWhat(Qvar.boundedInstance[instItem][0],strItem[item] + str(instItem[0]),instItem[1])
                flagIns=1
        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item] and strItem[item]=="S":
                print "That is What Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotWhat(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassWhat(Qvar.boundedSlot[slotItem][0],strItem[item] + str(slotItem[0]),slotItem[1])
                flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1, ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is what Class!!",clsItem,Qvar.boundedClass[clsItem]
                    if Qvar.addBoundedClassWhat(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to what",Qvar.boundedClassWhat
                        retrieveInstanceWhat(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])
                        flagClass=1
        # if str(strItem[item]=="I") and flagIns!=1:
        #     print "Exception I!!!  Look for class in What ontology..., classWTemp[item]:", classWTemp[item]
        #     retrieveSlotsWhat(WDirectory,classWTemp[item],item[0],item[1],tk_Type,0)

        print "strItem,intItem[item],item, flagIns, flagClass: ", strItem[item],intItem[item], item, flagIns, flagClass
        print "Qvar.boundedInstanceWhat: ", Qvar.boundedInstanceWhat

def bindingEATsEntity_Ontology(WDirectory,listClass,strItem,intItem,tk_Ent):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    for item in classWTemp.keys():
        print "class Entity Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item]:
                print "That is Entity Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceEnt(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedSlotEnt(Qvar.boundedInstance[instItem],Qvar.boundedInstance[instItem][0],Qvar.boundedInstance[instItem][1],instItem[0],instItem[1])
                Qvar.addBoundedClassEnt(Qvar.boundedInstance[instItem][0],instItem[0],instItem[1])
                flagIns=1
        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item]:
                print "That is Entity Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotEnt(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassEnt(Qvar.boundedSlot[slotItem][0],slotItem[0],slotItem[1])
                flagSlot=1
        print "strItem,flagIns: ", strItem, flagIns
        if str(strItem[item]=="I") and flagIns!=1:
            print "Exception I: Look for class Entity...."
            retrieveSlotsEntity(WDirectory,classWTemp[item],item[0],item[1],tk_Ent,1)


def bindingEATsMemb_Ontology(WDirectory,listClass,strItem,intItem,tk_Memb):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    for item in classWTemp.keys():
        print "class Who Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item]:
                print "That is Member Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceMemb(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedSlotMemb(Qvar.boundedInstance[instItem],Qvar.boundedInstance[instItem][0],Qvar.boundedInstance[instItem][1],instItem[0],instItem[1])
                Qvar.addBoundedClassMemb(Qvar.boundedInstance[instItem][0],instItem[0],instItem[1])
                flagIns=1

        for slotItem in Qvar.boundedSlot:
            if slotItem[0]==intItem[item]:
                print "That is Member Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                Qvar.addBoundedSlotMemb(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                Qvar.addBoundedClassMemb(Qvar.boundedSlot[slotItem][0],slotItem[0],slotItem[1])
                flagSlot=1
            # retrieveInstanceWho(WDirectory,classWTemp[item],item)
        print "strItem,flagIns: ", strItem, flagIns
        if str(strItem[item]=="I") and flagIns!=1:
            print "Look for class Member...."
            retrieveSlotsWho(WDirectory,classWTemp[item],item[0],item[1],tk_Memb,1)


def bindingEATsStatus_Ontology(WDirectory,listClass,strItem,intItem,tk_Status):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    for item in classWTemp.keys():
        print "class Status Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item] and strItem[item]=="I":
                print "That is Status Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceStatus(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedSlotStatus(Qvar.boundedInstance[instItem],Qvar.boundedInstance[instItem][0],Qvar.boundedInstance[instItem][1],instItem[0],instItem[1])
                Qvar.addBoundedClassStatus(Qvar.boundedInstance[instItem][0],strItem[item]+ str(instItem[0]),instItem[1])
                flagIns=1
        if flagIns!=1:
            for slotItem in Qvar.boundedSlot:
                if slotItem[0]==intItem[item] and strItem[item]=="S":
                    print "That is Status Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                    Qvar.addBoundedSlotStatus(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                    Qvar.addBoundedClassStatus(Qvar.boundedSlot[slotItem][0],strItem[item]+ str(slotItem[0]),slotItem[1])
                    flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1, ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is Status Class!!",clsItem,Qvar.boundedClass[clsItem], Qvar.boundedClass[clsItem][0]
                    if Qvar.addBoundedClassStatus(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to status",Qvar.boundedClass[clsItem]
                        retrieveInstanceStatus(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])
                        flagClass=1

        print "strItem,flagIns, flagClass: ", strItem, flagIns,flagClass
        # if str(strItem[item]=="I") and flagIns!=1:
        #     print "Look for class Status...."
        #     retrieveSlotsWho(WDirectory,classWTemp[item],item[0],item[1],tk_Status,1)


def bindingEATsCmpProp_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    for item in classWTemp.keys():
        print "class CmpProp Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item] and strItem[item]=="I":
                print "That is Status Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceCmpProp(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedSlotCmpProp(Qvar.boundedInstance[instItem],Qvar.boundedInstance[instItem][0],Qvar.boundedInstance[instItem][1],instItem[0],instItem[1])
                Qvar.addBoundedClassCmpProp(Qvar.boundedInstance[instItem][0],strItem[item]+ str(instItem[0]),instItem[1])
                flagIns=1
        if flagIns!=1:
            for slotItem in Qvar.boundedSlot:
                if slotItem[0]==intItem[item] and strItem[item]=="S":
                    print "That is CmpProp Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                    Qvar.addBoundedSlotCmpProp(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                    Qvar.addBoundedClassCmpProp(Qvar.boundedSlot[slotItem][0],strItem[item]+ str(slotItem[0]),slotItem[1])
                    flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1, ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is CmpProp Class!!",clsItem,Qvar.boundedClass[clsItem], Qvar.boundedClass[clsItem][0]
                    if Qvar.addBoundedClassCmpProp(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to CmpProp: ",Qvar.boundedClass[clsItem]
                        retrieveInstanceCmpProp(WDirectory,Qvar.boundedClass[clsItem],clsItem[0])
                        flagClass=1

        print "strItem,flagIns, flagClass: ", strItem, flagIns,flagClass
        # if str(strItem[item]=="I") and flagIns!=1:
        #     print "Look for class Status...."
        #     retrieveSlotsWho(WDirectory,classWTemp[item],item[0],item[1],tk_Status,1)


def bindingEATsPerson_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    print "strItem,intItem: ", strItem,intItem
    for item in classWTemp.keys():
        print "class Person Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item][0] and instItem[1]==intItem[item][1] and strItem[item]=="I":
                print "That is Person Instances!!",instItem,Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstancePerson(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedSlotPerson(Qvar.boundedInstance[instItem],Qvar.boundedInstance[instItem][0],Qvar.boundedInstance[instItem][1],instItem[0],instItem[1])
                Qvar.addBoundedClassPerson(Qvar.boundedInstance[instItem][0],instItem[0],instItem[1])
                flagIns=1
        if flagIns!=1:
            for slotItem in Qvar.boundedSlot:
                if slotItem[0]==intItem[item][0] and slotItem[1]==intItem[item][1] and strItem[item]=="S":
                    print "That is Person Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                    Qvar.addBoundedSlotPerson(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],slotItem[0],slotItem[1])
                    Qvar.addBoundedClassPerson(Qvar.boundedSlot[slotItem][0],slotItem[0],slotItem[1])
                    flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            arg1=str(item[0])
            arg2=int(item[1])
            clsItem=(arg1,arg2)
            print "That is Person Class!!",clsItem,Qvar.boundedClass[clsItem]
            # Qvar.addBoundedClassPerson(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1])
            retrieveSlotsPerson(WDirectory,Qvar.boundedClass[clsItem],clsItem[0],clsItem[1])
            print "retrieveSlotsPerson after traverse :",Qvar.boundedSlotPerson
            for slotPerson in Qvar.boundedSlotPerson:
                print "slotPerson retrived ....",Qvar.boundedSlotPerson[slotPerson]
                itemdig=""
                seq1=str(slotPerson[0]),str(slotPerson[1])
                itemdig=itemdig.join(seq1)
                intitem=str(itemdig)
                retrieveInstancePerson(WDirectory,Qvar.boundedSlotPerson[slotPerson][0],Qvar.boundedSlotPerson[slotPerson][1],intitem)
            flagClass=1

        print "strItem,flagIns, flagClass in Person: ", strItem, flagIns,flagClass
    print "Note: addBoundedClassPerson :: ", Qvar.boundedClassPerson
    print "Note: addBoundedSlotPerson :: ", Qvar.boundedSlotPerson
    print "Note: addBoundedInstancePerson :: ", Qvar.boundedInstancePerson


def bindingEATsAction_Ontology(WDirectory,listClass,strItem,intItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    classWTemp={}
    classWTemp=listClass
    print "strItem,intItem: ", strItem,intItem
    for item in classWTemp.keys():
        print "class Act Retrieved is :", classWTemp[item],item[0],item[1]
        flagIns=0
        flagSlot=0
        flagClass=0
        for instItem in Qvar.boundedInstance:
            if instItem[0]==intItem[item][0] and instItem[1]==intItem[item][1] and strItem[item]=="I":
                print "instItem[0],instItem[1], That is Action Instances!!",instItem[0],instItem[1],Qvar.boundedInstance[instItem]
                Qvar.addBoundedInstanceAction(Qvar.boundedInstance[instItem],instItem[0],instItem[1])
                Qvar.addBoundedSlotAction(Qvar.boundedInstance[instItem],Qvar.boundedInstance[instItem][0],Qvar.boundedInstance[instItem][1],instItem[0],instItem[1])
                Qvar.addBoundedClassAction(Qvar.boundedInstance[instItem][0],strItem[item]+ str(instItem[0]),instItem[1])
                flagIns=1
        if flagIns!=1:
            for slotItem in Qvar.boundedSlot:
                if slotItem[0]==intItem[item][0] and slotItem[1]==intItem[item][1] and strItem[item]=="S":
                    print "That is Action Slot!!",slotItem,Qvar.boundedSlot[slotItem]
                    Qvar.addBoundedSlotAction(Qvar.boundedSlot[slotItem],Qvar.boundedSlot[slotItem][0],Qvar.boundedSlot[slotItem][1],strItem[item]+ str(slotItem[0]),slotItem[1])
                    Qvar.addBoundedClassAction(Qvar.boundedSlot[slotItem][0],strItem[item]+ str(slotItem[0]),slotItem[1])
                    flagSlot=1
        if flagIns!=1 and flagSlot!=1:
            print "flagIns!=1 and flagSlot!=1 in bindingEATsAction_Ontology  ",intItem[item]
            for clsItem in Qvar.boundedClass:
                if str(clsItem[0])==str(intItem[item]):
                    print "That is Action Class!!",clsItem,Qvar.boundedClass[clsItem], Qvar.boundedClass[clsItem][0]
                    if Qvar.addBoundedClassAction(Qvar.boundedClass[clsItem],clsItem[0],clsItem[1]):
                        print "Class added to Action",Qvar.boundedClass[clsItem]
                        retrieveInstanceAction(WDirectory,Qvar.boundedClass[clsItem][0],Qvar.boundedClass[clsItem][1],clsItem[0])
                        flagClass=1

        print "strItem,flagIns, flagClass in Action: ", strItem, flagIns,flagClass
    print "Note: addBoundedClassAction :: ", Qvar.boundedClassAction
    print "Note: addBoundedSlotAction :: ", Qvar.boundedSlotAction
    print "Note: addBoundedInstanceAction :: ", Qvar.boundedInstanceAction