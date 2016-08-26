__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        Constraints.py
#
# Author:      Majid
#
# Created:     2014/06/06
# Bounded vars added by Constraints.py for QAS
#-----------------------------------------------------------------------------


def obtainConstraintsWhere_Person_Action(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    flagList={}
    i=1
    while i<4 :
        flagList[i]=0
        i=i+1

    boundedValues=sorted(r.boundedVars.values())
    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values and flagList[1]!=1:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_WhereVar=s._constraints._vars[-1]._var
                flagList[1]=1
            elif BVars=="tk_PER" and r.boundedVars['tk_PER']==values and flagList[2]!=1:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
                flagList[2]=1
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values and flagList[3]!=1:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
                flagList[3]=1

    VArg=s._constraints.getVars()

    for vars in VArg:
        list_Dep.append(addDepList(s,vars._argument))

    i=0
    for lst_dep in range(len(list_Dep)):
        sublist.append(sintDp4Tk(r,s,list_Dep[i]))
        i=i+1

    i=0
    for sublst in sublist:
        j=0
        for subls in range(len(sublst)):
            sub_Temp=addDepList(s,sublst[j])
            if len(sub_Temp)!=0:
                lst_subDep.append(sub_Temp)
                if len(lst_subDep[i])!=0:
                    sintDp4Tk(r,s,lst_subDep[i])
                    i=i+1
            j=j+1

    VArg=s._constraints.getVars()
    k=0
    for BVars in r.boundedClassPerson:
        # print "BVars,endPER_Cls,startPER_Cls ",BVars
        s._constraints.addNewVariable(r.boundedClassPerson[BVars])
        s._constraints.addNewConstraint("class_PER_" + str(k),[r.boundedClassPerson[BVars],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_PER_"+ str(k),[ont_PerVar,s._constraints._vars[-1]._var],[ont_PerVar,s._constraints._vars[-1]._var])
        k=k+1

    k=0
    for BVars0,BVars1 in r.boundedSlotPerson:
        VArg=s._constraints.getVars()
        tempSlotPerson0=r.boundedSlotPerson[BVars0,BVars1][0]
        tempSlotPerson1=r.boundedSlotPerson[BVars0,BVars1][1]
        # print "BVars0, BVars1, r.boundedSlotPerson,r.boundedSlotPerson[BVars0,BVars1][0] ",BVars0,BVars1,r.boundedSlotPerson, r.boundedSlotPerson[BVars0,BVars1][0],r.boundedSlotPerson[BVars0,BVars1][1]
        # print "tempSlotPerson0,tempSlotPerson1",tempSlotPerson0,tempSlotPerson1
        chkArg=lookInExistVars(tempSlotPerson0,tempSlotPerson1,VArg)
        AddConstOnt_Slot_PerWith_2_Arg(s,tempSlotPerson0,tempSlotPerson1,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedSlotTypePerson:
        VArg=s._constraints.getVars()
        tempInstPerson0=r.boundedSlotTypePerson[BVars][0]
        tempInstPerson1=r.boundedSlotTypePerson[BVars][1]
        tempInstPerson2=r.boundedSlotTypePerson[BVars][2]
        # print "BVars, r.boundedSlotTypePerson,r.boundedSlotTypePerson[BVars0,BVars1][0] ",BVars,r.boundedSlotTypePerson, r.boundedSlotTypePerson[BVars][0],r.boundedSlotTypePerson[BVars][1]
        # print "tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars0,BVars1][1]",tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars][2]
        chkArg=lookInExistVars(tempInstPerson0,tempInstPerson1,VArg)
        AddConstOnt_Slot_PerWith_2_Arg(s,tempInstPerson1,tempInstPerson2,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedInstancePerson:
        VArg=s._constraints.getVars()
        tempClsPerson0=r.boundedInstancePerson[BVars][0]
        tempSlotPerson1=r.boundedInstancePerson[BVars][1]
        tempInstPerson2=r.boundedInstancePerson[BVars][2]
        # print "BVars r.boundedInstancePerson,r.boundedInstancePerson[BVars0,BVars1][0] ",BVars,r.boundedInstancePerson, r.boundedInstancePerson[BVars][0],r.boundedInstancePerson[BVars][1],r.boundedInstancePerson[BVars][2]
        # print "tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars0,BVars1][1]",tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars][2]
        chkArg=lookInExistVars(tempSlotPerson1,tempInstPerson2,VArg)
        AddConstOnt_Inst_PerWith_2_Arg(s,ont_PerVar,tempClsPerson0,tempSlotPerson1,tempInstPerson2,chkArg,k)
        k=k+1



    k=0
    for BVars in r.boundedClassAction:
        print "BVars,endACT_Cls,startACT_Cls ",BVars
        s._constraints.addNewVariable(r.boundedClassAction[BVars])
        s._constraints.addNewConstraint("class_ACT_" + str(k),[r.boundedClassAction[BVars],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_ACT_"+ str(k),[ont_ActVar,s._constraints._vars[-1]._var],[ont_ActVar,s._constraints._vars[-1]._var])
        k=k+1

    k=0
    for BVars0,BVars1 in r.boundedSlotAction:
        VArg=s._constraints.getVars()
        tempSlotAction0=r.boundedSlotAction[BVars0,BVars1][0]
        tempSlotAction1=r.boundedSlotAction[BVars0,BVars1][1]
        # print "BVars0, BVars1, r.boundedSlotPerson,r.boundedSlotPerson[BVars0,BVars1][0] ",BVars0,BVars1,r.boundedSlotPerson, r.boundedSlotPerson[BVars0,BVars1][0],r.boundedSlotPerson[BVars0,BVars1][1]
        chkArg=lookInExistVars(tempSlotAction0,tempSlotAction1,VArg)
        AddConstOnt_Slot_ActWith_2_Arg(s,tempSlotAction0,tempSlotAction1,chkArg,k)
        k=k+1

    print "boundedSlotTypeAction checking..: ", r.boundedSlotTypeAction
    k=0
    for BVars in r.boundedSlotTypeAction:
        VArg=s._constraints.getVars()
        tempInstAction0=r.boundedSlotTypeAction[BVars][0]
        tempInstAction1=r.boundedSlotTypeAction[BVars][1]
        # tempInstAction2=r.boundedSlotTypeAction[BVars][2]
        # print "BVars, r.boundedSlotTypePerson,r.boundedSlotTypePerson[BVars0,BVars1][0] ",BVars,r.boundedSlotTypePerson, r.boundedSlotTypePerson[BVars][0],r.boundedSlotTypePerson[BVars][1]
        # print "tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars0,BVars1][1]",tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars][2]
        chkArg=lookInExistVars(tempInstAction0,tempInstAction1,VArg)
        AddConstOnt_Slot_ActWith_2_Arg(s,tempInstAction0,tempInstAction1,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedInstanceAction:
        VArg=s._constraints.getVars()
        tempClsAction0=r.boundedInstanceAction[BVars][0]
        tempSlotAction1=r.boundedInstanceAction[BVars][1]
        tempInstAction2=r.boundedInstanceAction[BVars][2]
        # print "BVars r.boundedInstancePerson,r.boundedInstancePerson[BVars0,BVars1][0] ",BVars,r.boundedInstancePerson, r.boundedInstancePerson[BVars][0],r.boundedInstancePerson[BVars][1],r.boundedInstancePerson[BVars][2]
        chkArg=lookInExistVars(tempSlotAction1,tempInstAction2,VArg)
        AddConstOnt_Inst_ActWith_2_Arg(s,ont_PerVar,tempClsAction0,tempSlotAction1,tempInstAction2,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedClassWhere:
        tempClassWhere=r.boundedClassWhere[BVars]
        s._constraints.addNewVariable(tempClassWhere)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempClassWhere,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_Where_"+ str(k),[ont_WhereVar,s._constraints._vars[-1]._var],[ont_WhereVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSlotTypeWhere:
        tempSlotTypeWhere0=r.boundedSlotTypeWhere[BVars][0]
        tempSlotTypeWhere1=r.boundedSlotTypeWhere[BVars][1]
        # print "Where_in Class,",tempSlotTypeWhere1
        s._constraints.addNewVariable(tempSlotTypeWhere1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSlotTypeWhere1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_Where_"+ str(k),[ont_WhereVar,s._constraints._vars[-1]._var],[ont_WhereVar,s._constraints._vars[-1]._var])
        k=k+1


    for BVars in r.boundedSubClassWhere:
        VArg=s._constraints.getVars()
        tempSubClassSlotTypeWhere0=r.boundedSubClassWhere[BVars][0]
        tempSubClassSlotTypeWhere1=r.boundedSubClassWhere[BVars][1]
        # print "BVars, r.Qvar.boundedSubClassWhere_in,r.Qvar.boundedSubClassWhere_in[BVars][0] ",BVars,r.boundedSubClassWhere_in, r.boundedSubClassWhere_in[BVars][0],r.boundedSubClassWhere_in[BVars][1]
        s._constraints.addNewVariable(tempSubClassSlotTypeWhere1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSubClassSlotTypeWhere1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        chkArg=lookInExistVars(tempSubClassSlotTypeWhere0,tempSubClassSlotTypeWhere1,VArg)
        if chkArg[0]!=-1 and chkArg[1]!=-1:
            # print "boundedSubClassWhere_in in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
            s._constraints.addNewConstraint("ont_Subclass_"+ str(k),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
        else:
            print "NOT boundedSubClassWhere_in in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]

        k=k+1

    i=0
    for BVars in r.boundedInstanceWhere:
        VArg=s._constraints.getVars()
        tempClsWhere0=r.boundedInstanceWhere[BVars][0]
        tempSlotWhere1=r.boundedInstanceWhere[BVars][1]
        # print "BVars, r.boundedInstanceWhere_in[0],r.boundedInstanceWhere_in[1] ",BVars,r.boundedInstanceWhere_in[BVars][0],r.boundedInstanceWhere_in[BVars][1]
        chkArg=lookInExistVars(tempClsWhere0,tempSlotWhere1,VArg)
        AddConstOnt_Slot_EATWith_2_Arg(s,tempClsWhere0,tempSlotWhere1,chkArg,i)
        i=i+1

    i=0
    for BVars in r.boundedInstanceWhere:
        VArg=s._constraints.getVars()
        tempClsWhere0=r.boundedInstanceWhere[BVars][0]
        tempSlotWhere1=r.boundedInstanceWhere[BVars][1]
        tempInsWhere2=r.boundedInstanceWhere[BVars][2]
        # print "BVars, r.boundedInstanceWhere[1],r.boundedInstanceWhere_in[2] ",BVars,r.boundedInstanceWhere_in[BVars][1],r.boundedInstanceWhere_in[BVars][2]
        chkArg=lookInExistVars(tempSlotWhere1,tempInsWhere2,VArg)
        AddConstOnt_Inst_EATWith_2_Arg(s,ont_WhereVar,tempClsWhere0,tempSlotWhere1,tempInsWhere2,chkArg,i)
        i=i+1


    i=0
    for BVars in r.boundedExactAnswer:
        VArg=s._constraints.getVars()
        tempClsAnswer0=r.boundedExactAnswer[BVars][0]
        tempSlotAnswer1=r.boundedExactAnswer[BVars][1]
        tempInsAnswer2=r.boundedExactAnswer[BVars][2]
        tempInsLblAnswer3=r.boundedExactAnswer[BVars][3]
        chkArg=lookInExistVars(tempSlotAnswer1,tempInsLblAnswer3,VArg)
        AddConstOnt_Inst_AnswerWith_2_Arg(s,"",tempClsAnswer0,tempSlotAnswer1,tempInsAnswer2,tempInsLblAnswer3,chkArg,i)
        i=i+1


def AddConstOnt_Slot_EATWith_2_Arg(s,ont_Cls1,ont_Slot1,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Slot EAT chkArg[0]!=-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_Slot1)
        s._constraints.addNewConstraint("EAT_slot_" + str(idx),[ont_Slot1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Slot_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Slot EAT chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        print "Slot EAT chkArg[0]==-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_Cls1)
        s._constraints.addNewConstraint("EAT_class_" + str(idx),[ont_Cls1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        x1=s._constraints._vars[-1]._var

        s._constraints.addNewVariable(ont_Slot1)
        s._constraints.addNewConstraint("EAT_slot_" + str(idx),[ont_Slot1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Slot_"+ str(idx),[x1,s._constraints._vars[-1]._var],[x1,s._constraints._vars[-1]._var])

        # s._constraints.addNewConstraint("Class"+ str(idx),[ont_WrVar,s._constraints._vars[-1]._var],[x1,s._constraints._vars[-1]._var])
        # s._constraints.addNewConstraint("ont_Who_"+ str(k),[ont_WhoVar,s._constraints._vars[-1]._var],[ont_WhoVar,s._constraints._vars[-1]._var])


def AddConstOnt_Inst_AnswerWith_2_Arg(s,ont_WrVar,ont_Cls,ont_Slot,ont_Inst,ont_InstLbl,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Inst Answer chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
        s._constraints.addNewConstraint("Answer_" + str(idx),[chkArg[1],chkArg[0]],[chkArg[1],chkArg[0]])
        # s._constraints.addNewConstraint("Answer_Inst"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
    elif chkArg[0]!=-1 and chkArg[1]==-1:
        print "Inst Answer chkArg[0]!=-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_Inst)
        s._constraints.addNewConstraint("Answer_" + str(idx),[ont_Inst,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Answer_Inst"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        print "Inst Answer chkArg[0]==-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_Inst)
        s._constraints.addNewConstraint("Answer_" + str(idx),[ont_Inst,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewConstraint("EAT_class_" + str(idx),[ont_WrVar,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewVariable(ont_Cls)
        #
        # s._constraints.addNewConstraint("ont_EAT_"+ str(idx),[ont_Cls,s._constraints._vars[-1]._var],[ont_Cls,s._constraints._vars[-1]._var])



def AddConstWith_1_ArgFirst(s,list_Dep,chkArg,subListG):

    if chkArg[0]!=-1 and chkArg[1]!=-1:
        s._constraints.addNewConstraint(list_Dep[2],[chkArg[0]],[chkArg[0],chkArg[1]])
    elif chkArg[0]!=-1 and chkArg[1]==-1:
        s._constraints.addNewConstraint(list_Dep[2],[chkArg[0]],[chkArg[0]])
    elif chkArg[0]==-1 and chkArg[1]!=-1:
        s._constraints.addNewVariable(list_Dep[0])
        s._constraints.addNewConstraint('tk',[list_Dep[0],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        subListG.append(list_Dep[0])
        s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var],[s._constraints._vars[-1]._var,chkArg[1]])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        s._constraints.addNewVariable(list_Dep[0])
        subListG.append(list_Dep[0])
        s._constraints.addNewConstraint('tk',[list_Dep[0],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewVariable(list_Dep[1])
        subListG.append(list_Dep[1])
        s._constraints.addNewConstraint('tk',[list_Dep[1],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)



def AddConstWith_1_ArgSecond(s,list_Dep,chkArg,subListG):

    if chkArg[0]!=-1 and chkArg[1]!=-1:
        s._constraints.addNewConstraint(list_Dep[2],[chkArg[1]],[chkArg[1]])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        s._constraints.addNewVariable(list_Dep[1])
        subListG.append(list_Dep[1])
        s._constraints.addNewConstraint('tk',[list_Dep[1],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewVariable(list_Dep[0])
        subListG.append(list_Dep[0])
        s._constraints.addNewConstraint('tk',[list_Dep[0],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
