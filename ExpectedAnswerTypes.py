__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        ExpectedAnswerTypes.py
#
# Author:      Majid
#
# Created:     2015/01/29
# Functions to Find Answer Type for QAS




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

