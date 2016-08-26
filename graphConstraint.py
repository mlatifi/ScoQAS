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



def add_Node_Arg(dot,Idx,posArg):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    typeIdx=isinstance(Idx,list)
    if typeIdx==True:
        ln=len(Idx)
        i=0
        while (i< ln):
            posInt=int(posArg) + i
            dot.add_node(Idx[i],pos=(posInt,posInt), Arg=Idx[i], label=Idx[i],color="Red", fontsize="11" )
            classText="Node" + "\t" + str(Idx[i]) + "\t:\t" + "{" + "\t" + "Arg :" + "\t" + str(posArg) + "\t" + "}"
            graph2prologfile.write(classText)
            graph2prologfile.write("\n")
            i=i+1
    else:
        posInt=int(posArg)
        dot.add_node(Idx,pos=(posInt,posInt), Arg=Idx, label=Idx,color="Red", fontsize="11" )
        classText="Node" + "\t" + str(Idx) + "\t:\t" + "{" + "\t" + "Arg :" + "\t" + str(posArg) + "\t" + "}"
        graph2prologfile.write(classText)
        graph2prologfile.write("\n")

    graph2prologfile.close()

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

def add_Node_Instance(dot,Idx,Label):
    # graph2prologfile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\data\graphsentence\constraintGraph.txt", 'a+')
    posInt=int(Idx)
    print "Lable for Class",Label
    dot.add_node(Label,pos=(posInt,posInt), Instance=Label, label=Label, color="Red", fontsize="10")
    # classText="Node" + "\t" + str(Idx) + "\t:\t" + "{" + "Instance :" + "\t" + str(Label) + "}"
    # graph2prologfile.write(classText)
    # graph2prologfile.write("\n")
    # graph2prologfile.close()


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

def add_Edge_Var2tk(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    # print "Edge Var---> Token: source,destination",edge
    dot.add_edge(*edge,Predicate=Lbl, label=Lbl, color="Red", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + str(Lbl) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()


def add_Edge_Answer(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    print "Edge Answer: source,destination",edge
    dot.add_edge(*edge,Predicate=Lbl, label=Lbl, color="Black", fontsize="12")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + str(Lbl) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()

def add_Edge_Var2Class(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "constraintGraph.txt", 'a+')
    # print "Edge Variable---> Class: source,destination",edge
    dot.add_edge(*edge,Isa=Lbl, label=Lbl, color="Yellow", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + str(Lbl) + "\t" + "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()

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



