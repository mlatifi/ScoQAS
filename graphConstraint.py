__author__ = 'majid'
# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        graphConstraint.py
#
# Author:      Majid
#
# Created:     2014/12/16
# Creating Graph for Variables of Constraint
#------------------------------------------------------------------------


def build_Constraint_Prolog_Where_Person_Action(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        # print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        print "Predicate,argument,vars",c._predicate,c._arguments,c._vars
        # varArg=c.getVars()
        # arg=varArg.__argument
        # var=varArg._var
        pred=c._predicate
        # print "VarARG:",var,arg
        endPER_Cls=pred.lstrip('class_PER_')
        startPER_Cls=pred.rstrip(endPER_Cls)
        endPER_Slt=pred.lstrip('slot_PER_')
        startPER_Slt=pred.rstrip(endPER_Slt)
        endPER_Ins=pred.lstrip('instance_PER_')
        startPER_Ins=pred.rstrip(endPER_Ins)
        endPER_Ont=pred.lstrip('ont_PER_')
        startPER_Ont=pred.rstrip(endPER_Ont)

        endACT_Cls=pred.lstrip('class_ACT_')
        startACT_Cls=pred.rstrip(endACT_Cls)
        endACT_Slt=pred.lstrip('slot_ACT_')
        startACT_Slt=pred.rstrip(endACT_Slt)
        endACT_Ins=pred.lstrip('instance_ACT_')
        startACT_Ins=pred.rstrip(endACT_Ins)
        endACT_Ont=pred.lstrip('ont_ACT_')
        startACT_Ont=pred.rstrip(endACT_Ont)


        end_Ins=pred.lstrip('Inst_')
        start_Ins=pred.rstrip(end_Ins)

        endWhere_Cls=pred.lstrip('EAT_class_')
        startWhere_Cls=pred.rstrip(endWhere_Cls)
        endWhere_Slt=pred.lstrip('EAT_slot_')
        startWhere_Slt=pred.rstrip(endWhere_Slt)
        endWhere_Ins=pred.lstrip('EAT_inst_')
        startWhere_Ins=pred.rstrip(endWhere_Ins)
        endWhere_Ont=pred.lstrip('ont_Where_')
        startWhere_Ont=pred.rstrip(endWhere_Ont)
        endWhere_Subcls=pred.lstrip('ont_Subclass_')
        startWhere_Subcls=pred.rstrip(endWhere_Subcls)
        endAnswer_Ins=pred.lstrip('Answer_')
        startAnswer_Ins=pred.rstrip(endAnswer_Ins)


        endWhereIn_v_Ins=pred.lstrip('Inst')
        startWhereIn_v_Ins=pred.rstrip(endWhereIn_v_Ins)
        endWhereIn_v_Cls=pred.lstrip('Class')
        startWhereIn_v_Cls=pred.rstrip(endWhereIn_v_Cls)
        endWhereIn_v_Slt=pred.lstrip('Slot')
        startWhereIn_v_Slt=pred.rstrip(endWhereIn_v_Slt)

        if pred=="tk_PER" or pred=="tk_ACT" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)

        elif startPER_Cls=="class_PER_" or startACT_Cls=="class_ACT_" or startWhere_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startPER_Slt=="slot_PER_" or startACT_Slt=="slot_ACT_" or startWhere_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startPER_Ins=="instance_PER_" or startACT_Ins=="instance_ACT_" or startWhere_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWhere_Cls!="EAT_class_" and startWhere_Slt!="EAT_slot_" and startWhere_Ins!="EAT_inst_" and\
                      startPER_Cls!="class_PER_" and startPER_Slt!="slot_PER_" and startPER_Ins!="instance_PER_" and\
                    startACT_Cls!="class_ACT_" and startACT_Slt!="slot_ACT_" and startACT_Ins!="instance_ACT_" and startWhere_Subcls!="ont_Subclass_" and startAnswer_Ins!="Answer_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhere_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1
            elif startAnswer_Ins=="Answer_":
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Answer(dot,e,pred)
                pos=pos+1


    gen_graph(dot,pathgraph)



def build_Constraint_Prolog_Who_Properties_Person(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        # print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        # varArg=c.getVars()
        # arg=varArg.__argument
        # var=varArg._var
        pred=c._predicate
        # print "VarARG:",var,arg
        endPER_Cls=pred.lstrip('class_PER_')
        startPER_Cls=pred.rstrip(endPER_Cls)
        endPER_Slt=pred.lstrip('slot_PER_')
        startPER_Slt=pred.rstrip(endPER_Slt)
        endPER_Ins=pred.lstrip('instance_PER_')
        startPER_Ins=pred.rstrip(endPER_Ins)
        endPER_Ont=pred.lstrip('ont_PER_')
        startPER_Ont=pred.rstrip(endPER_Ont)

        endWho_Cls=pred.lstrip('EAT_class_')
        startWho_Cls=pred.rstrip(endWho_Cls)
        endWho_Slt=pred.lstrip('EAT_slot_')
        startWho_Slt=pred.rstrip(endWho_Slt)
        endWho_Ins=pred.lstrip('EAT_inst_')
        startWho_Ins=pred.rstrip(endWho_Ins)
        endWho_Ont=pred.lstrip('ont_Who_')
        startWho_Ont=pred.rstrip(endWho_Ont)
        endWho_Subcls=pred.lstrip('ont_Subclass_')
        startWho_Subcls=pred.rstrip(endWho_Subcls)

        endWhereIn_v_Ins=pred.lstrip('Inst')
        startWhereIn_v_Ins=pred.rstrip(endWhereIn_v_Ins)
        endWhereIn_v_Cls=pred.lstrip('Class')
        startWhereIn_v_Cls=pred.rstrip(endWhereIn_v_Cls)
        endWhereIn_v_Slt=pred.lstrip('Slot')
        startWhereIn_v_Slt=pred.rstrip(endWhereIn_v_Slt)

        if pred=="tk_PER" or pred=="tk_Prop" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)


        elif startPER_Cls=="class_PER_" or startWho_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startPER_Slt=="slot_PER_" or startWho_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startPER_Ins=="instance_PER_" or startWho_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWho_Cls!="EAT_class_" and startWho_Slt!="EAT_slot_" and startWho_Ins!="EAT_inst_" and\
                      startPER_Cls!="class_PER_" and startWho_Cls!="EAT_class_" and\
                      startPER_Slt!="slot_PER_" and startWho_Slt!="EAT_slot_"  and\
                      startPER_Ins!="instance_PER_" and startWho_Ins!="EAT_inst_" and startWho_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWho_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)


def build_Constraint_Prolog_Who_CompoundProperties_Person_Action(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        # print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        pred=c._predicate
        # print "VarARG:",var,arg
        endPER_Cls=pred.lstrip('class_PER_')
        startPER_Cls=pred.rstrip(endPER_Cls)
        endPER_Slt=pred.lstrip('slot_PER_')
        startPER_Slt=pred.rstrip(endPER_Slt)
        endPER_Ins=pred.lstrip('instance_PER_')
        startPER_Ins=pred.rstrip(endPER_Ins)
        endPER_Ont=pred.lstrip('ont_PER_')
        startPER_Ont=pred.rstrip(endPER_Ont)

        endWho_Cls=pred.lstrip('EAT_class_')
        startWho_Cls=pred.rstrip(endWho_Cls)
        endWho_Slt=pred.lstrip('EAT_slot_')
        startWho_Slt=pred.rstrip(endWho_Slt)
        endWho_Ins=pred.lstrip('EAT_inst_')
        startWho_Ins=pred.rstrip(endWho_Ins)
        endWho_Ont=pred.lstrip('ont_Who_')
        startWho_Ont=pred.rstrip(endWho_Ont)
        endWho_Subcls=pred.lstrip('ont_Subclass_')
        startWho_Subcls=pred.rstrip(endWho_Subcls)

        endWhereIn_v_Ins=pred.lstrip('Inst')
        startWhereIn_v_Ins=pred.rstrip(endWhereIn_v_Ins)
        endWhereIn_v_Cls=pred.lstrip('Class')
        startWhereIn_v_Cls=pred.rstrip(endWhereIn_v_Cls)
        endWhereIn_v_Slt=pred.lstrip('Slot')
        startWhereIn_v_Slt=pred.rstrip(endWhereIn_v_Slt)

        if pred=="tk_PER" or pred=="tk_CmpProp" or pred=="tk_ACT" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)
        elif startPER_Cls=="class_PER_" or startWho_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startPER_Slt=="slot_PER_" or startWho_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startPER_Ins=="instance_PER_" or startWho_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWho_Cls!="EAT_class_" and startWho_Slt!="EAT_slot_" and startWho_Ins!="EAT_inst_" and\
                      startPER_Cls!="class_PER_" and startWho_Cls!="EAT_class_" and\
                      startPER_Slt!="slot_PER_" and startWho_Slt!="EAT_slot_"  and\
                      startPER_Ins!="instance_PER_" and startWho_Ins!="EAT_inst_" and startWho_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWho_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)



def build_Constraint_Prolog_Who_Member_CompoundProperties(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        # print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        pred=c._predicate
        # print "VarARG:",var,arg
        endMemb_Cls=pred.lstrip('class_Memb_')
        startMemb_Cls=pred.rstrip(endMemb_Cls)
        endMemb_Slt=pred.lstrip('slot_Memb_')
        startMemb_Slt=pred.rstrip(endMemb_Slt)
        endMemb_Ins=pred.lstrip('instance_Memb_')
        startMemb_Ins=pred.rstrip(endMemb_Ins)
        endMemb_Ont=pred.lstrip('ont_Memb_')
        startMemb_Ont=pred.rstrip(endMemb_Ont)

        endWho_Cls=pred.lstrip('EAT_class_')
        startWho_Cls=pred.rstrip(endWho_Cls)
        endWho_Slt=pred.lstrip('EAT_slot_')
        startWho_Slt=pred.rstrip(endWho_Slt)
        endWho_Ins=pred.lstrip('EAT_inst_')
        startWho_Ins=pred.rstrip(endWho_Ins)
        endWho_Ont=pred.lstrip('ont_Who_')
        startWho_Ont=pred.rstrip(endWho_Ont)
        endWho_Subcls=pred.lstrip('ont_Subclass_')
        startWho_Subcls=pred.rstrip(endWho_Subcls)

        endWhereIn_v_Ins=pred.lstrip('Inst')
        startWhereIn_v_Ins=pred.rstrip(endWhereIn_v_Ins)
        endWhereIn_v_Cls=pred.lstrip('Class')
        startWhereIn_v_Cls=pred.rstrip(endWhereIn_v_Cls)
        endWhereIn_v_Slt=pred.lstrip('Slot')
        startWhereIn_v_Slt=pred.rstrip(endWhereIn_v_Slt)

        if pred=="tk_Memb" or pred=="tk_CmpProp" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)


        elif startMemb_Cls=="class_Memb_" or startWho_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            print "e:  add_Edge_Var2Class ",c._vars,c._arguments
            add_Edge_Var2Class(dot,e,pred)
        elif startMemb_Slt=="slot_Memb_" or startWho_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startMemb_Ins=="instance_Memb_" or startWho_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWho_Cls!="EAT_class_" and startWho_Slt!="EAT_slot_" and startWho_Ins!="EAT_inst_" and\
                      startMemb_Cls!="class_Memb_" and startWho_Cls!="EAT_class_" and\
                      startMemb_Slt!="slot_Memb_" and startWho_Slt!="EAT_slot_"  and\
                      startMemb_Ins!="instance_Memb_" and startWho_Ins!="EAT_inst_" and startWho_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWho_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)


def build_Constraint_Prolog_What_Action_Properties_Status(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        pred=c._predicate
        # print "VarARG:",var,arg
        endMemb_Cls=pred.lstrip('class_Memb_')
        startMemb_Cls=pred.rstrip(endMemb_Cls)
        endMemb_Slt=pred.lstrip('slot_Memb_')
        startMemb_Slt=pred.rstrip(endMemb_Slt)
        endMemb_Ins=pred.lstrip('instance_Memb_')
        startMemb_Ins=pred.rstrip(endMemb_Ins)
        endMemb_Ont=pred.lstrip('ont_Memb_')
        startMemb_Ont=pred.rstrip(endMemb_Ont)

        endWhat_Cls=pred.lstrip('EAT_class_')
        startWhat_Cls=pred.rstrip(endWhat_Cls)
        endWhat_Slt=pred.lstrip('EAT_slot_')
        startWhat_Slt=pred.rstrip(endWhat_Slt)
        endWhat_Ins=pred.lstrip('EAT_inst_')
        startWhat_Ins=pred.rstrip(endWhat_Ins)
        endWhat_Ont=pred.lstrip('ont_What_')
        startWhat_Ont=pred.rstrip(endWhat_Ont)
        endWhat_Subcls=pred.lstrip('ont_Subclass_')
        startWhat_Subcls=pred.rstrip(endWhat_Subcls)

        if pred=="tk_Status" or pred=="tk_Prop" or pred=="tk" or pred=="tk_Type" or pred=="tk_ACT":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)


        elif startMemb_Cls=="class_Memb_" or startWhat_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            print "e:  add_Edge_Var2Class ",c._vars,c._arguments
            add_Edge_Var2Class(dot,e,pred)
        elif startMemb_Slt=="slot_Memb_" or startWhat_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startMemb_Ins=="instance_Memb_" or startWhat_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWhat_Cls!="EAT_class_" and startWhat_Slt!="EAT_slot_" and startWhat_Ins!="EAT_inst_" and\
                      startMemb_Cls!="class_Memb_" and startWhat_Cls!="EAT_class_" and\
                      startMemb_Slt!="slot_Memb_" and startWhat_Slt!="EAT_slot_"  and\
                      startMemb_Ins!="instance_Memb_" and startWhat_Ins!="EAT_inst_" and startWhat_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhat_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)

def build_Constraint_Prolog_What_Properties_Entity(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        pred=c._predicate
        endEnt_Cls=pred.lstrip('class_Ent_')
        startEnt_Cls=pred.rstrip(endEnt_Cls)
        endEnt_Slt=pred.lstrip('slot_Ent_')
        startEnt_Slt=pred.rstrip(endEnt_Slt)
        endEnt_Ins=pred.lstrip('instance_Ent_')
        startEnt_Ins=pred.rstrip(endEnt_Ins)
        endEnt_Ont=pred.lstrip('ont_Ent_')
        startEnt_Ont=pred.rstrip(endEnt_Ont)

        endWhat_Cls=pred.lstrip('EAT_class_')
        startWhat_Cls=pred.rstrip(endWhat_Cls)
        endWhat_Slt=pred.lstrip('EAT_slot_')
        startWhat_Slt=pred.rstrip(endWhat_Slt)
        endWhat_Ins=pred.lstrip('EAT_inst_')
        startWhat_Ins=pred.rstrip(endWhat_Ins)
        endWhat_Ont=pred.lstrip('ont_What_')
        startWhat_Ont=pred.rstrip(endWhat_Ont)
        endWhat_Subcls=pred.lstrip('ont_Subclass_')
        startWhat_Subcls=pred.rstrip(endWhat_Subcls)

        if pred=="tk_Ent" or pred=="tk_Prop" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)

        elif startEnt_Cls=="class_Ent_" or startWhat_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startEnt_Slt=="slot_Ent_" or startWhat_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startEnt_Ins=="instance_Ent_" or startWhat_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWhat_Cls!="EAT_class_" and startWhat_Slt!="EAT_slot_" and startWhat_Ins!="EAT_inst_" and\
                      startEnt_Cls!="class_Ent_" and startWhat_Cls!="EAT_class_" and\
                      startEnt_Slt!="slot_Ent_" and startWhat_Slt!="EAT_slot_"  and\
                      startEnt_Ins!="instance_Ent_" and startWhat_Ins!="EAT_inst_" and startWhat_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhat_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)


def build_Constraint_Prolog_What_CompoundProperties_Entity(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        pred=c._predicate
        # print "VarARG:",var,arg
        endMemb_Cls=pred.lstrip('class_Memb_')
        startMemb_Cls=pred.rstrip(endMemb_Cls)
        endMemb_Slt=pred.lstrip('slot_Memb_')
        startMemb_Slt=pred.rstrip(endMemb_Slt)
        endMemb_Ins=pred.lstrip('instance_Memb_')
        startMemb_Ins=pred.rstrip(endMemb_Ins)
        endMemb_Ont=pred.lstrip('ont_Memb_')
        startMemb_Ont=pred.rstrip(endMemb_Ont)

        endWhat_Cls=pred.lstrip('EAT_class_')
        startWhat_Cls=pred.rstrip(endWhat_Cls)
        endWhat_Slt=pred.lstrip('EAT_slot_')
        startWhat_Slt=pred.rstrip(endWhat_Slt)
        endWhat_Ins=pred.lstrip('EAT_inst_')
        startWhat_Ins=pred.rstrip(endWhat_Ins)
        endWhat_Ont=pred.lstrip('ont_What_')
        startWhat_Ont=pred.rstrip(endWhat_Ont)
        endWhat_Subcls=pred.lstrip('ont_Subclass_')
        startWhat_Subcls=pred.rstrip(endWhat_Subcls)

        if pred=="tk_Ent" or pred=="tk_CmpProp" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)

        elif startMemb_Cls=="class_Memb_" or startWhat_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startMemb_Slt=="slot_Memb_" or startWhat_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startMemb_Ins=="instance_Memb_" or startWhat_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWhat_Cls!="EAT_class_" and startWhat_Slt!="EAT_slot_" and startWhat_Ins!="EAT_inst_" and\
                      startMemb_Cls!="class_Memb_" and startWhat_Cls!="EAT_class_" and\
                      startMemb_Slt!="slot_Memb_" and startWhat_Slt!="EAT_slot_"  and\
                      startMemb_Ins!="instance_Memb_" and startWhat_Ins!="EAT_inst_" and startWhat_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhat_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)



def build_Constraint_Prolog_Howmuch_Properties_Person(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        # varArg=c.getVars()
        # arg=varArg.__argument
        # var=varArg._var
        pred=c._predicate
        # print "VarARG:",var,arg
        endPer_Cls=pred.lstrip('class_PER_')
        startPer_Cls=pred.rstrip(endPer_Cls)
        endPer_Slt=pred.lstrip('slot_PER_')
        startPer_Slt=pred.rstrip(endPer_Slt)
        endPer_Ins=pred.lstrip('instance_PER_')
        startPer_Ins=pred.rstrip(endPer_Ins)
        endPer_Ont=pred.lstrip('ont_PER_')
        startPer_Ont=pred.rstrip(endPer_Ont)

        endHowmuch_Cls=pred.lstrip('EAT_class_')
        startHowmuch_Cls=pred.rstrip(endHowmuch_Cls)
        endHowmuch_Slt=pred.lstrip('EAT_slot_')
        startHowmuch_Slt=pred.rstrip(endHowmuch_Slt)
        endHowmuch_Ins=pred.lstrip('EAT_inst_')
        startHowmuch_Ins=pred.rstrip(endHowmuch_Ins)
        endHowmuch_Ont=pred.lstrip('ont_Howmuch_')
        startHowmuch_Ont=pred.rstrip(endHowmuch_Ont)
        endHowmuch_Subcls=pred.lstrip('ont_Subclass_')
        startHowmuch_Subcls=pred.rstrip(endHowmuch_Subcls)

        if pred=="tk_Prop" or pred=="tk" or pred=="tk_Type" or pred=="tk_PER":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)


        elif startPer_Cls=="class_PER_" or startHowmuch_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startPer_Slt=="slot_PER_" or startHowmuch_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startPer_Ins=="instance_PER_" or startHowmuch_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startHowmuch_Cls!="EAT_class_" and startHowmuch_Slt!="EAT_slot_" and startHowmuch_Ins!="EAT_inst_" and\
                      startPer_Cls!="class_PER_" and startHowmuch_Cls!="EAT_class_" and\
                      startPer_Slt!="slot_PER_" and startHowmuch_Slt!="EAT_slot_"  and\
                      startPer_Ins!="instance_PER_" and startHowmuch_Ins!="EAT_inst_" and startHowmuch_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startHowmuch_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)



def build_Constraint_Prolog_Howmuch_CompoundProperties(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        # varArg=c.getVars()
        # arg=varArg.__argument
        # var=varArg._var
        pred=c._predicate
        # print "VarARG:",var,arg
        endCmpProp_Cls=pred.lstrip('class_CmpProp_')
        startCmpProp_Cls=pred.rstrip(endCmpProp_Cls)
        endCmpProp_Slt=pred.lstrip('slot_CmpProp_')
        startCmpProp_Slt=pred.rstrip(endCmpProp_Slt)
        endCmpProp_Ins=pred.lstrip('instance_CmpProp_')
        startCmpProp_Ins=pred.rstrip(endCmpProp_Ins)
        endCmpProp_Ont=pred.lstrip('ont_CmpProp_')
        startCmpProp_Ont=pred.rstrip(endCmpProp_Ont)

        end_Ins=pred.lstrip('Inst_')
        start_Ins=pred.rstrip(end_Ins)

        endHowmuch_Cls=pred.lstrip('EAT_class_')
        startHowmuch_Cls=pred.rstrip(endHowmuch_Cls)
        endHowmuch_Slt=pred.lstrip('EAT_slot_')
        startHowmuch_Slt=pred.rstrip(endHowmuch_Slt)
        endHowmuch_Ins=pred.lstrip('EAT_inst_')
        startHowmuch_Ins=pred.rstrip(endHowmuch_Ins)
        endHowmuch_Ont=pred.lstrip('ont_Howmuch_')
        startHowmuch_Ont=pred.rstrip(endHowmuch_Ont)
        endHowmuch_Subcls=pred.lstrip('ont_Subclass_')
        startHowmuch_Subcls=pred.rstrip(endHowmuch_Subcls)
        endAnswer_Ins=pred.lstrip('Answer_')
        startAnswer_Ins=pred.rstrip(endAnswer_Ins)

        if pred=="tk_CmpProp" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)


        elif startCmpProp_Cls=="class_CmpProp_" or startHowmuch_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startCmpProp_Slt=="slot_CmpProp_" or startHowmuch_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startCmpProp_Ins=="instance_CmpProp_" or startHowmuch_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)

        elif pred!="det":
            if startHowmuch_Cls!="EAT_class_" and startHowmuch_Slt!="EAT_slot_" and startHowmuch_Ins!="EAT_inst_" and\
                      startCmpProp_Cls!="class_CmpProp_" and startCmpProp_Slt!="slot_CmpProp_" and\
                      startCmpProp_Ins!="instance_CmpProp_" and startHowmuch_Subcls!="ont_Subclass_" and startAnswer_Ins!="Answer_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startHowmuch_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1
            elif startAnswer_Ins=="Answer_":
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Answer(dot,e,pred)
                pos=pos+1


    gen_graph(dot,pathgraph)




def build_Constraint_Prolog_What_CompoundProperties(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        pred=c._predicate
        # print "VarARG:",var,arg
        endCmpProp_Cls=pred.lstrip('class_CmpProp_')
        startCmpProp_Cls=pred.rstrip(endCmpProp_Cls)
        endCmpProp_Slt=pred.lstrip('slot_CmpProp_')
        startCmpProp_Slt=pred.rstrip(endCmpProp_Slt)
        endCmpProp_Ins=pred.lstrip('instance_CmpProp_')
        startCmpProp_Ins=pred.rstrip(endCmpProp_Ins)
        endCmpProp_Ont=pred.lstrip('ont_CmpProp_')
        startCmpProp_Ont=pred.rstrip(endCmpProp_Ont)

        end_Ins=pred.lstrip('Inst_')
        start_Ins=pred.rstrip(end_Ins)

        endWhat_Cls=pred.lstrip('EAT_class_')
        startWhat_Cls=pred.rstrip(endWhat_Cls)
        endWhat_Slt=pred.lstrip('EAT_slot_')
        startWhat_Slt=pred.rstrip(endWhat_Slt)
        endWhat_Ins=pred.lstrip('EAT_inst_')
        startWhat_Ins=pred.rstrip(endWhat_Ins)
        endWhat_Ont=pred.lstrip('ont_Howmuch_')
        startWhat_Ont=pred.rstrip(endWhat_Ont)
        endWhat_Subcls=pred.lstrip('ont_Subclass_')
        startWhat_Subcls=pred.rstrip(endWhat_Subcls)
        endAnswer_Ins=pred.lstrip('Answer_')
        startAnswer_Ins=pred.rstrip(endAnswer_Ins)

        if pred=="tk_CmpProp" or pred=="tk" or pred=="tk_Type":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)

        elif startCmpProp_Cls=="class_CmpProp_" or startWhat_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startCmpProp_Slt=="slot_CmpProp_" or startWhat_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startCmpProp_Ins=="instance_CmpProp_" or startWhat_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)

        elif pred!="det":
            if startWhat_Cls!="EAT_class_" and startWhat_Slt!="EAT_slot_" and startWhat_Ins!="EAT_inst_" and\
                      startCmpProp_Cls!="class_CmpProp_" and startWhat_Cls!="EAT_class_" and\
                      startCmpProp_Slt!="slot_CmpProp_" and startWhat_Slt!="EAT_slot_"  and\
                      startCmpProp_Ins!="instance_CmpProp_" and startWhat_Ins!="EAT_inst_"  and startWhat_Subcls!="ont_Subclass_" and startAnswer_Ins!="Answer_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhat_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1
            elif startAnswer_Ins=="Answer_":
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Answer(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)


def build_Constraint_Prolog_When_Person(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        # varArg=c.getVars()
        # arg=varArg.__argument
        # var=varArg._var
        pred=c._predicate
        # print "VarARG:",var,arg
        endPer_Cls=pred.lstrip('class_PER_')
        startPer_Cls=pred.rstrip(endPer_Cls)
        endPer_Slt=pred.lstrip('slot_PER_')
        startPer_Slt=pred.rstrip(endPer_Slt)
        endPer_Ins=pred.lstrip('instance_PER_')
        startPer_Ins=pred.rstrip(endPer_Ins)
        endPer_Ont=pred.lstrip('ont_PER_')
        startPer_Ont=pred.rstrip(endPer_Ont)

        endWhen_Cls=pred.lstrip('EAT_class_')
        startWhen_Cls=pred.rstrip(endWhen_Cls)
        endWhen_Slt=pred.lstrip('EAT_slot_')
        startWhen_Slt=pred.rstrip(endWhen_Slt)
        endWhen_Ins=pred.lstrip('EAT_inst_')
        startWhen_Ins=pred.rstrip(endWhen_Ins)
        endWhen_Ont=pred.lstrip('ont_When_')
        startWhen_Ont=pred.rstrip(endWhen_Ont)
        endWhen_Subcls=pred.lstrip('ont_Subclass_')
        startWhen_Subcls=pred.rstrip(endWhen_Subcls)

        if pred=="tk_Prop" or pred=="tk" or pred=="tk_Type" or pred=="tk_PER":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)

        elif startPer_Cls=="class_PER_" or startWhen_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startPer_Slt=="slot_PER_" or startWhen_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startPer_Ins=="instance_PER_" or startWhen_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWhen_Cls!="EAT_class_" and startWhen_Slt!="EAT_slot_" and startWhen_Ins!="EAT_inst_" and\
                      startPer_Cls!="class_PER_" and startWhen_Cls!="EAT_class_" and\
                      startPer_Slt!="slot_PER_" and startWhen_Slt!="EAT_slot_"  and\
                      startPer_Ins!="instance_PER_" and startWhen_Ins!="EAT_inst_" and startWhen_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhen_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)




def build_Constraint_Prolog_When_Person_Properties(s,workingdirectory):
    global currentRule
    pathgraph=workingdirectory + "graphsentence/"
    from rule import currentRule
    Qvar=currentRule
    dot=Qvar.currentConsDGraph
    cs = s._constraints
    cs.describe()
    VArg=cs.getVars()
    for vars in VArg:
        arg=vars._argument
        var=vars._var
        print "arg, var:",arg,var
        posArgInt=add_Node_Var(dot,var)
        posArgInt=posArgInt-100
        add_Node_Arg(dot,arg,posArgInt)
    const=cs.getConstraints()
    pos=200
    for c in const:
        # print "Predicate,argument,vars in build_Constraint_Graph_Who_Properties_Person ",c._predicate,c._arguments,c._vars
        # varArg=c.getVars()
        # arg=varArg.__argument
        # var=varArg._var
        pred=c._predicate
        # print "VarARG:",var,arg
        endPer_Cls=pred.lstrip('class_PER_')
        startPer_Cls=pred.rstrip(endPer_Cls)
        endPer_Slt=pred.lstrip('slot_PER_')
        startPer_Slt=pred.rstrip(endPer_Slt)
        endPer_Ins=pred.lstrip('instance_PER_')
        startPer_Ins=pred.rstrip(endPer_Ins)
        endPer_Ont=pred.lstrip('ont_PER_')
        startPer_Ont=pred.rstrip(endPer_Ont)

        endWhen_Cls=pred.lstrip('EAT_class_')
        startWhen_Cls=pred.rstrip(endWhen_Cls)
        endWhen_Slt=pred.lstrip('EAT_slot_')
        startWhen_Slt=pred.rstrip(endWhen_Slt)
        endWhen_Ins=pred.lstrip('EAT_inst_')
        startWhen_Ins=pred.rstrip(endWhen_Ins)
        endWhen_Ont=pred.lstrip('ont_When_')
        startWhen_Ont=pred.rstrip(endWhen_Ont)
        endWhen_Subcls=pred.lstrip('ont_Subclass_')
        startWhen_Subcls=pred.rstrip(endWhen_Subcls)

        if pred=="tk_Prop" or pred=="tk" or pred=="tk_Type" or pred=="tk_PER":
            typeIdx=isinstance(c._arguments[0],list)
            if typeIdx==True:
                ln=len(c._arguments[0])
                i=0
                while (i< ln):
                    e=(c._vars,c._arguments[0][i])
                    add_Edge_Var2tk(dot,e,pred)
                    i=i+1
            else:
                e=(c._vars,c._arguments[0])
                add_Edge_Var2tk(dot,e,pred)

        elif startPer_Cls=="class_PER_" or startWhen_Cls=="EAT_class_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Class(dot,e,pred)
        elif startPer_Slt=="slot_PER_" or startWhen_Slt=="EAT_slot_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Slot(dot,e,pred)
        elif startPer_Ins=="instance_PER_" or startWhen_Ins=="EAT_inst_":
            e=(c._vars,c._arguments[0])
            add_Edge_Var2Instance(dot,e,pred)
        elif pred!="det":
            if startWhen_Cls!="EAT_class_" and startWhen_Slt!="EAT_slot_" and startWhen_Ins!="EAT_inst_" and\
                      startPer_Cls!="class_PER_" and startWhen_Cls!="EAT_class_" and\
                      startPer_Slt!="slot_PER_" and startWhen_Slt!="EAT_slot_"  and\
                      startPer_Ins!="instance_PER_" and startWhen_Ins!="EAT_inst_" and startWhen_Subcls!="ont_Subclass_":
                print "pred,c._arguments[0],c._arguments[1]",pred,c._arguments[1]
                add_Node_Instance(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2tk(dot,e,pred)
                pos=pos+1
            elif startWhen_Subcls=="ont_Subclass_":
                add_Node_Subclass(dot,pos,c._arguments[1])
                e=(c._arguments[0],c._arguments[1])
                add_Edge_Var2SubClass(dot,e,pred)
                pos=pos+1

    gen_graph(dot,pathgraph)



def add_Node_Var(dot,Idx):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    print "Var: Idx,Label",Idx
    pos=Idx.strip('X')
    posInt=int(pos)
    posInt=posInt*50+100
    # print "posInt,Var",posInt,Idx
    dot.add_node(Idx,pos=(posInt,posInt), Var=Idx, label=Idx,color="Blue", fontsize="11" )
    classText="Node" + "\t" + str(Idx) + "\t:\t" + "{" + "\t" + "Var :" + "\t" + str(Idx) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()

    return posInt


def add_Node_Subclass(dot,Idx,Label):
    # graph2prologfile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\data\graphsentence\constraintGraph.txt", 'a+')
    posInt=int(Idx)
    print "Lable for SubClass",Label
    dot.add_node(Label,pos=(posInt,posInt), Instance=Label, label=Label, color="Red", fontsize="10")
    # classText="Node" + "\t" + str(Idx) + "\t:\t" + "{" + "Subclass :" + "\t" + str(Label) + "}"
    # graph2prologfile.write(classText)
    # graph2prologfile.write("\n")
    # graph2prologfile.close()


def add_Edge_Slot(dot,src,dest):
    print "Edge Slot: source,destination",src,dest
    dot.add_edge(src, dest, 'link Slot')


def add_Edge_Var2Slot(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')

    # print "Edge Variable---> Slot: source,destination",edge
    dot.add_edge(*edge,Isa=Lbl, label=Lbl, color="Blue", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + str(Lbl) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()

def add_Edge_Var2SubClass(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    # print "Edge Variable---> SubClass: source,destination",edge
    dot.add_edge(*edge,Isa=Lbl, label=Lbl, color="Brown", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + str(Lbl) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()

def add_Edge_Var2Instance(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    # print "Edge Variable---> Instance: source,destination",edge
    dot.add_edge(*edge,Isa=Lbl, label=Lbl, color="Green", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + str(Lbl) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()


def remove_Node_Class(dot,Idx):
    dot.remove_node(Idx)
    print " Class was removed",Idx


def gen_graph(dot,path):
    g=nx.DiGraph()
    pos=nx.get_node_attributes(dot,'pos')
    Var=nx.get_node_attributes(dot,'Var')
    # Instance=nx.get_node_attributes(dot,'Instance')
    # Subclass=nx.get_node_attributes(dot,'Isa')

    print "positions are",pos
    # print "Instanece",Instance
    print "Var",Var
    # print "Subclass",Subclass
    nx.draw_networkx_edge_labels(dot,pos=pos)
    nx.write_dot(dot,path + 'graphConstraint.dot')
    print "All of Nodes for graph constraint are: \n", dot.nodes(data=True)


def gen_CombineGraph(dot,path):
    g=nx.DiGraph()
    pos=nx.get_node_attributes(dot,'pos')
    Var=nx.get_node_attributes(dot,'Var')
    # Instance=nx.get_node_attributes(dot,'Instance')
    # Subclass=nx.get_node_attributes(dot,'Isa')
    Class=nx.get_node_attributes(dot,'Class')
    Instance=nx.get_node_attributes(dot,'Instance')
    Subclass=nx.get_node_attributes(dot,'Isa')


    print "Combined positions are",pos
    # print "Instanece",Instance
    print "Var",Var
    # print "Subclass",Subclass
    nx.draw_networkx_edge_labels(dot,pos=pos)
    nx.write_dot(dot,path + 'graphCombined.dot')
    print "All of Nodes are:", dot.nodes(data=True)






