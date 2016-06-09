__author__ = 'majid'
# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        prologGraph.py
#
# Author:      Majid
#
# Created:     2015/12/25
# Creating Graph for Prolog text file
#------------------------------------------------------------------------

from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import string



def build_Prolog_Graph_Where_Person_Action(s,WorkingDirectory,output):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10
    if output=="CONST":
        prolog2graphfile = open(path + "constraintGraph.txt", 'a+')
    elif output=="MERGE":
        prolog2graphfile = open(path + "mergePrologGraph.txt", 'a+')

    while True:
        textLine=prolog2graphfile.readline()
        while textLine=="\n":
            textLine=prolog2graphfile.readline()
        if len(textLine) == 0:
            print "Break at line : " , pos
            break
        print "textline for prolog2graphfile:",textLine
        newtxtTab=string.split(textLine,None)

        if newtxtTab[0]=="Node":
            i=1
            argNode1=newtxtTab[1]
            if argNode1.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(argNode1)
                argNode1=str(argNode1[ln1:ln2])
            while(newtxtTab[i+1]!=":"):
                argNode1=argNode1 + " " + newtxtTab[i+1]
                i=i+1
            j=i+3
            nodeLabel=str(newtxtTab[j])
            k=j+2
            argLabel=newtxtTab[k]
            while(newtxtTab[k+1]!="}"):
                argLabel=argLabel + " " + newtxtTab[k+1]
                k=k+1
            if nodeLabel.startswith('Class'):
                add_Node_Var_Class_Prolog(dotPr,argNode1,str(argLabel),pos)
            elif nodeLabel.startswith('Instance'):
                add_Node_Instance_Prolog(dotPr,argNode1,str(argLabel),pos)
            else:
                add_Node_Var_Prolog(dotPr,str(argNode1),pos)

        elif newtxtTab[0]=="Edge":
            i=2
            arg2=newtxtTab[i]
            arg2=arg2.lstrip("'")
            if arg2.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(arg2)
                arg2=str(arg2[ln1:ln2])

            while(newtxtTab[i+1]!=":"):
                arg2=arg2 + " " + str(newtxtTab[i+1])
                i=i+1
            arg2=arg2.rstrip("')")
            arg1=newtxtTab[1].lstrip("('")
            arg1=arg1.rstrip("',")
            item1=arg1
            item2=arg2

            e=(item1,item2)
            edgeLabel=str(newtxtTab[i+3])
            if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
                add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
                add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_inst_'):
                add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('instance_'):
                add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Class":
                add_Edge_Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Instance":
                add_Edge_Instance_Prolog(dotPr,e,edgeLabel)
            else:
                add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
        pos=pos+5
    prolog2graphfile.close()
    gen_prolog_graph(dotPr,path,output)

def build_Prolog_Graph_Who_Properties_Person(s,WorkingDirectory,output):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10
    if output=="CONST":
        prolog2graphfile = open(path + "constraintGraph.txt", 'a+')
    elif output=="MERGE":
        prolog2graphfile = open(path + "mergePrologGraph.txt", 'a+')


    while True:
        textLine=prolog2graphfile.readline()
        while textLine=="\n":
            textLine=prolog2graphfile.readline()
        if len(textLine) == 0:
            break
        # print "textline for prolog2graphfile:",textLine
        newtxtTab=string.split(textLine,None)

        if newtxtTab[0]=="Node":
            i=1
            argNode1=newtxtTab[1]
            if argNode1.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(argNode1)
                argNode1=str(argNode1[ln1:ln2])
            while(newtxtTab[i+1]!=":"):
                argNode1=argNode1 + " " + newtxtTab[i+1]
                i=i+1
            j=i+3
            nodeLabel=str(newtxtTab[j])
            k=j+2
            argLabel=newtxtTab[k]
            while(newtxtTab[k+1]!="}"):
                argLabel=argLabel + " " + newtxtTab[k+1]
                k=k+1

            if nodeLabel.startswith('Class'):
                add_Node_Var_Class_Prolog(dotPr,argNode1,str(argLabel),pos)
            elif nodeLabel.startswith('Instance'):
                add_Node_Instance_Prolog(dotPr,argNode1,str(argLabel),pos)
            else:
                add_Node_Var_Prolog(dotPr,str(argNode1),pos)

        elif newtxtTab[0]=="Edge":
            i=2
            arg2=newtxtTab[i]
            arg2=arg2.lstrip("'")
            if arg2.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(arg2)
                arg2=str(arg2[ln1:ln2])

            while(newtxtTab[i+1]!=":"):
                arg2=arg2 + " " + str(newtxtTab[i+1])
                i=i+1
            arg2=arg2.rstrip("')")
            arg1=newtxtTab[1].lstrip("('")
            arg1=arg1.rstrip("',")
            item1=arg1
            item2=arg2

            e=(item1,item2)
            edgeLabel=str(newtxtTab[i+3])
            if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
                add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
                add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_inst_'):
                add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('instance_'):
                add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Class":
                add_Edge_Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Instance":
                add_Edge_Instance_Prolog(dotPr,e,edgeLabel)
            else:
                add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
        pos=pos+1

    prolog2graphfile.close()
    gen_prolog_graph(dotPr,path,output)


def build_Prolog_Graph_Who_CompoundProperties_Person_Action(s,WorkingDirectory,output):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10
    if output=="CONST":
        prolog2graphfile = open(path + "constraintGraph.txt", 'a+')
    elif output=="MERGE":
        prolog2graphfile = open(path + "mergePrologGraph.txt", 'a+')


    while True:
        textLine=prolog2graphfile.readline()
        while textLine=="\n":
            textLine=prolog2graphfile.readline()
        if len(textLine) == 0:
            break
        # print "textline for prolog2graphfile:",textLine
        newtxtTab=string.split(textLine,None)

        if newtxtTab[0]=="Node":
            i=1
            argNode1=newtxtTab[1]
            if argNode1.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(argNode1)
                argNode1=str(argNode1[ln1:ln2])
            while(newtxtTab[i+1]!=":"):
                argNode1=argNode1 + " " + newtxtTab[i+1]
                i=i+1
            j=i+3
            nodeLabel=str(newtxtTab[j])
            k=j+2
            argLabel=newtxtTab[k]
            while(newtxtTab[k+1]!="}"):
                argLabel=argLabel + " " + newtxtTab[k+1]
                k=k+1
            if nodeLabel.startswith('Class'):
                add_Node_Var_Class_Prolog(dotPr,argNode1,str(argLabel),pos)
            elif nodeLabel.startswith('Instance'):
                add_Node_Instance_Prolog(dotPr,argNode1,str(argLabel),pos)
            else:
                add_Node_Var_Prolog(dotPr,str(argNode1),pos)

        elif newtxtTab[0]=="Edge":
            i=2
            arg2=newtxtTab[i]
            arg2=arg2.lstrip("'")
            if arg2.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(arg2)
                arg2=str(arg2[ln1:ln2])

            while(newtxtTab[i+1]!=":"):
                arg2=arg2 + " " + str(newtxtTab[i+1])
                i=i+1
            arg2=arg2.rstrip("')")
            arg1=newtxtTab[1].lstrip("('")
            arg1=arg1.rstrip("',")
            item1=arg1
            item2=arg2

            e=(item1,item2)
            edgeLabel=str(newtxtTab[i+3])
            if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
                add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
                add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_inst_'):
                add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('instance_'):
                add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Class":
                add_Edge_Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Instance":
                add_Edge_Instance_Prolog(dotPr,e,edgeLabel)
            else:
                add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
        pos=pos+1

    prolog2graphfile.close()
    gen_prolog_graph(dotPr,path,output)



def build_Prolog_Graph_Who_Member_CompoundProperties(s,WorkingDirectory,output):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10
    if output=="CONST":
        prolog2graphfile = open(path + "constraintGraph.txt", 'a+')
    elif output=="MERGE":
        prolog2graphfile = open(path + "mergePrologGraph.txt", 'a+')


    while True:
        textLine=prolog2graphfile.readline()
        while textLine=="\n":
            textLine=prolog2graphfile.readline()
        if len(textLine) == 0:
            break
        # print "textline for prolog2graphfile:",textLine
        newtxtTab=string.split(textLine,None)

        if newtxtTab[0]=="Node":
            i=1
            argNode1=newtxtTab[1]
            if argNode1.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(argNode1)
                argNode1=str(argNode1[ln1:ln2])
            while(newtxtTab[i+1]!=":"):
                argNode1=argNode1 + " " + newtxtTab[i+1]
                i=i+1
            j=i+3
            nodeLabel=str(newtxtTab[j])
            k=j+2
            argLabel=newtxtTab[k]
            while(newtxtTab[k+1]!="}"):
                argLabel=argLabel + " " + newtxtTab[k+1]
                k=k+1
            if nodeLabel.startswith('Class'):
                add_Node_Var_Class_Prolog(dotPr,argNode1,str(argLabel),pos)
            elif nodeLabel.startswith('Instance'):
                add_Node_Instance_Prolog(dotPr,argNode1,str(argLabel),pos)
            else:
                add_Node_Var_Prolog(dotPr,str(argNode1),pos)

        elif newtxtTab[0]=="Edge":
            i=2
            arg2=newtxtTab[i]
            arg2=arg2.lstrip("'")
            if arg2.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(arg2)
                arg2=str(arg2[ln1:ln2])

            while(newtxtTab[i+1]!=":"):
                arg2=arg2 + " " + str(newtxtTab[i+1])
                i=i+1
            arg2=arg2.rstrip("')")
            arg1=newtxtTab[1].lstrip("('")
            arg1=arg1.rstrip("',")
            item1=arg1
            item2=arg2

            e=(item1,item2)
            edgeLabel=str(newtxtTab[i+3])
            if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
                add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
                add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_inst_'):
                add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('instance_'):
                add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Class":
                add_Edge_Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Instance":
                add_Edge_Instance_Prolog(dotPr,e,edgeLabel)
            else:
                add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
        pos=pos+1

    prolog2graphfile.close()
    gen_prolog_graph(dotPr,path,output)


def build_Prolog_Graph_What_Action_Properties_Status(s,WorkingDirectory,output):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10
    if output=="CONST":
        prolog2graphfile = open(path + "constraintGraph.txt", 'a+')
    elif output=="MERGE":
        prolog2graphfile = open(path + "mergePrologGraph.txt", 'a+')


    while True:
        textLine=prolog2graphfile.readline()
        while textLine=="\n":
            textLine=prolog2graphfile.readline()
        if len(textLine) == 0:
            break
        # print "textline for prolog2graphfile:",textLine
        newtxtTab=string.split(textLine,None)

        if newtxtTab[0]=="Node":
            i=1
            argNode1=newtxtTab[1]
            if argNode1.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(argNode1)
                argNode1=str(argNode1[ln1:ln2])
            while(newtxtTab[i+1]!=":"):
                argNode1=argNode1 + " " + newtxtTab[i+1]
                i=i+1
            j=i+3
            nodeLabel=str(newtxtTab[j])
            k=j+2
            argLabel=newtxtTab[k]
            while(newtxtTab[k+1]!="}"):
                argLabel=argLabel + " " + newtxtTab[k+1]
                k=k+1
            if nodeLabel.startswith('Class'):
                add_Node_Var_Class_Prolog(dotPr,argNode1,str(argLabel),pos)
            elif nodeLabel.startswith('Instance'):
                add_Node_Instance_Prolog(dotPr,argNode1,str(argLabel),pos)
            else:
                add_Node_Var_Prolog(dotPr,str(argNode1),pos)

        elif newtxtTab[0]=="Edge":
            i=2
            arg2=newtxtTab[i]
            arg2=arg2.lstrip("'")
            if arg2.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(arg2)
                arg2=str(arg2[ln1:ln2])

            while(newtxtTab[i+1]!=":"):
                arg2=arg2 + " " + str(newtxtTab[i+1])
                i=i+1
            arg2=arg2.rstrip("')")
            arg1=newtxtTab[1].lstrip("('")
            arg1=arg1.rstrip("',")
            item1=arg1
            item2=arg2

            e=(item1,item2)
            edgeLabel=str(newtxtTab[i+3])
            if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
                add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
                add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_inst_'):
                add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('instance_'):
                add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Class":
                add_Edge_Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Instance":
                add_Edge_Instance_Prolog(dotPr,e,edgeLabel)
            else:
                add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
        pos=pos+1

    prolog2graphfile.close()
    gen_prolog_graph(dotPr,path,output)


def build_Prolog_Graph(s,WorkingDirectory,output):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10
    if output=="CONST":
        prolog2graphfile = open(path + "constraintGraph.txt", 'a+')
    elif output=="MERGE":
        prolog2graphfile = open(path + "mergePrologGraph.txt", 'a+')

    while True:
        textLine=prolog2graphfile.readline()
        while textLine=="\n":
            textLine=prolog2graphfile.readline()
        if len(textLine) == 0:
            break
        # print "textline for prolog2graphfile:",textLine
        newtxtTab=string.split(textLine,None)

        if newtxtTab[0]=="Node":
            i=1
            argNode1=newtxtTab[1]
            if argNode1.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(argNode1)
                argNode1=str(argNode1[ln1:ln2])
            while(newtxtTab[i+1]!=":"):
                argNode1=argNode1 + " " + newtxtTab[i+1]
                i=i+1
            j=i+3
            nodeLabel=str(newtxtTab[j])
            k=j+2
            argLabel=newtxtTab[k]
            while(newtxtTab[k+1]!="}"):
                argLabel=argLabel + " " + newtxtTab[k+1]
                k=k+1
            if nodeLabel.startswith('Class'):
                add_Node_Var_Class_Prolog(dotPr,argNode1,str(argLabel),pos)
            elif nodeLabel.startswith('Instance'):
                add_Node_Instance_Prolog(dotPr,argNode1,str(argLabel),pos)
            else:
                add_Node_Var_Prolog(dotPr,str(argNode1),pos)

        elif newtxtTab[0]=="Edge":
            i=2
            arg2=newtxtTab[i]
            arg2=arg2.lstrip("'")
            if arg2.startswith("http://protege.stanford.edu/rdf"):
                http="http://protege.stanford.edu/rdf"
                ln1=len(http)
                ln2=len(arg2)
                arg2=str(arg2[ln1:ln2])

            while(newtxtTab[i+1]!=":"):
                arg2=arg2 + " " + str(newtxtTab[i+1])
                i=i+1
            arg2=arg2.rstrip("')")
            arg1=newtxtTab[1].lstrip("('")
            arg1=arg1.rstrip("',")
            item1=arg1
            item2=arg2

            e=(item1,item2)
            edgeLabel=str(newtxtTab[i+3])
            if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
                add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
                add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('EAT_inst_'):
                add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('Answer_'):
                add_Edge_Answer_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel.startswith('instance_'):
                add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Class":
                add_Edge_Class_Prolog(dotPr,e,edgeLabel)
            elif edgeLabel=="Instance":
                add_Edge_Instance_Prolog(dotPr,e,edgeLabel)
            else:
                add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
        pos=pos+5

    prolog2graphfile.close()
    gen_prolog_graph(dotPr,path,output)


def getItemfromValue(idx,myItem):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    if str(idx)=="Cls":
        for item,value in Qvar.boundedGraphClass.items():
            if item==myItem:
                return value
    elif str(idx)=="Inst":
        for item,value in Qvar.boundedGraphInstance.items():
            if item==myItem:
                return value


def add_Node_Var_Prolog(dotProlog,Idx,pos):
    posInt=int(pos)
    dotProlog.add_node(Idx, pos=(posInt,posInt), Var=Idx, label=Idx,color="Blue", fontsize="11" )

def add_Node_Var_Class_Prolog(dotProlog,Idx,nodeLabel,pos):
    posInt=int(pos)
    dotProlog.add_node(Idx, pos=(posInt,posInt), Var=nodeLabel, label=Idx,color="Blue", fontsize="11" )

def add_Node_Instance_Prolog(dotProlog,Idx,nodeLabel,pos):
    posInt=int(pos)
    dotProlog.add_node(Idx, pos=(posInt,posInt), Instance=nodeLabel, label=Idx,shape="box", color="Green", fontsize="10")

def add_Edge_Var2tk_Prolog(dotProlog,edge,Lbl):
    dotProlog.add_edge(*edge,Predicate=Lbl, label=Lbl, color="Red", fontsize="11")

def add_Edge_Var2Class_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Isa=Lbl, label=Lbl, color="Yellow", fontsize="11")

def add_Edge_Class_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Isa=Lbl, label=Lbl, color="Brown", fontsize="11")

def add_Edge_Var2Slot_Prolog(dotProlog,edge,Lbl):
    dotProlog.add_edge(*edge,Isa=Lbl, label=Lbl, color="Blue", fontsize="11")

def add_Edge_Var2InstanceEAT_Prolog(dotProlog,edge,Lbl):
    dotProlog.add_edge(*edge,Isa=Lbl, label=Lbl, color="Green", fontsize="11")

def add_Edge_Answer_Prolog(dotProlog,edge,Lbl):
    dotProlog.add_edge(*edge,Isa=Lbl, label=Lbl, color="Black", fontsize="12")

def add_Edge_Var2Instance_Prolog(dotProlog,edge,Lbl):
    dotProlog.add_edge(*edge,Isa=Lbl, label=Lbl, color="Brown", fontsize="11")

def add_Edge_Instance_Prolog(dotProlog,edge,Lbl):
    dotProlog.add_edge(*edge,Isa=Lbl, label=Lbl, color="Orange", fontsize="11")

def gen_prolog_graph(dotProlog,path,output):
    g=nx.DiGraph()
    if output=="CONST":
        prolog2graphfile = "constraintPrologGraph.dot"
    elif output=="MERGE":
        prolog2graphfile = "mergePrologGraph.dot"

    pos=nx.get_node_attributes(dotProlog,'pos')
    Var=nx.get_node_attributes(dotProlog,'Var')
    # Instance=nx.get_node_attributes(dot,'Instance')
    # Subclass=nx.get_node_attributes(dot,'Isa')

    print "positions are for new prolog, \n",pos
    # print "Instanece",Instance
    print "\n, Var for new prolog, \n",Var
    # print "Subclass",Subclass
    nx.draw_networkx_edge_labels(dotProlog, pos=pos)
    nx.write_dot(dotProlog,path + prolog2graphfile)
    print "All of Nodes for new prolog are:", dotProlog.nodes(data=True)
