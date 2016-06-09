__author__ = 'majid'
# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        graph.py
#
# Author:      Majid
#
# Created:     2014/12/16
# Creating Graph for Question
#------------------------------------------------------------------------

from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt
import numpy



def add_Node_Class(dot,Idx,Label):
    # print "Class: Idx,Label",Idx,Label
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "generalGraph.txt", 'a+')
    print "\n Node: Class:  ",Idx,Label
    duplicate=0
    pos1=Idx.strip('S')
    pos1=pos1.strip('C')
    pos1=pos1.strip('I')
    pos1=pos1.strip('C')
    pos=pos1.strip('S')
    posInt=int(pos)

    # print "\n Node: Class:  ",Idx,Label,posInt
    # dot.add_node(Idx,pos=(posInt,posInt), Class=Label, label=Label,color="Blue", fontsize="11" )
    classText="Node" + "\t" + Label + "\t:\t" + "{" + "\t" + "Class :" + "\t" + Idx + "\t" + "}"
    classIdx="Node" + "\t" + Idx + "\t:\t" + "{" + "\t" + "ClsIdx :" + "\t" + Idx + "\t" + "}"
    e=(Idx,Label)
    edgeCls="Edge" + "\t" + str(e) + "\t:\t" + "{" + "\t" + "Class" + "\t"+ "}"
    while True:
        textLine=graph2prologfile.readline()
        while textLine=="\n":
            textLine=graph2prologfile.readline()
        if len(textLine) == 0:
            break
        textLine=textLine.rstrip("\n")
        # print "textLine : classText",textLine,classText
        if str(textLine) == str(classText) or str(textLine) == str(classIdx) or str(textLine) == str(edgeCls):
            print "find duplicate class:, textLine,classText, classIdx, edgeCls : ",textLine + "\n" + classText + "\n" + classIdx + "\n" + edgeCls
            duplicate=1
            break
    position = graph2prologfile.tell()
    position = graph2prologfile.seek(0, 2)
    if duplicate!=1:
        graph2prologfile.write(classText)
        graph2prologfile.write("\n")
        graph2prologfile.write(classIdx)
        graph2prologfile.write("\n")
        graph2prologfile.write(edgeCls)
        graph2prologfile.write("\n")

    graph2prologfile.close()


def add_Node_Instance(dot,Idx,Label):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "generalGraph.txt", 'a+')

    pos=Idx.strip('I')
    posInt=int(pos)*150
    # print "\n Node : Instance  ",Idx,Label
    # dot.add_node(Idx,pos=(posInt,posInt), Instance=Label, label=Label,shape="box", color="Green", fontsize="10")
    instanceText="Node" + "\t" + Label + "\t:\t" + "{" + "\t" + "Instance :" + "\t" + Idx + "\t" + "}"
    instanceIdx="Node" + "\t" + Idx + "\t:\t" + "{" + "\t" + "InsIdx :" + "\t" + Idx + "\t" + "}"
    e=(Idx,Label)
    edgeIns="Edge" + "\t" + str(e) + "\t:\t" + "{" + "\t" + "Instance" + "\t"+ "}"

    graph2prologfile.write(instanceText)
    graph2prologfile.write("\n")
    graph2prologfile.write(instanceIdx)
    graph2prologfile.write("\n")
    graph2prologfile.write(edgeIns)
    graph2prologfile.write("\n")

    graph2prologfile.close()


def add_Edge_Slot(dot,src,dest):
    print "\n Edge: Slot: source,destination",src,dest
    dot.add_edge(src, dest, 'link Slot')

def add_Edge_Class2Inst(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "generalGraph.txt", 'a+')

    # print "\n Edge: Class ----> Instance: source,destination",edge
    # dot.add_edge(*edge,Slot=Lbl, label=Lbl, color="Red", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + Lbl + "\t"+ "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()

def add_Edge_Class2Class(dot,edge,Lbl):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    path=Qvar.workingDir + "graphsentence/"
    graph2prologfile = open(path + "generalGraph.txt", 'a+')

    # graph2prologfile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\data\graphsentence\constraintGraph.txt", 'a+')
    # print "\n Edge: Class ----> Class: source,destination",edge
    # dot.add_edge(*edge,Isa=Lbl, label=Lbl, color="Yellow", fontsize="11")
    classText="Edge" + "\t" + str(edge) + "\t:\t" + "{" + "\t" + Lbl + "\t"+ "}"
    graph2prologfile.write(classText)
    graph2prologfile.write("\n")
    graph2prologfile.close()


def remove_Node_Class(dot,Idx):
    dot.remove_node(Idx)
    # print " Class was removed",Idx


def gen_graph(dot,path):
    g=nx.DiGraph()
    pos=nx.get_node_attributes(dot,'pos')
    Class=nx.get_node_attributes(dot,'Class')
    Instance=nx.get_node_attributes(dot,'Instance')
    Subclass=nx.get_node_attributes(dot,'Isa')

    print "\n positions are",pos
    print "\n Instanece",Instance
    print "\n Class",Class
    print "\n Subclass",Subclass
    nx.draw_networkx_edge_labels(dot,pos=pos)
    nx.write_dot(dot,path + 'generalOntology.dot')
    # print "All of Nodes are:","\n",dot.nodes()
    # for (u,d) in dot.nodes(data=True):
    #     print "\n Node ",u,":  ",d
    #     # print "Neighbors of:",u, dot.neighbors(u)
    #
    # print "All of Edges are:","\n", dot.edges()
    # for (u,v,d) in dot.edges(data=True):
    #     print "\n Edge: ",u, "--------->",v,":  ",d
    #


    # nx.draw(dot)
    # plt.savefig(path + "path.png")
    # plt.savefig(path + "question.pdf")

    # nx.draw_networkx_nodes(dot,pos=pos,label=True)
    # nx.draw_networkx(dot,pos=pos,with_labels=True,)

    # nx.draw_networkx_labels(dot,pos=pos,labels=Instance)

    # nx.draw_graphviz(dot)

    # plt.show()
    # print "One Node:",dot.node['60']
    # plt.savefig(path + "question.pdf")
    # dot1=dot
    # print(dot1.source)
    # dot1.render('sentence.gv')
    # print"Grapgh is: ",dot.graph
    # eps, pdf, pgf, png, ps, raw, rgba, svg, svgz.