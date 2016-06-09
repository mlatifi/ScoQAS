__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        Answers.py
#
# Author:      Majid
#
# Created:     2016/04/01
# Functions to Find Exact Answer from Ontology



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
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    Const_EAT=s._constraints.getConstraints()
    VArg_EAT=s._constraints.getVars()
    for VArg in VArg_EAT:
        print "str(VArg._argument), VArg._var", str(VArg._argument),VArg._var
    i=0
    j=0
    k=0
    instText="EAT_instance" + "\t"
    classText="EAT_class" + "\t"
    answerText="Answer" + "\t"

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
        elif strPred.startswith("Answer_"):
            print '\t', c._predicate+'('+ str(map(str,c._arguments)) +')', 'involving variables', c._vars
            for cAnsw in Const_EAT:
                EAT_Pred=str(cAnsw._predicate)
                if (EAT_Pred.startswith("EAT_inst_") or EAT_Pred.startswith("instance_PER_") or EAT_Pred.startswith("instance_ACT_")) and str(cAnsw._arguments[1])==str(c._arguments[0]):
                    answerText= answerText + str(cAnsw._arguments[0]) + "," + "\t"
            k=k+1

    print "NO of EAT-Inst is:", i
    print "NO of EAT-Class is:", j
    print "NO of Exact Answer is:", k

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
    graph2prologfile.write(answerText)
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


def obtainAnswerHowmuch_CompoundProperties(r,s):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    WDirectory=Qvar.workingDir
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    lstitkW={}
    lstitkWClass={}
    itkW=0
    Flag=0
    list_Cls_Howmuch=[]
    list_Slot_Howmuch=[]
    list_Inst_Howmuch=[]
    boundedValues=sorted(r.boundedVars.values())
    print "\n boundedClassHowmuch in Answer Module: ", Qvar.boundedClassHowmuch
    print "\n boundedSlotHowmuch in Answer Module: ", Qvar.boundedSlotHowmuch
    print "\n boundedInstanceHowmuch in Answer Module: ", Qvar.boundedInstanceHowmuch
    answerBoundedClass=Qvar.boundedClassHowmuch
    for item in answerBoundedClass.keys():
        retrieveSlotsAnswer(WDirectory,answerBoundedClass[item],item[0],item[1])
    classAnswerTemp=Qvar.boundedClassAnswer
    slotAnswerTemp=Qvar.boundedSlotAnswer
    slotHmchTemp=Qvar.boundedSlotHowmuch
    print "\n boundedClassAnswer in Answer Module after retrive: ", classAnswerTemp
    print "\n boundedSlotAnswer in Answer Module after retrive: ", slotAnswerTemp

    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        for hmSlot0,hmSlot1 in Qvar.boundedSlotHowmuch:
            if (slotAnswerTemp[itemSlot0,itemSlot1][0]== slotHmchTemp[hmSlot0,hmSlot1][0]) and (slotAnswerTemp[itemSlot0,itemSlot1][1]== slotHmchTemp[hmSlot0,hmSlot1][1]):
                print "Was found the Slot for rerieve::: ",slotAnswerTemp[itemSlot0,itemSlot1]
                slotArg=slotAnswerTemp[itemSlot0,itemSlot1]
                list_Slot_Howmuch.append(slotArg)
            print "\n boundedSlot in Answer Module: ", Qvar.boundedSlotAnswer
            retrieveDataTypeAnswer(WDirectory,slotAnswerTemp[itemSlot0,itemSlot1][0],slotAnswerTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
    print "\n boundedSlotTypeAnswer: ", Qvar.boundedSlotTypeAnswer
    print "\n list_Slot_Howmuch:",list_Slot_Howmuch
    tempSlottypeAnswer=Qvar.boundedSlotTypeAnswer
    tempClassCmpProp=Qvar.boundedClassCmpProp

    for item0,item1 in Qvar.boundedSlotTypeAnswer:
        for item in Qvar.boundedClassCmpProp:
            if str(tempSlottypeAnswer[item0,item1][1])==str(tempClassCmpProp[item]):
                print "Answer: Was found tempBoundedClassCmpProp:",tempSlottypeAnswer[item0,item1]
                Qvar.addBoundedExactSlotAnswer(tempSlottypeAnswer[item0,item1],tempSlottypeAnswer[item0,item1][0],tempSlottypeAnswer[item0,item1][1],item0,item1)
                intitem=int(removeAlphabetfromIdx(item0))
                retrieveInstanceAnswer(WDirectory,tempSlottypeAnswer[item0,item1][1],intitem)

    print "\n boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer
    tempInstanceCmpProp=Qvar.boundedInstanceCmpProp
    tempInstanceAnswer=Qvar.boundedInstanceAnswer
    i=0
    exAnsw=0
    for item0,item1 in Qvar.boundedInstanceAnswer:
        for itemInst0,itemInst1 in Qvar.boundedInstanceCmpProp:
            if str(tempInstanceAnswer[item0,item1][2])==str(tempInstanceCmpProp[itemInst0,itemInst1][2]):
                print "Exact Answer founded !!!:", tempInstanceAnswer[item0,item1]
                if Qvar.addBoundedExactInstanceAnswer(tempInstanceCmpProp[itemInst0,itemInst1],itemInst0,itemInst1):
                    i=i+1
                exAnsw=1

    print "\n Final Result: boundedExactAnswer in Answer Module: ", Qvar.boundedExactAnswer
    tempExactSlotAnswer=Qvar.boundedExactSlotAnswer
    tempExactInstanceAnswer=Qvar.boundedExactInstanceAnswer

    if exAnsw==1:
        for item in list_Slot_Howmuch:
            for itemSlot0,itemSlot1 in Qvar.boundedExactSlotAnswer:
                for itemInst0,itemInst1 in Qvar.boundedExactInstanceAnswer:
                    print "\n list_Slot_Howmuch :", item[0],item[1]
                    print "\n Qvar.boundedExactSlotAnswer :", tempExactSlotAnswer[itemSlot0,itemSlot1][0], tempExactSlotAnswer[itemSlot0,itemSlot1][1]
                    print "\n Qvar.boundedExactAnswer : ",tempExactInstanceAnswer[itemInst0,itemInst1][0],tempExactInstanceAnswer[itemInst0,itemInst1][1],tempExactInstanceAnswer[itemInst0,itemInst1][2]
                    retrieveExactInstanceAnswer(WDirectory,item[0],item[1],tempExactInstanceAnswer[itemInst0,itemInst1],itemInst0,itemInst1,tempExactSlotAnswer[itemSlot0,itemSlot1],itemSlot0,itemSlot1)


    print "\n","NOTE:    Howmuch_Ont was found in Ontology, Qvar.boundedClassHowmuch,",Qvar.boundedClassHowmuch,"\n"
    print "\n","NOTE:    Howmuch_Ont was found in Ontology, Qvar.boundedSlotHowmuch,",Qvar.boundedSlotHowmuch,"\n"
    print "\n","NOTE:    Howmuch_Ont was found in Ontology, Qvar.boundedInstanceHowmuch,",Qvar.boundedInstanceHowmuch,"\n"
    print "\n","NOTE:    Howmuch_Ont was found in Ontology, Qvar.boundedSlotTypeHowmuch,",Qvar.boundedSlotTypeHowmuch,"\n"
    print "\n","NOTE:    Final answer record is :",Qvar.boundedExactAnswer



def obtainAnswerWhat_CompoundProperties(r,s):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    WDirectory=Qvar.workingDir
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    lstitkW={}
    lstitkWClass={}
    itkW=0
    Flag=0
    list_Cls_What=[]
    list_Slot_What=[]
    list_Inst_What=[]
    boundedTempExactSlotAnswer={}
    boundedValues=sorted(r.boundedVars.values())
    print "\n boundedClassWhat in Answer Module: ", Qvar.boundedClassWhat
    print "\n boundedSlotWhat in Answer Module: ", Qvar.boundedSlotWhat
    answerBoundedClass=Qvar.boundedClassWhat
    for item in answerBoundedClass.keys():
        retrieveSlotsAnswer(WDirectory,answerBoundedClass[item],item[0],item[1])
    classAnswerTemp=Qvar.boundedClassAnswer
    slotAnswerTemp=Qvar.boundedSlotAnswer
    # slotWhatTemp=Qvar.boundedSlotWhat
    print "\n boundedClassAnswer in Answer Module after retrive: ", classAnswerTemp
    print "\n boundedSlotAnswer in Answer Module after retrive: ", slotAnswerTemp
#  -----   This Part dedicated to analyze slot type of a class  -----

    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        retrieveDataTypeAnswer(WDirectory,slotAnswerTemp[itemSlot0,itemSlot1][0],slotAnswerTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
    print "\n boundedSlotTypeAnswer:: ", Qvar.boundedSlotTypeAnswer
    tempSlottypeAnswer=Qvar.boundedSlotTypeAnswer
    tempClassCmpProp=Qvar.boundedClassCmpProp
    for item0,item1 in Qvar.boundedSlotTypeAnswer:
        for item in Qvar.boundedClassCmpProp:
            if str(tempSlottypeAnswer[item0,item1][1])==str(tempClassCmpProp[item]):
                print "Answer Class: Was found tempBoundedClassCmpProp:",tempSlottypeAnswer[item0,item1]
                Qvar.addBoundedExactSlotAnswer(tempSlottypeAnswer[item0,item1],tempSlottypeAnswer[item0,item1][0],tempSlottypeAnswer[item0,item1][1],item0,item1)
                intitem=int(removeAlphabetfromIdx(item0))
                retrieveInstanceAnswer(WDirectory,tempSlottypeAnswer[item0,item1][1],intitem)

    print "\n Step1: boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n Step1: boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer
    print "\n Step1: boundedSlotAnswer in Answer Module: ", Qvar.boundedSlotAnswer
    print "\n Step1: boundedSlotCmpProp in Answer Module: ", Qvar.boundedSlotCmpProp
    print "\n Step1: boundedInstanceCmpProp in Answer Module: ", Qvar.boundedInstanceCmpProp

#   This part is dedicated to analyze Slot of What
    tempSlotCmpProp=Qvar.boundedSlotCmpProp
    tempSlotAnswer=Qvar.boundedSlotAnswer
    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        for slotCmpProp0, slotCmpProp1 in Qvar.boundedSlotCmpProp:
            # print "Checking Answer Slot: tempSlotAnswer[itemSlot0,itemSlot1], tempSlotCmpProp :",tempSlotAnswer[itemSlot0,itemSlot1],tempSlotCmpProp[slotCmpProp0,slotCmpProp1]
            if str(tempSlotAnswer[itemSlot0,itemSlot1][1])==str(tempSlotCmpProp[slotCmpProp0,slotCmpProp1][1]):
                print "Answer Slot: Was found tempSlotAnswer:",tempSlotAnswer[itemSlot0,itemSlot1][1]
                Qvar.addBoundedExactSlotAnswer(tempSlotAnswer[itemSlot0,itemSlot1],tempSlotAnswer[itemSlot0,itemSlot1][0],tempSlotAnswer[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
                intitem=int(removeAlphabetfromIdx(itemSlot0))
                retrieveInstanceAnswer(WDirectory,tempSlotAnswer[itemSlot0,itemSlot1][1],intitem)

    print "\n Step2: boundedSlotWhat in Answer Module: ", Qvar.boundedSlotWhat
    print "\n Step2: boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n Step2: boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer

    tempInstanceCmpProp=Qvar.boundedInstanceCmpProp
    tempInstanceAnswer=Qvar.boundedInstanceAnswer
    i=0
    exAnsw=0
    for item0,item1 in Qvar.boundedInstanceAnswer:
        for itemInst0,itemInst1 in Qvar.boundedInstanceCmpProp:
            if str(tempInstanceAnswer[item0,item1][2])==str(tempInstanceCmpProp[itemInst0,itemInst1][2]):
                print "Exact Answer founded !!!:", tempInstanceAnswer[item0,item1]
                if Qvar.addBoundedExactInstanceAnswer(tempInstanceCmpProp[itemInst0,itemInst1],itemInst0,itemInst1):
                    print "itemInst0,itemInst1:", itemInst0,itemInst1
                    boundedTempExactSlotAnswer[itemInst0,itemInst1]={}
                    boundedTempExactSlotAnswer[itemInst0,itemInst1][0]=tempInstanceCmpProp[itemInst0,itemInst1][0]
                    boundedTempExactSlotAnswer[itemInst0,itemInst1][1]=tempInstanceCmpProp[itemInst0,itemInst1][1]
                    Qvar.addBoundedExactSlotAnswer(boundedTempExactSlotAnswer[itemInst0,itemInst1],boundedTempExactSlotAnswer[itemInst0,itemInst1][0],boundedTempExactSlotAnswer[itemInst0,itemInst1][1],itemInst0,itemInst1)
                    i=i+1
                exAnsw=1

    print "\n Step3: boundedExactSlotAnswer: ", Qvar.boundedExactSlotAnswer
    print "\n Step3: boundedExactInstanceAnswer: ", Qvar.boundedExactInstanceAnswer
    print "\n Step3: boundedSlotWhat: ", Qvar.boundedSlotWhat
    print "\n Step3: boundedInstanceWhat : ", Qvar.boundedInstanceWhat

    tempSlotTypeAnswer=Qvar.boundedSlotTypeAnswer
    slotWhatTemp=Qvar.boundedSlotWhat
    instanceWhatTemp=Qvar.boundedInstanceWhat
    tempExactSlotAnswer=Qvar.boundedExactSlotAnswer
    tempExactInstanceAnswer=Qvar.boundedExactInstanceAnswer
    if exAnsw==1:
        for item in slotWhatTemp.keys():
            for itemSlot0,itemSlot1 in Qvar.boundedExactSlotAnswer:
                for itemInst0,itemInst1 in Qvar.boundedExactInstanceAnswer:
                    for itemInstWhat in Qvar.boundedInstanceWhat:
                        print "\n slotWhatTemp :", slotWhatTemp[item]
                        if str(tempExactInstanceAnswer[itemInst0,itemInst1][2])== str(instanceWhatTemp[itemInstWhat][2]):
                            print "Matched Instance found: What!!! ", instanceWhatTemp[itemInstWhat]
                            print "Matched Instance found: Exact Answer!!! ", tempExactInstanceAnswer[itemInst0,itemInst1]
                            for itemSlotTypeAnswer in Qvar.boundedSlotTypeAnswer:
                                if str(tempExactInstanceAnswer[itemInst0,itemInst1][1])==str(tempSlotTypeAnswer[itemSlotTypeAnswer][0]):
                                    retrieveSlotsItem(WDirectory,tempSlotTypeAnswer[itemSlotTypeAnswer][1],itemInst0,itemInst0)
                                    print "Retrive Slots of the class Type:",Qvar.boundedClassItem, Qvar.boundedSlotItem
                                    print "That is DT instance",tempExactInstanceAnswer[itemInst0,itemInst1],tempSlottypeAnswer[itemSlotTypeAnswer][1]
                                    for itemSlotsType in Qvar.boundedSlotItem:
                                        retrieveExactInstanceAnswer(WDirectory,Qvar.boundedSlotItem[itemSlotsType],itemInst0,tempExactInstanceAnswer[itemInst0,itemInst1][2])
                                else:
                                    Qvar.addBoundedExactAnswer(tempExactInstanceAnswer[itemInst0,itemInst1],itemInst0,itemInst1)
                        elif str(tempExactSlotAnswer[itemSlot0,itemSlot1][0])==str(slotWhatTemp[item][0]) and str(tempExactSlotAnswer[itemSlot0,itemSlot1][1])==str(slotWhatTemp[item][1]):
                            print "\n Qvar.boundedExactSlotAnswer :", tempExactSlotAnswer[itemSlot0,itemSlot1][0], tempExactSlotAnswer[itemSlot0,itemSlot1][1]
                            print "\n Qvar.tempExactInstanceAnswer : ",tempExactInstanceAnswer[itemInst0,itemInst1][0],tempExactInstanceAnswer[itemInst0,itemInst1][1],tempExactInstanceAnswer[itemInst0,itemInst1][2]
                            if str(tempExactSlotAnswer[itemSlot0,itemSlot1][0])==str(tempExactInstanceAnswer[itemInst0,itemInst1][0]) and str(tempExactSlotAnswer[itemSlot0,itemSlot1][1])==str(tempExactInstanceAnswer[itemInst0,itemInst1][1]):
                                print "Last Step: tempExactInstanceAnswer result !!!",str(tempExactInstanceAnswer[itemInst0,itemInst1])
                                print "Last Step: tempExactSlotAnswer result !!!",  tempExactSlotAnswer[itemSlot0,itemSlot1]
                                retrieveExactInstanceAnswer(WDirectory,tempExactSlotAnswer[itemSlot0,itemSlot1],itemInst1,tempExactInstanceAnswer[itemInst0,itemInst1][2])

    print "\n","NOTE:    What_Ont was found in Ontology, Qvar.boundedClassWhat,",Qvar.boundedClassWhat,"\n"
    print "\n","NOTE:    What_Ont was found in Ontology, Qvar.boundedSlotWhat,",Qvar.boundedSlotWhat,"\n"
    print "\n","NOTE:    What_Ont was found in Ontology, Qvar.boundedInstanceWhat,",Qvar.boundedInstanceWhat,"\n"
    print "\n","NOTE:    What_Ont was found in Ontology, Qvar.boundedSlotTypeWhat,",Qvar.boundedSlotTypeWhat,"\n"
    print "\n","NOTE:    Final answer record is :",Qvar.boundedExactAnswer


def obtainAnswerWhere_Person_Action(r,s):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    WDirectory=Qvar.workingDir
    itkW=0
    Flag=0
    boundedTempExactSlotAnswer={}
    boundedValues=sorted(r.boundedVars.values())
    print "\n boundedClassWhere in Answer Module: ", Qvar.boundedClassWhere
    print "\n boundedSlotWhere in Answer Module: ", Qvar.boundedSlotWhere
    answerBoundedClass=Qvar.boundedClassWhere
    for item in answerBoundedClass.keys():
        retrieveSlotsAnswer(WDirectory,answerBoundedClass[item],item[0],item[1])
    classAnswerTemp=Qvar.boundedClassAnswer
    slotAnswerTemp=Qvar.boundedSlotAnswer
    print "\n boundedClassAnswer in Answer Module after retrive: ", classAnswerTemp
    print "\n boundedSlotAnswer in Answer Module after retrive: ", slotAnswerTemp
#  -----   This Part dedicated to analyze slot type of a class  -----
    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        retrieveDataTypeAnswer(WDirectory,slotAnswerTemp[itemSlot0,itemSlot1][0],slotAnswerTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)

    print "\n Step0: boundedSlotTypeAction:: ", Qvar.boundedSlotTypeAction
    print "\n Step0: boundedSlotTypePerson:: ", Qvar.boundedSlotTypePerson
    print "\n Step0: boundedSlotTypeAnswer:: ", Qvar.boundedSlotTypeAnswer
    print "\n Step0: Qvar.boundedClassPerson:: ", Qvar.boundedClassPerson
    print "\n Step0: Qvar.boundedClassAction:: ", Qvar.boundedClassAction

    tempSlottypeAnswer=Qvar.boundedSlotTypeAnswer
    tempSlottypeAction=Qvar.boundedSlotTypeAction
    tempClassPerson=Qvar.boundedClassPerson
    tempClassAction=Qvar.boundedClassAction
    for itemAnswType0,itemAnswType1 in Qvar.boundedSlotTypeAnswer:
        for itemActType0, itemActType1 in Qvar.boundedSlotTypeAction:
            for itemPer in Qvar.boundedClassPerson:
                for itemAction in Qvar.boundedClassAction:
                    if str(tempSlottypeAnswer[itemAnswType0,itemAnswType1][1])==str(tempSlottypeAction[itemActType0, itemActType1][1]) or str(tempSlottypeAnswer[itemAnswType0,itemAnswType1][1])==str(tempClassPerson[itemPer]) or str(tempSlottypeAnswer[itemAnswType0,itemAnswType1][1])==str(tempClassAction[itemAction]):
                        print "Answer Class: Was found tempBoundedClassPerson and Action:",tempSlottypeAnswer[itemAnswType0,itemAnswType1]
                        Qvar.addBoundedExactSlotAnswer(tempSlottypeAnswer[itemAnswType0,itemAnswType1],tempSlottypeAnswer[itemAnswType0,itemAnswType1][0],tempSlottypeAnswer[itemAnswType0,itemAnswType1][1],itemAnswType0,itemAnswType1)
                        intitem=int(removeAlphabetfromIdx(itemAnswType0))
                        retrieveInstanceAnswer(WDirectory,tempSlottypeAnswer[itemAnswType0,itemAnswType1][1],intitem)

    print "\n Step1: boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n Step1: boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer
    print "\n Step1: boundedSlotAnswer in Answer Module: ", Qvar.boundedSlotAnswer
    print "\n Step1: boundedSlotPerson in Answer Module: ", Qvar.boundedSlotPerson
    print "\n Step1: boundedSlotAction in Answer Module: ", Qvar.boundedSlotAction

#   This part is dedicated to analyze Slot of Where
    tempSlotPerson=Qvar.boundedSlotPerson
    tempSlotAction=Qvar.boundedSlotAction
    tempSlotAnswer=Qvar.boundedSlotAnswer
    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        for slotPerson0, slotPerson1 in Qvar.boundedSlotPerson:
            for slotAction0, slotAction1 in Qvar.boundedSlotAction:
                # print "Checking Answer Slot: tempSlotAnswer[itemSlot0,itemSlot1], tempSlotCmpProp :",tempSlotAnswer[itemSlot0,itemSlot1],tempSlotCmpProp[slotCmpProp0,slotCmpProp1]
                if str(tempSlotAnswer[itemSlot0,itemSlot1][1])==str(tempSlotPerson[slotPerson0,slotPerson1][1]) or str(tempSlotAnswer[itemSlot0,itemSlot1][1])==str(tempSlotAction[slotAction0,slotAction1][1]):
                    print "Answer Slot: Was found tempSlotAnswer:",tempSlotAnswer[itemSlot0,itemSlot1][1]
                    Qvar.addBoundedExactSlotAnswer(tempSlotAnswer[itemSlot0,itemSlot1],tempSlotAnswer[itemSlot0,itemSlot1][0],tempSlotAnswer[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
                    intitem=int(removeAlphabetfromIdx(itemSlot0))
                    retrieveInstanceAnswer(WDirectory,tempSlotAnswer[itemSlot0,itemSlot1][1],intitem)

    print "\n Step2: boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n Step2: boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer
    print "\n Step2: boundedInstancePerson in Answer Module: ", Qvar.boundedInstancePerson
    print "\n Step2: boundedInstanceAction : ", Qvar.boundedInstanceAction

    tempInstancePerson=Qvar.boundedInstancePerson
    tempInstanceAction=Qvar.boundedInstanceAction
    tempInstanceAnswer=Qvar.boundedInstanceAnswer
    i=0
    exAnsw=0
    for item0,item1 in Qvar.boundedInstanceAnswer:
        for itemInstPer0,itemInstPer1 in Qvar.boundedInstancePerson:
            for itemInstAct0, itemInstAct1 in Qvar.boundedInstanceAction:
                if str(tempInstanceAnswer[item0,item1][2])==str(tempInstancePerson[itemInstPer0,itemInstPer1][2]) or str(tempInstanceAnswer[item0,item1][2])==str(tempInstanceAction[itemInstAct0,itemInstAct1][2]):
                    # print "Exact Answer tempInstanceAnswer founded !!!:", tempInstanceAnswer[item0,item1]
                    # print "Exact Answer tempInstancePerson founded !!!:", tempInstancePerson[itemInstPer0,itemInstPer1]
                    # print "Exact Answer tempInstanceAction founded !!!:", tempInstanceAction[itemInstAct0,itemInstAct1]
                    if Qvar.addBoundedExactInstanceAnswer(tempInstanceAnswer[item0,item1],item0,item1):
                        print "addBoundedExactInstanceAnswer:", item0,item1
                        boundedTempExactSlotAnswer[item0,item1]={}
                        boundedTempExactSlotAnswer[item0,item1][0]=tempInstanceAnswer[item0,item1][0]
                        boundedTempExactSlotAnswer[item0,item1][1]=tempInstanceAnswer[item0,item1][1]
                        Qvar.addBoundedExactSlotAnswer(boundedTempExactSlotAnswer[item0,item1],boundedTempExactSlotAnswer[item0,item1][0],boundedTempExactSlotAnswer[item0,item1][1],item0,item1)
                        i=i+1
                    exAnsw=1

    print "\n Step3: boundedExactSlotAnswer: ", Qvar.boundedExactSlotAnswer
    print "\n Step3: boundedExactInstanceAnswer: ", Qvar.boundedExactInstanceAnswer
    print "\n Step3: boundedSlotWhere: ", Qvar.boundedSlotWhere
    print "\n Step3: boundedInstanceWhere : ", Qvar.boundedInstanceWhere

    tempSlotTypeAnswer=Qvar.boundedSlotTypeAnswer
    slotWhereTemp=Qvar.boundedSlotWhere
    instanceWhereTemp=Qvar.boundedInstanceWhere
    tempExactSlotAnswer=Qvar.boundedExactSlotAnswer
    tempExactInstanceAnswer=Qvar.boundedExactInstanceAnswer
    if exAnsw==1:
        for item in slotWhereTemp.keys():
            for itemSlot0,itemSlot1 in Qvar.boundedExactSlotAnswer:
                for itemInst0,itemInst1 in Qvar.boundedExactInstanceAnswer:
                    for itemInstWhere in Qvar.boundedInstanceWhere:
                        if str(tempExactInstanceAnswer[itemInst0,itemInst1][2])== str(instanceWhereTemp[itemInstWhere][2]):
                            print "Matched Instance found: Where!!! ", instanceWhereTemp[itemInstWhere]
                            print "Matched Instance found: Exact Answer!!! ", tempExactInstanceAnswer[itemInst0,itemInst1]
                            for itemSlotTypeAnswer in Qvar.boundedSlotTypeAnswer:
                                if str(tempExactInstanceAnswer[itemInst0,itemInst1][1])==str(tempSlotTypeAnswer[itemSlotTypeAnswer][0]):
                                    retrieveSlotsItem(WDirectory,tempSlotTypeAnswer[itemSlotTypeAnswer][1],itemInst0,itemInst0)
                                    print "Retrive Slots of the class Type:",Qvar.boundedClassItem, Qvar.boundedSlotItem
                                    print "That is DT instance",tempExactInstanceAnswer[itemInst0,itemInst1],tempSlottypeAnswer[itemSlotTypeAnswer][1]
                                    for itemSlotsType in Qvar.boundedSlotItem:
                                        retrieveExactInstanceAnswer(WDirectory,Qvar.boundedSlotItem[itemSlotsType],itemInst0,tempExactInstanceAnswer[itemInst0,itemInst1][2])
                                else:
                                    Qvar.addBoundedExactAnswer(tempExactInstanceAnswer[itemInst0,itemInst1],itemInst0,itemInst1)
                        elif str(tempExactSlotAnswer[itemSlot0,itemSlot1][0])==str(slotWhereTemp[item][0]) and str(tempExactSlotAnswer[itemSlot0,itemSlot1][1])==str(slotWhereTemp[item][1]):
                            print "\n Qvar.boundedExactSlotAnswer :", tempExactSlotAnswer[itemSlot0,itemSlot1][0], tempExactSlotAnswer[itemSlot0,itemSlot1][1]
                            print "\n Qvar.tempExactInstanceAnswer : ",tempExactInstanceAnswer[itemInst0,itemInst1][0],tempExactInstanceAnswer[itemInst0,itemInst1][1],tempExactInstanceAnswer[itemInst0,itemInst1][2]
                            if str(tempExactSlotAnswer[itemSlot0,itemSlot1][0])==str(tempExactInstanceAnswer[itemInst0,itemInst1][0]) and str(tempExactSlotAnswer[itemSlot0,itemSlot1][1])==str(tempExactInstanceAnswer[itemInst0,itemInst1][1]):
                                print "Last Step: tempExactInstanceAnswer result !!!",str(tempExactInstanceAnswer[itemInst0,itemInst1])
                                print "Last Step: tempExactSlotAnswer result !!!",  tempExactSlotAnswer[itemSlot0,itemSlot1]
                                retrieveExactInstanceAnswer(WDirectory,tempExactSlotAnswer[itemSlot0,itemSlot1],itemInst1,tempExactInstanceAnswer[itemInst0,itemInst1][2])

    print "\n","NOTE:    Where_Ont was found in Ontology, Qvar.boundedClassWhere,",Qvar.boundedClassWhere,"\n"
    print "\n","NOTE:    Where_Ont was found in Ontology, Qvar.boundedSlotWhere,",Qvar.boundedSlotWhere,"\n"
    print "\n","NOTE:    Where_Ont was found in Ontology, Qvar.boundedInstanceWhere,",Qvar.boundedInstanceWhere,"\n"
    print "\n","NOTE:    Where_Ont was found in Ontology, Qvar.boundedSlotTypeWhere,",Qvar.boundedSlotTypeWhere,"\n"
    print "\n","NOTE:    Final answer record is :",Qvar.boundedExactAnswer

def obtainAnswerWho_Properties_Person(r,s):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    WDirectory=Qvar.workingDir
    itkW=0
    Flag=0
    boundedTempExactSlotAnswer={}
    boundedValues=sorted(r.boundedVars.values())
    print "\n boundedClassWho in Answer Module: ", Qvar.boundedClassWho
    print "\n boundedSlotWho in Answer Module: ", Qvar.boundedSlotWho
    answerBoundedClass=Qvar.boundedClassWho
    for item in answerBoundedClass.keys():
        retrieveSlotsAnswer(WDirectory,answerBoundedClass[item],item[0],item[1])
    classAnswerTemp=Qvar.boundedClassAnswer
    slotAnswerTemp=Qvar.boundedSlotAnswer
    print "\n boundedClassAnswer in Answer Module after retrive: ", classAnswerTemp
    print "\n boundedSlotAnswer in Answer Module after retrive: ", slotAnswerTemp
#  -----   This Part dedicated to analyze slot type of a class  -----
    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        retrieveDataTypeAnswer(WDirectory,slotAnswerTemp[itemSlot0,itemSlot1][0],slotAnswerTemp[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)

    print "\n Step0: boundedSlotTypeProp:: ", Qvar.boundedSlotTypeProp
    print "\n Step0: boundedSlotTypePerson:: ", Qvar.boundedSlotTypePerson
    print "\n Step0: boundedSlotTypeAnswer:: ", Qvar.boundedSlotTypeAnswer
    print "\n Step0: Qvar.boundedClassPerson:: ", Qvar.boundedClassPerson
    print "\n Step0: Qvar.boundedClassProp:: ", Qvar.boundedClassProp

    tempSlottypeAnswer=Qvar.boundedSlotTypeAnswer
    tempSlottypePerson=Qvar.boundedSlotTypePerson
    tempClassPerson=Qvar.boundedClassPerson
    tempClassProp=Qvar.boundedClassProp
    for itemAnswType0,itemAnswType1 in Qvar.boundedSlotTypeAnswer:
        for itemPerType0, itemPerType1 in Qvar.boundedSlotTypePerson:
            for itemProp in Qvar.boundedClassProp:
                for itemPerson in Qvar.boundedClassPerson:
                    if str(tempSlottypeAnswer[itemAnswType0,itemAnswType1][1])==str(tempSlottypePerson[itemPerType0, itemPerType1][1]) or str(tempSlottypeAnswer[itemAnswType0,itemAnswType1][1])==str(tempClassPerson[itemPer]) or str(tempSlottypeAnswer[itemAnswType0,itemAnswType1][1])==str(tempClassPerson[itemPerson]):
                        print "Answer Class: Was found tempBoundedClassPerson and Prop:",tempSlottypeAnswer[itemAnswType0,itemAnswType1]
                        Qvar.addBoundedExactSlotAnswer(tempSlottypeAnswer[itemAnswType0,itemAnswType1],tempSlottypeAnswer[itemAnswType0,itemAnswType1][0],tempSlottypeAnswer[itemAnswType0,itemAnswType1][1],itemAnswType0,itemAnswType1)
                        intitem=int(removeAlphabetfromIdx(itemAnswType0))
                        retrieveInstanceAnswer(WDirectory,tempSlottypeAnswer[itemAnswType0,itemAnswType1][1],intitem)

    print "\n Step1: boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n Step1: boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer
    print "\n Step1: boundedSlotAnswer in Answer Module: ", Qvar.boundedSlotAnswer
    print "\n Step1: boundedSlotPerson in Answer Module: ", Qvar.boundedSlotPerson
    print "\n Step1: boundedSlotProp in Answer Module: ", Qvar.boundedSlotProp

#   This part is dedicated to analyze Slot of Who
    tempSlotPerson=Qvar.boundedSlotPerson
    tempSlotProp=Qvar.boundedSlotProp
    tempSlotAnswer=Qvar.boundedSlotAnswer
    for itemSlot0,itemSlot1 in Qvar.boundedSlotAnswer:
        for slotPerson0, slotPerson1 in Qvar.boundedSlotPerson:
            for slotProp0, slotProp1 in Qvar.boundedSlotProp:
                # print "Checking Answer Slot: tempSlotAnswer[itemSlot0,itemSlot1], tempSlotCmpProp :",tempSlotAnswer[itemSlot0,itemSlot1],tempSlotCmpProp[slotCmpProp0,slotCmpProp1]
                if str(tempSlotAnswer[itemSlot0,itemSlot1][1])==str(tempSlotPerson[slotPerson0,slotPerson1][1]) or str(tempSlotAnswer[itemSlot0,itemSlot1][1])==str(tempSlotProp[slotProp0,slotProp1][1]):
                    print "Answer Slot: Was found tempSlotAnswer:",tempSlotAnswer[itemSlot0,itemSlot1][1]
                    Qvar.addBoundedExactSlotAnswer(tempSlotAnswer[itemSlot0,itemSlot1],tempSlotAnswer[itemSlot0,itemSlot1][0],tempSlotAnswer[itemSlot0,itemSlot1][1],itemSlot0,itemSlot1)
                    intitem=int(removeAlphabetfromIdx(itemSlot0))
                    retrieveInstanceAnswer(WDirectory,tempSlotAnswer[itemSlot0,itemSlot1][1],intitem)

    print "\n Step2: boundedExactSlotAnswer in Buffer: ", Qvar.boundedExactSlotAnswer
    print "\n Step2: boundedInstanceAnswer in Answer Module: ", Qvar.boundedInstanceAnswer
    print "\n Step2: boundedInstancePerson in Answer Module: ", Qvar.boundedInstancePerson
    print "\n Step2: boundedInstanceProp : ", Qvar.boundedInstanceProp

    tempInstancePerson=Qvar.boundedInstancePerson
    tempInstanceProp=Qvar.boundedInstanceProp
    tempInstanceAnswer=Qvar.boundedInstanceAnswer
    i=0
    exAnsw=0
    for item0,item1 in Qvar.boundedInstanceAnswer:
        for itemInstPer0,itemInstPer1 in Qvar.boundedInstancePerson:
            for itemInstProp0, itemInstProp1 in Qvar.boundedInstanceProp:
                if str(tempInstanceAnswer[item0,item1][2])==str(tempInstancePerson[itemInstPer0,itemInstPer1][2]) or str(tempInstanceAnswer[item0,item1][2])==str(tempInstanceProp[itemInstProp0,itemInstProp1][2]):
                    # print "Exact Answer tempInstanceAnswer founded !!!:", tempInstanceAnswer[item0,item1]
                    # print "Exact Answer tempInstancePerson founded !!!:", tempInstancePerson[itemInstPer0,itemInstPer1]
                    # print "Exact Answer tempInstanceAction founded !!!:", tempInstanceAction[itemInstAct0,itemInstAct1]
                    if Qvar.addBoundedExactInstanceAnswer(tempInstanceAnswer[item0,item1],item0,item1):
                        print "addBoundedExactInstanceAnswer:", item0,item1
                        boundedTempExactSlotAnswer[item0,item1]={}
                        boundedTempExactSlotAnswer[item0,item1][0]=tempInstanceAnswer[item0,item1][0]
                        boundedTempExactSlotAnswer[item0,item1][1]=tempInstanceAnswer[item0,item1][1]
                        Qvar.addBoundedExactSlotAnswer(boundedTempExactSlotAnswer[item0,item1],boundedTempExactSlotAnswer[item0,item1][0],boundedTempExactSlotAnswer[item0,item1][1],item0,item1)
                        i=i+1
                    exAnsw=1

    print "\n Step3: boundedExactSlotAnswer: ", Qvar.boundedExactSlotAnswer
    print "\n Step3: boundedExactInstanceAnswer: ", Qvar.boundedExactInstanceAnswer
    print "\n Step3: boundedSlotWho: ", Qvar.boundedSlotWho
    print "\n Step3: boundedInstanceWho : ", Qvar.boundedInstanceWho

    tempSlotTypeAnswer=Qvar.boundedSlotTypeAnswer
    slotWhoTemp=Qvar.boundedSlotWho
    instanceWhoTemp=Qvar.boundedInstanceWho
    tempExactSlotAnswer=Qvar.boundedExactSlotAnswer
    tempExactInstanceAnswer=Qvar.boundedExactInstanceAnswer
    if exAnsw==1:
        for item in slotWhoTemp.keys():
            for itemSlot0,itemSlot1 in Qvar.boundedExactSlotAnswer:
                for itemInst0,itemInst1 in Qvar.boundedExactInstanceAnswer:
                    for itemInstWho in Qvar.boundedInstanceWho:
                        if str(tempExactInstanceAnswer[itemInst0,itemInst1][2])== str(instanceWhoTemp[itemInstWho][2]):
                            print "Matched Instance found: Who!!! ", instanceWhoTemp[itemInstWho]
                            print "Matched Instance found: Exact Answer!!! ", tempExactInstanceAnswer[itemInst0,itemInst1]
                            for itemSlotTypeAnswer in Qvar.boundedSlotTypeAnswer:
                                if str(tempExactInstanceAnswer[itemInst0,itemInst1][1])==str(tempSlotTypeAnswer[itemSlotTypeAnswer][0]):
                                    retrieveSlotsItem(WDirectory,tempSlotTypeAnswer[itemSlotTypeAnswer][1],itemInst0,itemInst0)
                                    print "Retrive Slots of the class Type:",Qvar.boundedClassItem, Qvar.boundedSlotItem
                                    print "That is DT instance",tempExactInstanceAnswer[itemInst0,itemInst1],tempSlottypeAnswer[itemSlotTypeAnswer][1]
                                    for itemSlotsType in Qvar.boundedSlotItem:
                                        retrieveExactInstanceAnswer(WDirectory,Qvar.boundedSlotItem[itemSlotsType],itemInst0,tempExactInstanceAnswer[itemInst0,itemInst1][2])
                                else:
                                    Qvar.addBoundedExactAnswer(tempExactInstanceAnswer[itemInst0,itemInst1],itemInst0,itemInst1)
                        elif str(tempExactSlotAnswer[itemSlot0,itemSlot1][0])==str(slotWhoTemp[item][0]) and str(tempExactSlotAnswer[itemSlot0,itemSlot1][1])==str(slotWhoTemp[item][1]):
                            print "\n Qvar.boundedExactSlotAnswer :", tempExactSlotAnswer[itemSlot0,itemSlot1][0], tempExactSlotAnswer[itemSlot0,itemSlot1][1]
                            print "\n Qvar.tempExactInstanceAnswer : ",tempExactInstanceAnswer[itemInst0,itemInst1][0],tempExactInstanceAnswer[itemInst0,itemInst1][1],tempExactInstanceAnswer[itemInst0,itemInst1][2]
                            if str(tempExactSlotAnswer[itemSlot0,itemSlot1][0])==str(tempExactInstanceAnswer[itemInst0,itemInst1][0]) and str(tempExactSlotAnswer[itemSlot0,itemSlot1][1])==str(tempExactInstanceAnswer[itemInst0,itemInst1][1]):
                                print "Last Step: tempExactInstanceAnswer result !!!",str(tempExactInstanceAnswer[itemInst0,itemInst1])
                                print "Last Step: tempExactSlotAnswer result !!!",  tempExactSlotAnswer[itemSlot0,itemSlot1]
                                retrieveExactInstanceAnswer(WDirectory,tempExactSlotAnswer[itemSlot0,itemSlot1],itemInst1,tempExactInstanceAnswer[itemInst0,itemInst1][2])

    print "\n","NOTE:    Who_Ont was found in Ontology, Qvar.boundedClassWho,",Qvar.boundedClassWho,"\n"
    print "\n","NOTE:    Who_Ont was found in Ontology, Qvar.boundedSlotWho,",Qvar.boundedSlotWho,"\n"
    print "\n","NOTE:    Who_Ont was found in Ontology, Qvar.boundedInstanceWho,",Qvar.boundedInstanceWho,"\n"
    print "\n","NOTE:    Who_Ont was found in Ontology, Qvar.boundedSlotTypeWho,",Qvar.boundedSlotTypeWho,"\n"
    print "\n","NOTE:    Final answer record is :",Qvar.boundedExactAnswer
