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


   i=0
 
 d

def obtainConstraintsWhat_Synonym(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_Synonym",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Syn" and r.boundedVars['tk_Syn']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Syn'])
                s._constraints.addNewConstraint('tk_Syn',[r.boundedVars['tk_Syn'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Quant" and r.boundedVars['tk_Quant']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Quant'])
                s._constraints.addNewConstraint('tk_Quant',[r.boundedVars['tk_Quant'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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



def obtainConstraintsWho_Synonym(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Synonym",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Syn" and r.boundedVars['tk_Syn']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Syn'])
                s._constraints.addNewConstraint('tk_Syn',[r.boundedVars['tk_Syn'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Quant" and r.boundedVars['tk_Quant']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Quant'])
                s._constraints.addNewConstraint('tk_Quant',[r.boundedVars['tk_Quant'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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


def obtainConstraintsWhat_CompoundProperties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    flagList={}
    i=1
    while i<3 :
        flagList[i]=0
        i=i+1

    boundedValues=sorted(r.boundedVars.values())
    print "Bounded vars for obtainConstraintsWhat_CompoundProperties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values and flagList[1]!=1:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_WhatVar=s._constraints._vars[-1]._var
                flagList[1]=1

            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values and flagList[2]!=1:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_CmpPropVar=s._constraints._vars[-1]._var
                flagList[2]=1

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
    for BVars in r.boundedClassCmpProp:
        print "BVars,r.boundedClassCmpProp[BVars]: ",BVars, r.boundedClassCmpProp[BVars]
        s._constraints.addNewVariable(r.boundedClassCmpProp[BVars])
        s._constraints.addNewConstraint("class_CmpProp_" + str(k),[r.boundedClassCmpProp[BVars],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_CmpProp_"+ str(k),[ont_CmpPropVar,s._constraints._vars[-1]._var],[ont_CmpPropVar,s._constraints._vars[-1]._var])
        k=k+1

    k=0
    for BVars0,BVars1 in r.boundedSlotCmpProp:
        VArg=s._constraints.getVars()
        tempSlotCmpProp0=r.boundedSlotCmpProp[BVars0,BVars1][0]
        tempSlotCmpProp1=r.boundedSlotCmpProp[BVars0,BVars1][1]
        # print "BVars0, BVars1, r.boundedSlotPerson,r.boundedSlotPerson[BVars0,BVars1][0] ",BVars0,BVars1,r.boundedSlotPerson, r.boundedSlotPerson[BVars0,BVars1][0],r.boundedSlotPerson[BVars0,BVars1][1]
        # print "tempSlotPerson0,tempSlotPerson1",tempSlotPerson0,tempSlotPerson1
        chkArg=lookInExistVars(tempSlotCmpProp0,tempSlotCmpProp1,VArg)
        AddConstOnt_Slot_CmpPropWith_2_Arg(s,tempSlotCmpProp0,tempSlotCmpProp1,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedSlotTypeCmpProp:
        VArg=s._constraints.getVars()
        tempInstCmpProp0=r.boundedSlotTypeCmpProp[BVars][0]
        tempInstCmpProp1=r.boundedSlotTypeCmpProp[BVars][1]
        tempInstCmpProp2=r.boundedSlotTypeCmpProp[BVars][2]
        # print "BVars, r.boundedSlotTypePerson,r.boundedSlotTypePerson[BVars0,BVars1][0] ",BVars,r.boundedSlotTypePerson, r.boundedSlotTypePerson[BVars][0],r.boundedSlotTypePerson[BVars][1]
        # print "tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars0,BVars1][1]",tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars][2]
        chkArg=lookInExistVars(tempInstCmpProp0,tempInstCmpProp1,VArg)
        AddConstOnt_Slot_CmpPropWith_2_Arg(s,tempInstCmpProp1,tempInstCmpProp2,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedInstanceCmpProp:
        VArg=s._constraints.getVars()
        tempClsCmpProp0=r.boundedInstanceCmpProp[BVars][0]
        tempSlotCmpProp1=r.boundedInstanceCmpProp[BVars][1]
        tempInstCmpProp2=r.boundedInstanceCmpProp[BVars][2]
        # print "BVars r.boundedInstancePerson,r.boundedInstancePerson[BVars0,BVars1][0] ",BVars,r.boundedInstancePerson, r.boundedInstancePerson[BVars][0],r.boundedInstancePerson[BVars][1],r.boundedInstancePerson[BVars][2]
        # print "tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars0,BVars1][1]",tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars][2]
        chkArg=lookInExistVars(tempSlotCmpProp1,tempInstCmpProp2,VArg)
        AddConstOnt_Inst_CmpPropWith_2_Arg(s,ont_CmpPropVar,tempClsCmpProp0,tempSlotCmpProp1,tempInstCmpProp2,chkArg,k)
        k=k+1

    k=0
    for BVars in r.boundedClassWhat:
        tempClassWhat=r.boundedClassWhat[BVars]
        s._constraints.addNewVariable(tempClassWhat)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempClassWhat,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_What_"+ str(k),[ont_WhatVar,s._constraints._vars[-1]._var],[ont_WhatVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSlotTypeWhat:
        tempSlotTypeWhat0=r.boundedSlotTypeWhat[BVars][0]
        tempSlotTypeWhat1=r.boundedSlotTypeWhat[BVars][1]
        s._constraints.addNewVariable(tempSlotTypeWhat1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSlotTypeWhat1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_What_"+ str(k),[ont_WhatVar,s._constraints._vars[-1]._var],[ont_WhatVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSubClassWhat:
        VArg=s._constraints.getVars()
        tempSubClassSlotTypeWhat0=r.boundedSubClassWhat[BVars][0]
        tempSubClassSlotTypeWhat1=r.boundedSubClassWhat[BVars][1]
        # print "BVars, r.Qvar.boundedSubClassWhere_in,r.Qvar.boundedSubClassWhere_in[BVars][0] ",BVars,r.boundedSubClassWhere_in, r.boundedSubClassWhere_in[BVars][0],r.boundedSubClassWhere_in[BVars][1]
        s._constraints.addNewVariable(tempSubClassSlotTypeWhat1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSubClassSlotTypeWhat1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        chkArg=lookInExistVars(tempSubClassSlotTypeWhat0,tempSubClassSlotTypeWhat1,VArg)
        if chkArg[0]!=-1 and chkArg[1]!=-1:
            # print "boundedSubClassWhere_in in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
            s._constraints.addNewConstraint("ont_Subclass_"+ str(k),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
        else:
            print "NOT boundedSubClassWhat in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]

        k=k+1

    i=0
    for BVars in r.boundedInstanceWhat:
        VArg=s._constraints.getVars()
        tempClsWhat0=r.boundedInstanceWhat[BVars][0]
        tempSlotWhat1=r.boundedInstanceWhat[BVars][1]
        # print "BVars, r.boundedInstanceWhere_in[0],r.boundedInstanceWhere_in[1] ",BVars,r.boundedInstanceWhere_in[BVars][0],r.boundedInstanceWhere_in[BVars][1]
        chkArg=lookInExistVars(tempClsWhat0,tempSlotWhat1,VArg)
        AddConstOnt_Slot_EATWith_2_Arg(s,tempClsWhat0,tempSlotWhat1,chkArg,i)
        i=i+1

    i=0
    for BVars in r.boundedInstanceWhat:
        VArg=s._constraints.getVars()
        tempClsWhat0=r.boundedInstanceWhat[BVars][0]
        tempSlotWhat1=r.boundedInstanceWhat[BVars][1]
        tempInsWhat2=r.boundedInstanceWhat[BVars][2]
        # print "BVars, r.boundedInstanceWhere_in[1],r.boundedInstanceWhere_in[2] ",BVars,r.boundedInstanceWhere_in[BVars][1],r.boundedInstanceWhere_in[BVars][2]
        chkArg=lookInExistVars(tempSlotWhat1,tempInsWhat2,VArg)
        AddConstOnt_Inst_EATWith_2_Arg(s,ont_WhatVar,tempClsWhat0,tempSlotWhat1,tempInsWhat2,chkArg,i)
        i=i+1

    i=0
    for BVars in r.boundedExactAnswer:
        VArg=s._constraints.getVars()
        tempClsAnswer0=r.boundedExactAnswer[BVars][0]
        tempSlotAnswer1=r.boundedExactAnswer[BVars][1]
        tempInsAnswer2=r.boundedExactAnswer[BVars][2]
        chkArg=lookInExistVars(tempSlotAnswer1,tempInsAnswer2,VArg)
        AddConstOnt_Inst_AnswerWith_2_Arg(s,"",tempClsAnswer0,tempSlotAnswer1,tempInsAnswer2,chkArg,i)
        i=i+1


def obtainConstraintsWhat_CompoundProperties_Person(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_CompoundProperties_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWhat_CompoundProperties_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_CompoundProperties_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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




def obtainConstraintsWhat_CompoundProperties_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhat_CompoundProperties_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    flagList={}
    i=1
    while i<5 :
        flagList[i]=0
        i=i+1

    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_CmpPropVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_EntVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_WhatVar=s._constraints._vars[-1]._var

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
    # k=0
    # for BVars in r.boundedClassPerson:
    #     print "BVars,r.boundedClassPerson[BVars]: ",BVars, r.boundedClassPerson[BVars]
    #     s._constraints.addNewVariable(r.boundedClassPerson[BVars])
    #     s._constraints.addNewConstraint("class_PER_" + str(k),[r.boundedClassPerson[BVars],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
    #     s._constraints.addNewConstraint("ont_PER_"+ str(k),[ont_PerVar,s._constraints._vars[-1]._var],[ont_PerVar,s._constraints._vars[-1]._var])
    #     k=k+1
    #
    # k=0
    # for BVars0,BVars1 in r.boundedSlotPerson:
    #     VArg=s._constraints.getVars()
    #     tempSlotPerson0=r.boundedSlotPerson[BVars0,BVars1][0]
    #     tempSlotPerson1=r.boundedSlotPerson[BVars0,BVars1][1]
    #     # print "BVars0, BVars1, r.boundedSlotPerson,r.boundedSlotPerson[BVars0,BVars1][0] ",BVars0,BVars1,r.boundedSlotPerson, r.boundedSlotPerson[BVars0,BVars1][0],r.boundedSlotPerson[BVars0,BVars1][1]
    #     # print "tempSlotPerson0,tempSlotPerson1",tempSlotPerson0,tempSlotPerson1
    #     chkArg=lookInExistVars(tempSlotPerson0,tempSlotPerson1,VArg)
    #     AddConstOnt_Slot_PerWith_2_Arg(s,tempSlotPerson0,tempSlotPerson1,chkArg,k)
    #     k=k+1
    #
    # k=0
    # for BVars in r.boundedSlotTypePerson:
    #     VArg=s._constraints.getVars()
    #     tempInstPerson0=r.boundedSlotTypePerson[BVars][0]
    #     tempInstPerson1=r.boundedSlotTypePerson[BVars][1]
    #     tempInstPerson2=r.boundedSlotTypePerson[BVars][2]
    #     # print "BVars, r.boundedSlotTypePerson,r.boundedSlotTypePerson[BVars0,BVars1][0] ",BVars,r.boundedSlotTypePerson, r.boundedSlotTypePerson[BVars][0],r.boundedSlotTypePerson[BVars][1]
    #     # print "tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars0,BVars1][1]",tempInstPerson0,tempInstPerson1,tempInstPerson2,r.boundedSlotTypePerson[BVars][2]
    #     chkArg=lookInExistVars(tempInstPerson0,tempInstPerson1,VArg)
    #     AddConstOnt_Slot_PerWith_2_Arg(s,tempInstPerson1,tempInstPerson2,chkArg,k)
    #     k=k+1
    #
    # k=0
    # for BVars in r.boundedInstancePerson:
    #     VArg=s._constraints.getVars()
    #     tempClsPerson0=r.boundedInstancePerson[BVars][0]
    #     tempSlotPerson1=r.boundedInstancePerson[BVars][1]
    #     tempInstPerson2=r.boundedInstancePerson[BVars][2]
    #     # print "BVars r.boundedInstancePerson,r.boundedInstancePerson[BVars0,BVars1][0] ",BVars,r.boundedInstancePerson, r.boundedInstancePerson[BVars][0],r.boundedInstancePerson[BVars][1],r.boundedInstancePerson[BVars][2]
    #     # print "tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars0,BVars1][1]",tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars][2]
    #     chkArg=lookInExistVars(tempSlotPerson1,tempInstPerson2,VArg)
    #     AddConstOnt_Inst_PerWith_2_Arg(s,ont_PerVar,tempClsPerson0,tempSlotPerson1,tempInstPerson2,chkArg,k)
    #     k=k+1

    k=0
    for BVars in r.boundedClassWhat:
        tempClassWhat=r.boundedClassWhat[BVars]
        s._constraints.addNewVariable(tempClassWhat)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempClassWhat,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_What_"+ str(k),[ont_WhatVar,s._constraints._vars[-1]._var],[ont_WhatVar,s._constraints._vars[-1]._var])
        k=k+1


    for BVars in r.boundedSlotTypeWhat:
        tempSlotTypeWhat0=r.boundedSlotTypeWhat[BVars][0]
        tempSlotTypeWhat1=r.boundedSlotTypeWhat[BVars][1]
        s._constraints.addNewVariable(tempSlotTypeWhat1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSlotTypeWhat1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_What_"+ str(k),[ont_WhatVar,s._constraints._vars[-1]._var],[ont_WhatVar,s._constraints._vars[-1]._var])
        k=k+1


    for BVars in r.boundedSubClassWhat:
        VArg=s._constraints.getVars()
        tempSubClassSlotTypeWhat0=r.boundedSubClassWhat[BVars][0]
        tempSubClassSlotTypeWhat1=r.boundedSubClassWhat[BVars][1]
        # print "BVars, r.Qvar.boundedSubClassWhere_in,r.Qvar.boundedSubClassWhere_in[BVars][0] ",BVars,r.boundedSubClassWhere_in, r.boundedSubClassWhere_in[BVars][0],r.boundedSubClassWhere_in[BVars][1]
        s._constraints.addNewVariable(tempSubClassSlotTypeWhat1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSubClassSlotTypeWhat1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        chkArg=lookInExistVars(tempSubClassSlotTypeWhat0,tempSubClassSlotTypeWhat1,VArg)
        if chkArg[0]!=-1 and chkArg[1]!=-1:
            # print "boundedSubClassWhere_in in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
            s._constraints.addNewConstraint("ont_Subclass_"+ str(k),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
        else:
            print "NOT boundedSubClassWhat in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]

        k=k+1

    i=0
    for BVars in r.boundedInstanceWhat:
        VArg=s._constraints.getVars()
        tempClsWhat0=r.boundedInstanceWhat[BVars][0]
        tempSlotWhat1=r.boundedInstanceWhat[BVars][1]
        # print "BVars, r.boundedInstanceWhere_in[0],r.boundedInstanceWhere_in[1] ",BVars,r.boundedInstanceWhere_in[BVars][0],r.boundedInstanceWhere_in[BVars][1]
        chkArg=lookInExistVars(tempClsWhat0,tempSlotWhat1,VArg)
        AddConstOnt_Slot_EATWith_2_Arg(s,tempClsWhat0,tempSlotWhat1,chkArg,i)
        i=i+1

    i=0
    for BVars in r.boundedInstanceWhat:
        VArg=s._constraints.getVars()
        tempClsWhat0=r.boundedInstanceWhat[BVars][0]
        tempSlotWhat1=r.boundedInstanceWhat[BVars][1]
        tempInsWhat2=r.boundedInstanceWhat[BVars][2]
        # print "BVars, r.boundedInstanceWhere_in[1],r.boundedInstanceWhere_in[2] ",BVars,r.boundedInstanceWhere_in[BVars][1],r.boundedInstanceWhere_in[BVars][2]
        chkArg=lookInExistVars(tempSlotWhat1,tempInsWhat2,VArg)
        AddConstOnt_Inst_EATWith_2_Arg(s,ont_WhatVar,tempClsWhat0,tempSlotWhat1,tempInsWhat2,chkArg,i)
        i=i+1


def obtainConstraintsWhat_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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

def obtainConstraintsWhat_Action_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhat_GEO(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_GEO",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="ont_PER_Cls" and r.boundedVars['ont_PER_Cls']!=None and r.boundedVars['ont_PER_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_PER_Slot" and r.boundedVars['ont_PER_Slot']!=None and r.boundedVars['ont_PER_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_PER_Inst" and r.boundedVars['ont_PER_Inst']!=None and r.boundedVars['ont_PER_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

            elif BVars=="ont_Wherein_Cls" and r.boundedVars['ont_Wherein_Cls']!=None and r.boundedVars['ont_Wherein_Cls']==values:
                s._constraints.addNewConstraint("EAT_class",r.boundedVars['ont_Wherein_Cls'],"")

            elif BVars=="ont_Wherein_Slot" and r.boundedVars['ont_Wherein_Slot']!=None and r.boundedVars['ont_Wherein_Slot']==values:
                s._constraints.addNewConstraint("EAT_slot",r.boundedVars['ont_Wherein_Slot'],"")

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


def obtainConstraintsWhat_Properties_GEO(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_GEO",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="ont_PER_Cls" and r.boundedVars['ont_PER_Cls']!=None and r.boundedVars['ont_PER_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_PER_Slot" and r.boundedVars['ont_PER_Slot']!=None and r.boundedVars['ont_PER_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_PER_Inst" and r.boundedVars['ont_PER_Inst']!=None and r.boundedVars['ont_PER_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

            elif BVars=="ont_Wherein_Cls" and r.boundedVars['ont_Wherein_Cls']!=None and r.boundedVars['ont_Wherein_Cls']==values:
                s._constraints.addNewConstraint("EAT_class",r.boundedVars['ont_Wherein_Cls'],"")

            elif BVars=="ont_Wherein_Slot" and r.boundedVars['ont_Wherein_Slot']!=None and r.boundedVars['ont_Wherein_Slot']==values:
                s._constraints.addNewConstraint("EAT_slot",r.boundedVars['ont_Wherein_Slot'],"")

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

def obtainConstraintsWho_Action_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Action_Entity",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_Ent')
            if BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWho_Action_Entity_CompoundProperties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Action_Entity_CompoundProperties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_Ent')
            if BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWho_Person_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Person_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_PER')
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWho_Properties_GEO(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Properties_GEO",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="ont_PER_Cls" and r.boundedVars['ont_PER_Cls']!=None and r.boundedVars['ont_PER_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_PER_Slot" and r.boundedVars['ont_PER_Slot']!=None and r.boundedVars['ont_PER_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_PER_Inst" and r.boundedVars['ont_PER_Inst']!=None and r.boundedVars['ont_PER_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

            elif BVars=="ont_Wherein_Cls" and r.boundedVars['ont_Wherein_Cls']!=None and r.boundedVars['ont_Wherein_Cls']==values:
                s._constraints.addNewConstraint("EAT_class",r.boundedVars['ont_Wherein_Cls'],"")

            elif BVars=="ont_Wherein_Slot" and r.boundedVars['ont_Wherein_Slot']!=None and r.boundedVars['ont_Wherein_Slot']==values:
                s._constraints.addNewConstraint("EAT_slot",r.boundedVars['ont_Wherein_Slot'],"")

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

def obtainConstraintsWho_Properties_Action_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Properties_Action_GEO",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Quant" and r.boundedVars['tk_Quant']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Quant'])
                s._constraints.addNewConstraint('tk_Quant',[r.boundedVars['tk_Quant'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var


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


def obtainConstraintsWho_Person(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Is_Person",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_PER')
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="ont_PER_Cls" and r.boundedVars['ont_PER_Cls']!=None and r.boundedVars['ont_PER_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_PER_Slot" and r.boundedVars['ont_PER_Slot']!=None and r.boundedVars['ont_PER_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_PER_Inst" and r.boundedVars['ont_PER_Inst']!=None and r.boundedVars['ont_PER_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

            elif BVars=="ont_Wherein_Cls" and r.boundedVars['ont_Wherein_Cls']!=None and r.boundedVars['ont_Wherein_Cls']==values:
                s._constraints.addNewConstraint("EAT_class",r.boundedVars['ont_Wherein_Cls'],"")

            elif BVars=="ont_Wherein_Slot" and r.boundedVars['ont_Wherein_Slot']!=None and r.boundedVars['ont_Wherein_Slot']==values:
                s._constraints.addNewConstraint("EAT_slot",r.boundedVars['ont_Wherein_Slot'],"")

            elif BVars=="ont_ACT" and r.boundedVars['ont_ACT']!=None and r.boundedVars['ont_ACT']==values:
                s._constraints.addNewConstraint("instance",[ont_ActVar,r.boundedVars['ont_ACT']],[ont_ActVar])

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

def obtainConstraintsWhen_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Person_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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

def obtainConstraintsWhen_Action_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for When_Action_Entity",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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


def obtainConstraintsWhen_CompoundProperties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_CompoundProperties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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

def obtainConstraintsWhen_CompoundProperties_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_CompoundProperties_Entity",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhen_Person_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Person_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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

def obtainConstraintsWhen_Action_Properties_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Action_Properties_Entity",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWhen_Action_Properties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Action_CompoundProperties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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




def obtainConstraintsWhen_Action_CompoundProperties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Action_CompoundProperties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhen_Action_CompoundProperties_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Action_CompoundProperties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWhen_GEO_Action(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_GEO_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="ont_PER_Cls" and r.boundedVars['ont_PER_Cls']!=None and r.boundedVars['ont_PER_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_PER_Slot" and r.boundedVars['ont_PER_Slot']!=None and r.boundedVars['ont_PER_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_PER_Inst" and r.boundedVars['ont_PER_Inst']!=None and r.boundedVars['ont_PER_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

            elif BVars=="ont_Wherein_Cls" and r.boundedVars['ont_Wherein_Cls']!=None and r.boundedVars['ont_Wherein_Cls']==values:
                s._constraints.addNewConstraint("EAT_class",r.boundedVars['ont_Wherein_Cls'],"")

            elif BVars=="ont_Wherein_Slot" and r.boundedVars['ont_Wherein_Slot']!=None and r.boundedVars['ont_Wherein_Slot']==values:
                s._constraints.addNewConstraint("EAT_slot",r.boundedVars['ont_Wherein_Slot'],"")

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


def obtainConstraintsWhen_Person(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Person",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_WhenVar=s._constraints._vars[-1]._var

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
    for BVars in r.boundedClassWhen:
        tempClassWhen=r.boundedClassWhen[BVars]
        s._constraints.addNewVariable(tempClassWhen)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempClassWhen,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_When_"+ str(k),[ont_WhenVar,s._constraints._vars[-1]._var],[ont_WhenVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSlotTypeWhen:
        tempSlotTypeWhen0=r.boundedSlotTypeWhen[BVars][0]
        tempSlotTypeWhen1=r.boundedSlotTypeWhen[BVars][1]
        s._constraints.addNewVariable(tempSlotTypeWhen1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSlotTypeWhen1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_When_"+ str(k),[ont_WhenVar,s._constraints._vars[-1]._var],[ont_WhenVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSubClassWhen:
        VArg=s._constraints.getVars()
        tempSubClassSlotTypeWhen0=r.boundedSubClassWhen[BVars][0]
        tempSubClassSlotTypeWhen1=r.boundedSubClassWhen[BVars][1]
        # print "BVars, r.Qvar.boundedSubClassWhere_in,r.Qvar.boundedSubClassWhere_in[BVars][0] ",BVars,r.boundedSubClassWhere_in, r.boundedSubClassWhere_in[BVars][0],r.boundedSubClassWhere_in[BVars][1]
        s._constraints.addNewVariable(tempSubClassSlotTypeWhen1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSubClassSlotTypeWhen1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        chkArg=lookInExistVars(tempSubClassSlotTypeWhen0,tempSubClassSlotTypeWhen1,VArg)
        if chkArg[0]!=-1 and chkArg[1]!=-1:
            # print "boundedSubClassWhere_in in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
            s._constraints.addNewConstraint("ont_Subclass_"+ str(k),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
        else:
            print "NOT boundedSubClassWhen in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]

        k=k+1

    i=0
    for BVars in r.boundedInstanceWhen:
        VArg=s._constraints.getVars()
        tempClsWhen0=r.boundedInstanceWhen[BVars][0]
        tempSlotWhen1=r.boundedInstanceWhen[BVars][1]
        # print "BVars, r.boundedInstanceWhere_in[0],r.boundedInstanceWhere_in[1] ",BVars,r.boundedInstanceWhere_in[BVars][0],r.boundedInstanceWhere_in[BVars][1]
        chkArg=lookInExistVars(tempClsWhen0,tempSlotWhen1,VArg)
        AddConstOnt_Slot_EATWith_2_Arg(s,tempClsWhen0,tempSlotWhen1,chkArg,i)
        i=i+1

    i=0
    for BVars in r.boundedInstanceWhen:
        VArg=s._constraints.getVars()
        tempClsWhen0=r.boundedInstanceWhen[BVars][0]
        tempSlotWhen1=r.boundedInstanceWhen[BVars][1]
        tempInsWhen2=r.boundedInstanceWhen[BVars][2]
        # print "BVars, r.boundedInstanceWhere_in[1],r.boundedInstanceWhere_in[2] ",BVars,r.boundedInstanceWhere_in[BVars][1],r.boundedInstanceWhere_in[BVars][2]
        chkArg=lookInExistVars(tempSlotWhen1,tempInsWhen2,VArg)
        AddConstOnt_Inst_EATWith_2_Arg(s,ont_WhenVar,tempClsWhen0,tempSlotWhen1,tempInsWhen2,chkArg,i)
        i=i+1



def obtainConstraintsWhen_Person_Properties(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for When_Person_Properties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_WhenVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PropVar=s._constraints._vars[-1]._var

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
    print "r.boundedClassPerson",r.boundedClassPerson
    for BVars in r.boundedClassPerson:
        print "BVars,endPER_Cls,startPER_Cls ",BVars
        s._constraints.addNewVariable(r.boundedClassPerson[BVars])
        s._constraints.addNewConstraint("class_PER_" + str(k),[r.boundedClassPerson[BVars],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_PER_"+ str(k),[ont_PerVar,s._constraints._vars[-1]._var],[ont_PerVar,s._constraints._vars[-1]._var])
        k=k+1

    k=0
    for BVars0,BVars1 in r.boundedSlotPerson:
        VArg=s._constraints.getVars()
        tempSlotPerson0=r.boundedSlotPerson[BVars0,BVars1][0]
        tempSlotPerson1=r.boundedSlotPerson[BVars0,BVars1][1]
        print "BVars0, BVars1, r.boundedSlotPerson,r.boundedSlotPerson[BVars0,BVars1][0] ",BVars0,BVars1,r.boundedSlotPerson, r.boundedSlotPerson[BVars0,BVars1][0],r.boundedSlotPerson[BVars0,BVars1][1]
        print "tempSlotPerson0,tempSlotPerson1",tempSlotPerson0,tempSlotPerson1
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
        print "BVars r.boundedInstancePerson,r.boundedInstancePerson[BVars0,BVars1][0] ",BVars,r.boundedInstancePerson, r.boundedInstancePerson[BVars][0],r.boundedInstancePerson[BVars][1],r.boundedInstancePerson[BVars][2]
        print "tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars0,BVars1][1]",tempClsPerson0,tempSlotPerson1,r.boundedInstancePerson[BVars][2]
        chkArg=lookInExistVars(tempSlotPerson1,tempInstPerson2,VArg)
        AddConstOnt_Inst_PerWith_2_Arg(s,ont_PerVar,tempClsPerson0,tempSlotPerson1,tempInstPerson2,chkArg,k)
        k=k+1

    print "r.boundedClassWhen",r.boundedClassWhen
    k=0
    for BVars in r.boundedClassWhen:
        tempClassWhen=r.boundedClassWhen[BVars]
        print "tempClassWhen",tempClassWhen
        s._constraints.addNewVariable(tempClassWhen)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempClassWhen,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_When_"+ str(k),[ont_WhenVar,s._constraints._vars[-1]._var],[ont_WhenVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSlotTypeWhen:
        tempSlotTypeWhen0=r.boundedSlotTypeWhen[BVars][0]
        tempSlotTypeWhen1=r.boundedSlotTypeWhen[BVars][1]
        print "tempSlotTypeWhen0",tempSlotTypeWhen0
        s._constraints.addNewVariable(tempSlotTypeWhen1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSlotTypeWhen1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("ont_When_"+ str(k),[ont_WhenVar,s._constraints._vars[-1]._var],[ont_WhenVar,s._constraints._vars[-1]._var])
        k=k+1

    for BVars in r.boundedSubClassWhen:
        VArg=s._constraints.getVars()
        tempSubClassSlotTypeWhen0=r.boundedSubClassWhen[BVars][0]
        tempSubClassSlotTypeWhen1=r.boundedSubClassWhen[BVars][1]
        print "BVars, r.Qvar.boundedSubClassWhen,r.Qvar.boundedSubClassWhen[BVars][0] ",BVars,r.boundedSubClassWhen, r.boundedSubClassWhen[BVars][0],r.boundedSubClassWhen[BVars][1]
        s._constraints.addNewVariable(tempSubClassSlotTypeWhen1)
        s._constraints.addNewConstraint("EAT_class_" + str(k),[tempSubClassSlotTypeWhen1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        chkArg=lookInExistVars(tempSubClassSlotTypeWhen0,tempSubClassSlotTypeWhen1,VArg)
        if chkArg[0]!=-1 and chkArg[1]!=-1:
            print "boundedSubClassWhen in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]
            s._constraints.addNewConstraint("ont_Subclass_"+ str(k),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])
        else:
            print "NOT boundedSubClassWhen in chkArg[0]!=-1 and chkArg[1]!=-1",chkArg[0],chkArg[1]

        k=k+1

    i=0
    for BVars in r.boundedInstanceWhen:
        VArg=s._constraints.getVars()
        tempClsWhen0=r.boundedInstanceWhen[BVars][0]
        tempSlotWhen1=r.boundedInstanceWhen[BVars][1]
        print "BVars, r.boundedInstanceWhen[0],r.boundedInstanceWhen[1] ",BVars,r.boundedInstanceWhen[BVars][0],r.boundedInstanceWhen[BVars][1]
        chkArg=lookInExistVars(tempClsWhen0,tempSlotWhen1,VArg)
        AddConstOnt_Slot_EATWith_2_Arg(s,tempClsWhen0,tempSlotWhen1,chkArg,i)
        i=i+1

    i=0
    for BVars in r.boundedInstanceWhen:
        VArg=s._constraints.getVars()
        tempClsWhen0=r.boundedInstanceWhen[BVars][0]
        tempSlotWhen1=r.boundedInstanceWhen[BVars][1]
        tempInsWhen2=r.boundedInstanceWhen[BVars][2]
        print "BVars, r.boundedInstanceWhen[1],r.boundedInstanceWhen[2] ",BVars,r.boundedInstanceWhen[BVars][1],r.boundedInstanceWhen[BVars][2]
        chkArg=lookInExistVars(tempSlotWhen1,tempInsWhen2,VArg)
        AddConstOnt_Inst_EATWith_2_Arg(s,ont_WhenVar,tempClsWhen0,tempSlotWhen1,tempInsWhen2,chkArg,i)
        i=i+1


def obtainConstraintsWhere_Properties_Entity_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_CompoundProperties_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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


def obtainConstraintsWhere_CompoundProperties_Entity_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_CompoundProperties_Entity_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)


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


def obtainConstraintsWhere_CompoundProperties_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_CompoundProperties_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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



def obtainConstraintsWhere_CompoundProperties_Person(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_CompoundProperties_Person",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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

def obtainConstraintsWhere_CompoundProperties_Person_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())
    print "Bounded vars for Where_CompoundProperties_Person_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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

def obtainConstraintsWhere_CompoundProperties_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_CompoundProperties_GEO",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_GEO')
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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

def obtainConstraintsWhere_Properties_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_Entity_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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

def obtainConstraintsWhere_Properties_Action_TimeRelation(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_Entity_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_DUR" and r.boundedVars['tk_DUR']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_DUR'])
                s._constraints.addNewConstraint('tk_DUR',[r.boundedVars['tk_DUR'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var


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


def obtainConstraintsWhere_Properties_GEO_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_Properties_GEO_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWhere_Entity_Action(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_Entity_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ENT')
            if BVars=="tk_ENT" and r.boundedVars['tk_ENT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_ENT',[r.boundedVars['tk_ENT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="ont_ENT_Cls" and r.boundedVars['ont_ENT_Cls']!=None and r.boundedVars['ont_ENT_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_ENT_Slot" and r.boundedVars['ont_ENT_Slot']!=None and r.boundedVars['ont_ENT_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_ENT_Inst" and r.boundedVars['ont_ENT_Inst']!=None and r.boundedVars['ont_ENT_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

            elif BVars=="ont_Wherein_Cls" and r.boundedVars['ont_Wherein_Cls']!=None and r.boundedVars['ont_Wherein_Cls']==values:
                s._constraints.addNewConstraint("EAT_class",r.boundedVars['ont_Wherein_Cls'],"")

            elif BVars=="ont_Wherein_Slot" and r.boundedVars['ont_Wherein_Slot']!=None and r.boundedVars['ont_Wherein_Slot']==values:
                s._constraints.addNewConstraint("EAT_slot",r.boundedVars['ont_Wherein_Slot'],"")

            elif BVars=="ont_ACT" and r.boundedVars['ont_ACT']!=None and r.boundedVars['ont_ACT']==values:
                s._constraints.addNewConstraint("instance",[ont_ActVar,r.boundedVars['ont_ACT']],[ont_ActVar])

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


def obtainConstraintsWhere_Properties(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for Where_Properties_Person",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_PER')
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhere_Synonym(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for Where_Synonym",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Syn" and r.boundedVars['tk_Syn']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Syn'])
                s._constraints.addNewConstraint('tk_Syn',[r.boundedVars['tk_Syn'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)


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



def obtainConstraintsWhere_Properties_Synonym(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for What_Synonym",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Syn" and r.boundedVars['tk_Syn']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Syn'])
                s._constraints.addNewConstraint('tk_Syn',[r.boundedVars['tk_Syn'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)


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



def obtainConstraintsWhere_GEO_Action(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Where_GEO_Action",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_ACT')
            if BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhere_CompoundProperties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for Where_Properties_Person",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('ont_PER')
            if BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="ont_PER_Cls" and r.boundedVars['ont_PER_Cls']!=None and r.boundedVars['ont_PER_Cls']==values:
                s._constraints.addNewConstraint("class_PER",[ont_PerVar,r.boundedVars['ont_PER_Cls']],ont_PerVar)

            elif BVars=="ont_PER_Slot" and r.boundedVars['ont_PER_Slot']!=None and r.boundedVars['ont_PER_Slot']==values:
                s._constraints.addNewConstraint("slot_PER",[ont_PerVar,r.boundedVars['ont_PER_Slot']],ont_PerVar)

            elif BVars=="ont_PER_Inst" and r.boundedVars['ont_PER_Inst']!=None and r.boundedVars['ont_PER_Inst']==values:
                s._constraints.addNewConstraint("instance_PER",[ont_PerVar,r.boundedVars['ont_PER_Inst']],ont_PerVar)

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


def obtainConstraintsWho_Action_GEO(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWho_Properties(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Properties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('tk_Prop')
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var


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


def obtainConstraintsWho_Action_Entity_Properties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    boundedClsPerson=sorted(r.boundedClassPerson.values())

    print "Bounded vars for Who_Properties",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            stripBVars=BVars.strip('tk_Prop')
            if BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWhich_Action_TimeRelation(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']!=None and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_FPer" and r.boundedVars['tk_FPer']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_FPer'])
                s._constraints.addNewConstraint('tk_FPer',[r.boundedVars['tk_FPer'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_SPer" and r.boundedVars['tk_SPer']!=None and r.boundedVars['tk_SPer']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SPer'])
                s._constraints.addNewConstraint('tk_SPer',[r.boundedVars['tk_SPer'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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



def obtainConstraintsWhich_Action_TimeRelation_Person(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']!=None and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_FDate" and r.boundedVars['tk_FDate']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_FDate'])
                s._constraints.addNewConstraint('tk_FDate',[r.boundedVars['tk_FDate'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_SDate" and r.boundedVars['tk_SDate']!=None and r.boundedVars['tk_SDate']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SDate'])
                s._constraints.addNewConstraint('tk_SDate',[r.boundedVars['tk_SDate'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhich_Person_Action_Properties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']!=None and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']!=None and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhich_Person_Action(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']!=None and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsWhich_Person_Action_Entity(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']!=None and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']!=None and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsQuantifier_Person_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)

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

def obtainConstraintsQuantifier_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var


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


def obtainConstraintsQuantifier_GEO_Properties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var


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




def obtainConstraintsQuantifier_GEO_CompoundProperties(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var


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


def obtainConstraintsQuantifier_Person(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Type" and r.boundedVars['tk_Type']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Type'])
                s._constraints.addNewConstraint('tk_Type',[r.boundedVars['tk_Type'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var


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


def obtainConstraintsYNo_SubType(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for YNo_SubType",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_SuperType" and r.boundedVars['tk_SuperType']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SuperType'])
                s._constraints.addNewConstraint('tk_SuperType',[r.boundedVars['tk_SuperType'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_SubType" and r.boundedVars['tk_SubType']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SubType'])
                s._constraints.addNewConstraint('tk_SubType',[r.boundedVars['tk_SubType'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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

def obtainConstraintsYNo_Synonym(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    print "Bounded vars for YNo_Synonym",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Nickname" and r.boundedVars['tk_Nickname']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Nickname'])
                s._constraints.addNewConstraint('tk_Nickname',[r.boundedVars['tk_Nickname'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            # elif BVars=="tk_Ent2" and r.boundedVars['tk_Ent2']==values:
            #     s._constraints.addNewVariable(r.boundedVars['tk_Ent2'])
            #     s._constraints.addNewConstraint('tk_Ent2',[r.boundedVars['tk_Ent2'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
            #     ont_ActVar=s._constraints._vars[-1]._var

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

def obtainConstraintsYNo_CompoundProperties_Synonym(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    print "Bounded vars for YNo_Synonym",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Nickname" and r.boundedVars['tk_Nickname']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Nickname'])
                s._constraints.addNewConstraint('tk_Nickname',[r.boundedVars['tk_Nickname'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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

def obtainConstraintsYNo_Equal(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())
    print "Bounded vars for YNo_Equal",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_Ent1" and r.boundedVars['tk_Ent1']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent1'])
                s._constraints.addNewConstraint('tk_Ent1',[r.boundedVars['tk_Ent1'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_Ent2" and r.boundedVars['tk_Ent2']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent2'])
                s._constraints.addNewConstraint('tk_Ent2',[r.boundedVars['tk_Ent2'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsYNo_Properties_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for YNo_Properties_GEO",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Prop" and r.boundedVars['tk_Prop']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Prop'])
                s._constraints.addNewConstraint('tk_Prop',[r.boundedVars['tk_Prop'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsYNo_CompoundProperties_TimeRelation(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_FDate" and r.boundedVars['tk_FDate']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_FDate'])
                s._constraints.addNewConstraint('tk_FDate',[r.boundedVars['tk_FDate'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_SDate" and r.boundedVars['tk_SDate']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SDate'])
                s._constraints.addNewConstraint('tk_SDate',[r.boundedVars['tk_SDate'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            if BVars=="tk_FMetric" and r.boundedVars['tk_FMetric']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_FMetric'])
                s._constraints.addNewConstraint('tk_FMetric',[r.boundedVars['tk_FMetric'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_SMetric" and r.boundedVars['tk_SMetric']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SMetric'])
                s._constraints.addNewConstraint('tk_SMetric',[r.boundedVars['tk_SMetric'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Than" and r.boundedVars['tk_Than']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Than'])
                s._constraints.addNewConstraint('tk_Than',[r.boundedVars['tk_Than'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var


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


def obtainConstraintsYNo_Person_Status(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Status" and r.boundedVars['tk_Status']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Status'])
                s._constraints.addNewConstraint('tk_Status',[r.boundedVars['tk_Status'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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

def obtainConstraintsYNo_Person_Action_Entity(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_Ent" and r.boundedVars['tk_Ent']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_Ent'])
                s._constraints.addNewConstraint('tk_Ent',[r.boundedVars['tk_Ent'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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


def obtainConstraintsYNo_CompoundProperties_Person_Action(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var
            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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

def obtainConstraintsYNo_Person_Action_GEO(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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




def obtainConstraintsYNo_Action_TimeRealation(r,s):
    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_FDate" and r.boundedVars['tk_FDate']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_FDate'])
                s._constraints.addNewConstraint('tk_FDate',[r.boundedVars['tk_FDate'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var
            elif BVars=="tk_SDate" and r.boundedVars['tk_SDate']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_SDate'])
                s._constraints.addNewConstraint('tk_SDate',[r.boundedVars['tk_SDate'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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




def obtainConstraintsYNo_CompoundProperties(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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



def obtainConstraintsYNo_CompoundProperties_GEO(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_GEO" and r.boundedVars['tk_GEO']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_GEO'])
                s._constraints.addNewConstraint('tk_GEO',[r.boundedVars['tk_GEO'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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




def obtainConstraintsYNo_CompoundProperties_Person(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_CmpProp" and r.boundedVars['tk_CmpProp']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_CmpProp'])
                s._constraints.addNewConstraint('tk_CmpProp',[r.boundedVars['tk_CmpProp'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

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





def obtainConstraintsYNo_Person_Action(r,s):

    list_Dep=[]
    sublist=[]
    lst_subDep=[]
    boundedValues=sorted(r.boundedVars.values())

    print "Bounded vars for sentence",s._text(),"is:", r.boundedVars,boundedValues
    for values in boundedValues:
        for BVars in r.boundedVars:
            if BVars=="tk_PER" and r.boundedVars['tk_PER']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_PER'])
                s._constraints.addNewConstraint('tk_PER',[r.boundedVars['tk_PER'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_PerVar=s._constraints._vars[-1]._var

            elif BVars=="tk_ACT" and r.boundedVars['tk_ACT']==values:
                s._constraints.addNewVariable(r.boundedVars['tk_ACT'])
                s._constraints.addNewConstraint('tk_ACT',[r.boundedVars['tk_ACT'],s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
                ont_ActVar=s._constraints._vars[-1]._var

            elif BVars=="ont_PER" and r.boundedVars['ont_PER']!=None and r.boundedVars['ont_PER']==values:
                s._constraints.addNewConstraint("instance",[ont_PerVar,r.boundedVars['ont_PER']],[ont_PerVar])
            elif BVars=="ont_ACT" and r.boundedVars['ont_ACT']!=None and r.boundedVars['ont_ACT']==values:
                s._constraints.addNewConstraint("instance",[ont_ActVar,r.boundedVars['ont_ACT']],[ont_ActVar])

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





def addDepList(s,tk):
    lst_Dep=[]
    type_tk=isinstance(tk,list)
    print "type of tk is:",tk,type_tk
    if type_tk==True:
        ln=len(tk)
        print "Len of tk in addDepList : ", ln
    else:
        ln=1
    tempDEP=s.sint._dependencies
    for element in tempDEP:
        for i in element[:1]:
            j=0
            while (j< ln):
                if ln==1:
                    itk=tk
                else:
                    itk=tk[j]
                if isinstance( itk, int )and str(i) == str(itk):
                    lst_Dep.append(element)
                j=j+1

    lst_Dep.sort()
    return lst_Dep


def sintDp4Tk(r,s,lst_DepSint):
    chkArg=[]
    subListG=[]
    consts_SEN=s._constraints.getConstraints()
    print "rule type, lst_DepSint: ", r.type, lst_DepSint

    for lst_Dep in lst_DepSint:
        VArg=s._constraints.getVars()
        tempstr0=lst_Dep[0]
        tempstr1=lst_Dep[1]

        if  str(lst_Dep[2])=="prep_of" or str(lst_Dep[2])=="prep_for" or str(lst_Dep[2])=="prep_in" or str(lst_Dep[2])=="prepc_in"  or str(lst_Dep[2])=="prep_before" or str(lst_Dep[2])=="prep_after" or \
                (str(lst_Dep[2])=="advmod" and r.type!="Where_Person_Action") or str(lst_Dep[2])=="agent" or str(lst_Dep[2])=="amod" or \
                (str(lst_Dep[2])=="aux" and r.type!="Where_Person_Action") or str(lst_Dep[2])=="auxpass" or str(lst_Dep[2])=="ccomp" or str(lst_Dep[2])=="cop" or \
                        str(lst_Dep[2])=="dep" or str(lst_Dep[2])=="dobj" or str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="mwe" or \
                        str(lst_Dep[2])=="nn" or str(lst_Dep[2])=="nsubjpass" or str(lst_Dep[2])=="num" or str(lst_Dep[2])=="tmod" or str(lst_Dep[2])=="xcomp":

            chkArg=lookInExistVars(tempstr0,tempstr1,VArg)
            print "str(lst_Dep[2]), chkArg0, chkArg1: ", str(lst_Dep[2]), chkArg[0],chkArg[1]
            AddConstWith_2_Arg(s,lst_Dep,chkArg,subListG)

        elif str(lst_Dep[2])=="pobj":
            chkArg=lookInExistVars(tempstr0,tempstr1,VArg)
            AddConstWith_1_ArgSecond(s,lst_Dep,chkArg,subListG)

        elif str(lst_Dep[2])=="det" or str(lst_Dep[2])=="mark" or str(lst_Dep[2])=="prep" or str(lst_Dep[2])=="quantmod":
            chkArg=lookInExistVars(tempstr0,tempstr1,VArg)
            AddConstWith_1_ArgFirst(s,lst_Dep,chkArg,subListG)



    subListG.sort()
    return subListG


def lookInExistVars(TempStr1,TempStr2,VArg_AP):
    temp_vars1=-1
    temp_vars2=-1

    for VArg in VArg_AP:

        if str(TempStr1)==str(VArg._argument):
            temp_vars1=VArg._var

        elif str(TempStr2)==str(VArg._argument):
            temp_vars2=VArg._var

    return temp_vars1,temp_vars2


def AddConstOnt_Slot_CmpPropWith_2_Arg(s,ont_SlotCmpProp0,ont_SlotCmpProp1,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Slot chkArg[0]!=-1 and chkArg[1]==-1: AddConstOnt_Slot_CmpPropWith_2_Arg"
        s._constraints.addNewVariable(ont_SlotCmpProp1)
        s._constraints.addNewConstraint("slot_CmpProp_" + str(idx),[ont_SlotCmpProp1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Slot_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "UHHH... Slot chkArg[0]!=-1 and chkArg[1]!=-1 : AddConstOnt_Slot_CmpPropWith_2_Arg"
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])


def AddConstOnt_Slot_MembWith_2_Arg(s,ont_SlotPerson0,ont_SlotMemb1,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Slot chkArg[0]!=-1 and chkArg[1]==-1: AddConstOnt_Slot_MembWith_2_Arg"
        s._constraints.addNewVariable(ont_SlotMemb1)
        s._constraints.addNewConstraint("slot_Memb_" + str(idx),[ont_SlotMemb1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Slot_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Slot chkArg[0]!=-1 and chkArg[1]!=-1: AddConstOnt_Slot_MembWith_2_Arg"
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])


def AddConstOnt_Slot_EntWith_2_Arg(s,ont_SlotPerson0,ont_SlotEnt1,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Slot chkArg[0]!=-1 and chkArg[1]==-1 : AddConstOnt_Slot_EntWith_2_Arg"
        s._constraints.addNewVariable(ont_SlotEnt1)
        s._constraints.addNewConstraint("slot_Ent_" + str(idx),[ont_SlotEnt1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Slot_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Slot chkArg[0]!=-1 and chkArg[1]!=-1 in AddConstOnt_Slot_EntWith_2_Arg"
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])


def AddConstOnt_Inst_CmpPropWith_2_Arg(s,ont_CmpPropVar,ont_ClsCmpProp0,ont_SlotCmpProp1,ont_InstCmpProp2,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Inst CmpProp chkArg[0]!=-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_InstCmpProp2)
        s._constraints.addNewConstraint("instance_CmpProp_" + str(idx),[ont_InstCmpProp2,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Inst_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Inst CmpProp chkArg[0]!=-1 and chkArg[1]!=-1"
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        print "Inst CmpProp chkArg[0]==-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_InstCmpProp2)
        s._constraints.addNewConstraint("instance_CmpProp_" + str(idx),[ont_InstCmpProp2,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewConstraint("EAT_class_" + str(idx),[ont_WrVar,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewVariable(ont_Cls)
        #
        # s._constraints.addNewConstraint("ont_EAT_"+ str(idx),[ont_Cls,s._constraints._vars[-1]._var],[ont_Cls,s._constraints._vars[-1]._var])


def AddConstOnt_Inst_MembWith_2_Arg(s,ont_PerVar,ont_ClsPerson0,ont_SlotPerson1,ont_InstMemb2,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Inst Memb chkArg[0]!=-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_InstMemb2)
        s._constraints.addNewConstraint("instance_Memb_" + str(idx),[ont_InstMemb2,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Inst_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Inst Memb chkArg[0]!=-1 and chkArg[1]!=-1"
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        print "Inst Memb chkArg[0]==-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_InstMemb2)
        s._constraints.addNewConstraint("instance_Memb_" + str(idx),[ont_InstMemb2,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewConstraint("EAT_class_" + str(idx),[ont_WrVar,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewVariable(ont_Cls)
        #
        # s._constraints.addNewConstraint("ont_EAT_"+ str(idx),[ont_Cls,s._constraints._vars[-1]._var],[ont_Cls,s._constraints._vars[-1]._var])


def AddConstOnt_Inst_EntWith_2_Arg(s,ont_PerVar,ont_ClsPerson0,ont_SlotPerson1,ont_InstEnt2,chkArg,idx):

    if chkArg[0]!=-1 and chkArg[1]==-1:
        print "Inst Entity chkArg[0]!=-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_InstEnt2)
        s._constraints.addNewConstraint("instance_Ent_" + str(idx),[ont_InstEnt2,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        s._constraints.addNewConstraint("Inst_"+ str(idx),[chkArg[0],s._constraints._vars[-1]._var],[chkArg[0],s._constraints._vars[-1]._var])

    elif chkArg[0]!=-1 and chkArg[1]!=-1:
        print "Inst Entity chkArg[0]!=-1 and chkArg[1]!=-1"
        # s._constraints.addNewVariable(ont_SlotPerson1)
        # s._constraints.addNewConstraint("slot_PER_" + str(idx),[ont_SlotPerson1,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # subListG.append(list_Dep[1])
        # s._constraints.addNewConstraint(list_Dep[2],[s._constraints._vars[-1]._var,chkArg[0]],[s._constraints._vars[-1]._var,chkArg[0]])
    elif chkArg[0]==-1 and chkArg[1]==-1:
        print "Inst Entity chkArg[0]==-1 and chkArg[1]==-1"
        s._constraints.addNewVariable(ont_InstEnt2)
        s._constraints.addNewConstraint("instance_Ent_" + str(idx),[ont_InstEnt2,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewConstraint("EAT_class_" + str(idx),[ont_WrVar,s._constraints._vars[-1]._var],s._constraints._vars[-1]._var)
        # s._constraints.addNewVariable(ont_Cls)
        #
        # s._constraints.addNewConstraint("ont_EAT_"+ str(idx),[ont_Cls,s._constraints._vars[-1]._var],[ont_Cls,s._constraints._vars[-1]._var])

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
