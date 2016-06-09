__author__ = 'majid'
# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        mergePrologGraph.py
#
# Author:      Majid
#
# Created:     2016/01/01
# Creating merged Graph in Prolog text file
#------------------------------------------------------------------------

from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import string



def mergeGenreal_ConstraintPrologGraph(s,WorkingDirectory):
    tup1 = ""
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    dotPr=Qvar.currentPrologDGraph
    path=WorkingDirectory + "graphsentence/"
    pos=10

    generalGraphfile = open(path + "generalGraph.txt", 'r')
    constraintGraphfile = open(path + "constraintGraph.txt", 'r')
    mergeGraphfile = open(path + "mergePrologGraph.txt", 'a+')
    ln=0
    while True:
        textLine=constraintGraphfile.readline()
        while textLine=="\n":
            textLine=constraintGraphfile.readline()
        if len(textLine) == 0:
            break
        mergeGraphfile.write(textLine)
        ln=ln+1
    print "No. of line was written in mergeGraphfile by constraintGraphfile: \n",ln
    ln=0
    while True:
        textLine=generalGraphfile.readline()
        while textLine=="\n":
            textLine=generalGraphfile.readline()
        if len(textLine) == 0:
            break
        mergeGraphfile.write(textLine)
        ln=ln+1
    print "No. of line was written in mergeGraphfile by generalGraphfile: \n",ln
    generalGraphfile.close()
    constraintGraphfile.close()
    mergeGraphfile.close()

# def drawPrologGraph():
#     global currentRule
#     from rule import currentRule
#     Qvar=currentRule
#     dotPr=Qvar.currentPrologDGraph
#     path=Qvar.workingDir + "graphsentence/"
#     pos=10
#
#     mergeGraphfile = open(path + "mergePrologGraph.txt", 'r')
#
#     while True:
#         textLine=mergeGraphfile.readline()
#         while textLine=="\n":
#             textLine=mergeGraphfile.readline()
#         if len(textLine) == 0:
#             break
#         newtxtTab=string.split(textLine,None)
#
#         if newtxtTab[0]=="Node":
#             i=1
#             argNode1=newtxtTab[1]
#             while(newtxtTab[i+1]!=":"):
#                 argNode1=argNode1 + " " + newtxtTab[i+1]
#                 i=i+1
#             j=i+3
#             nodeLabel=str(newtxtTab[j])
#             k=j+2
#             argLabel=newtxtTab[k]
#             while(newtxtTab[k+1]!="}"):
#                 argLabel=argLabel + " " + newtxtTab[k+1]
#                 k=k+1
#
#             if nodeLabel.startswith('Class'):
#                 # print "start with Class",argLabel
#                 Qvar.boundedGraphClass[argLabel] = str(argNode1)
#                 add_Node_Var_Class_Prolog(dotPr,str(argLabel),argNode1,pos)
#             elif nodeLabel.startswith('Instance'):
#                 # print "start with Instance",argLabel
#                 Qvar.boundedGraphInstance[argLabel] = str(argNode1)
#                 add_Node_Instance_Prolog(dotPr,str(argLabel),argNode1,pos)
#             else:
#                 add_Node_Var_Prolog(dotPr,str(argNode1),pos)
#
#         elif newtxtTab[0]=="Edge":
#             i=2
#             arg2=newtxtTab[i]
#             arg2=arg2.lstrip("'")
#             while(newtxtTab[i+1]!=":"):
#                 arg2=arg2 + " " + str(newtxtTab[i+1])
#                 i=i+1
#             arg2=arg2.rstrip("')")
#             # print "arg2 after concatinating and strip: ",arg2
#             arg1=newtxtTab[1].lstrip("('")
#             arg1=arg1.rstrip("',")
#             item1=arg1
#             item2=arg2
#             print "arg1 after strip",arg1
#             if arg1 in Qvar.boundedGraphClass.keys():
#                 print "arg1:  Founded in dictionary class", arg1
#                 item1=getItemfromValue("Cls",arg1)
#                 print "returned item for value is : ",item1, arg1
#             elif arg1 in Qvar.boundedGraphInstance.keys():
#                 print "Founded in dictionary instance", arg1
#                 item1=getItemfromValue("Inst",arg1)
#                 print "arg1 :returned item for value is : ",item1, arg1
#
#             if arg2 in Qvar.boundedGraphClass.keys():
#                 print "arg2 : Founded in dictionary class", arg2
#                 item2=getItemfromValue("Cls",arg2)
#                 print "returned item for value is : ",item2, arg2
#             elif arg2 in Qvar.boundedGraphInstance.keys():
#                 print "Founded in dictionary instance", arg2
#                 item2=getItemfromValue("Inst",arg2)
#                 print "arg2 : returned item for value is : ",item2, arg2
#
#             e=(item1,item2)
#             edgeLabel=str(newtxtTab[i+3])
#             if edgeLabel.startswith('EAT_class_') or edgeLabel.startswith('class_'):
#                 add_Edge_Var2Class_Prolog(dotPr,e,edgeLabel)
#             elif edgeLabel.startswith('EAT_slot_') or edgeLabel.startswith('slot_'):
#                 add_Edge_Var2Slot_Prolog(dotPr,e,edgeLabel)
#             elif edgeLabel.startswith('EAT_inst_'):
#                 add_Edge_Var2InstanceEAT_Prolog(dotPr,e,edgeLabel)
#             elif edgeLabel.startswith('instance_'):
#                 add_Edge_Var2Instance_Prolog(dotPr,e,edgeLabel)
#             else:
#                 add_Edge_Var2tk_Prolog(dotPr,e,edgeLabel)
#         elif newtxtTab[0]=="EAT":
#             continue
#         pos=pos+1
#
#     print "Qvar.boundedGraphClass.values() after for edge, \n",Qvar.boundedGraphClass.values()
#     print "Qvar.boundedGraphClass.Items() for edge, \n",Qvar.boundedGraphClass.items()
#     print "Qvar.boundedGraphInstance.Items() after for edge, \n",Qvar.boundedGraphInstance.items()
#     print "Qvar.boundedClass.Keys() after for edge, \n",Qvar.boundedClass.values()
#
#     # prolog2graphfile.write(classText)
#     # prolog2graphfile.write("\n")
#     mergeGraphfile.close()
#     gen_prolog_graph(dotPr,path)


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


def add_Node_Var_Prolog(dotPr,Idx,pos):
    posInt=int(pos)
    dotPr.add_node(Idx, pos=(posInt,posInt), Var=Idx, label=Idx,color="Blue", fontsize="11" )

def add_Node_Var_Class_Prolog(dotPr,Idx,nodeLabel,pos):
    posInt=int(pos)
    dotPr.add_node(Idx, pos=(posInt,posInt), Var=Idx, label=nodeLabel,color="Blue", fontsize="11" )

def add_Node_Instance_Prolog(dotPr,Idx,nodeLabel,pos):
    posInt=int(pos)
    dotPr.add_node(Idx, pos=(posInt,posInt), Instance=Idx, label=nodeLabel,shape="box", color="Green", fontsize="10")

def add_Edge_Var2tk_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Predicate=Lbl, label=Lbl, color="Red", fontsize="11")

def add_Edge_Var2Class_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Isa=Lbl, label=Lbl, color="Yellow", fontsize="11")

def add_Edge_Var2Slot_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Isa=Lbl, label=Lbl, color="Blue", fontsize="11")

def add_Edge_Var2InstanceEAT_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Isa=Lbl, label=Lbl, color="Green", fontsize="11")

def add_Edge_Var2Instance_Prolog(dotPr,edge,Lbl):
    dotPr.add_edge(*edge,Isa=Lbl, label=Lbl, color="Brown", fontsize="11")

def gen_prolog_graph(dotProlog,path):
    g=nx.DiGraph()
    pos=nx.get_node_attributes(dotProlog,'pos')
    Var=nx.get_node_attributes(dotProlog,'Var')
    # Instance=nx.get_node_attributes(dot,'Instance')
    # Subclass=nx.get_node_attributes(dot,'Isa')

    print "positions are for new prolog, \n",pos
    # print "Instanece",Instance
    print "\n, Var for new prolog, \n",Var
    # print "Subclass",Subclass
    nx.draw_networkx_edge_labels(dotProlog, pos=pos)
    nx.write_dot(dotProlog,path + 'prolog2graph.dot')
    print "All of Nodes for new prolog are:", dotProlog.nodes(data=True)
