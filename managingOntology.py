__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        managingOntology.py
#
# Author:      Majid
#
# Created:     2014/06/06
# managing ontology
#-----------------------------------------------------------------------------


def allclasses4Sentence(s,WorkingDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    pathgraph=WorkingDirectory + "graphsentence/"
    # Qvar.currentDGraph=Digraph(name='sentence',comment='Question',directory=pathgraph)

    classList={}
    classTemp={}

    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    tks=s._get_tokens()
    for itk in range(len(tks)):
        Flag=0
        tk = tks[itk]
        wrd=tk._word()
        pos=tk._pos()
        lma=tk._lemma()
        if lma=="s":
            continue
        lmas=string.lower(lma)

        if lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or \
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue
        if wrd.isupper() or wrd[0].isupper():
            lmas=wrd
            ln=1
            Flag=1
            # print "\t","this is Uppercase word", wrd, lmas
        else:
            lst_lma=lemmalist(lma)
            ln=len(lst_lma)
            i=0
            while i != ln:
                lst_lma[i]=Literal(lst_lma[i], datatype=XSD.string)
                lst_lma[i]=lst_lma[i].value
                lst_lma[i]=str(lst_lma[i])
                i=i+1
            lst_lma=list(set(lst_lma))
            # print "lemmalist is ",lst_lma
            ln=len(lst_lma)
        i=0
        j=0
        inc=0
        while j != ln:

            if Flag!=1:
                lmas=lst_lma[j]

            if Flag!=1:
                qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .

                    FILTER (CONTAINS ( LCASE( str(?varClass)), '"""+lmas+"""'))

                }""")
            else:
                qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  DISTINCT ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class .
                    ?varProperty rdf:type ?propertyType ;
                                 rdfs:domain ?varClass .

                    FILTER (CONTAINS ( str(?varClass), '"""+lmas+"""'))

                }""")

            i=0
            for row in qClass.result:
                # if i==0:
                #     print "The result of CLASS for Token:",itk, lmas, "(",wrd, ") are:----------------","\n"
                ji=""
                seq1=str(j),str(i)
                ji=ji.join(seq1)
                intji=int(ji)
                classTemp[itk,intji]=str(row)
                classTemp[itk,intji]=classTemp[itk,intji].split()
                classTemp[itk,intji][0]=classTemp[itk,intji][0].rsplit('/rdf')[-1]
                classTemp[itk,intji][1]=classTemp[itk,intji][1].rsplit('/rdf')[-1]

                classTemp[itk,intji][0]=classTemp[itk,intji][0].rstrip("'),)")
                classTemp[itk,intji][1]=classTemp[itk,intji][1].rstrip("'),)")

                pure_name=pure_class_name(classTemp[itk,intji][0])
                # print "Before separation",classTemp[itk,intji][0]
                # print "Pure name class",pure_name
                if Flag!=1:
                    # print "Lemma: ",lmas, "Class [",itk,"][",i,"]",classTemp[itk,intji], "\t"," LEVENSHTEIN for class :",'%.2f' % percent_diff(lmas,string.lower(pure_name)), "\n"
                    cls_Threshold=percent_diff(lmas,string.lower(pure_name))
                else:
                    # print "Lemma: ",lmas, "Class [",itk,"][",i,"]",classTemp[itk,intji], "\t"," LEVENSHTEIN for class :",'%.2f' % percent_diff(lmas,string.lower(pure_name)), "\n"
                    cls_Threshold=percent_diff(lmas,pure_name)
                if cls_Threshold > 0.75:
                    classList[itk,intji]=classTemp[itk,intji]
                    classList[itk,intji][0]=classTemp[itk,intji][0]

                    if Qvar.addBoundedClass(classList[itk,intji][0],str(itk),intji):
                        add_Cls_Graph(Qvar,classList,itk,intji)
                        i=i+1
            # print "NO. of Classes for Lemma:",lmas,"is:", j
            j=j+1
    # Qvar.describeBoundedOntology()



def classes4Sentence(s,WorkingDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    pathgraph=WorkingDirectory + "graphsentence/"

    propList={}
    propTemp={}

    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    tks=s._get_tokens()

    for itk in range(len(tks)):
        Flag=0
        tk = tks[itk]
        wrd=tk._word()
        pos=tk._pos()
        lma=tk._lemma()
        if lma=="s":
            continue
        lmas=string.lower(lma)
        if wrd.isupper() or wrd[0].isupper():
            lmas=wrd
            Flag=1
            # print "\t","this is Uppercase word", wrd, lmas

        if lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue
        if Flag!=1:
            qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .
                FILTER (CONTAINS ( LCASE( str(?varClass)), '"""+lmas+"""'))

            }""")
        else:
            qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT   ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .
                FILTER (CONTAINS ( str(?varClass), '"""+lmas+"""'))

            }""")

        i=0
        for row in qClass.result:
            # if i==0:
            #     print "The result of CLASS with SLOTS  for Token:",itk, lmas, "(",wrd, ") are:----------------","\n"
            propList[itk,i]=str(row)
            propTemp[itk,i]=propList[itk,i].split()
            Qvar.boundedSlot[itk,i]=propTemp[itk,i]

            propTemp[itk,i][0]=propTemp[itk,i][0].rsplit('/rdf')[-1]
            propTemp[itk,i][1]=propTemp[itk,i][1].rsplit('/rdf')[-1]

            propTemp[itk,i][0]=propTemp[itk,i][0].rstrip("'),)")
            propTemp[itk,i][1]=propTemp[itk,i][1].rstrip("'),)")

            pure_name=pure_slot_name(propTemp[itk,i][1])
            # print "Before separation",propTemp[itk,i][1]
            # print "Pure name Slot",pure_name

            if Flag!=1:
                # print "Lemma: ",lmas, "SLOT [",itk,"][",i,"]",propTemp[itk,i][1]," CLass Name:",Qvar.boundedSlot[itk,i][0], "\t"," LEVENSHTEIN for class :",'%.2f' % percent_diff(lmas,string.lower(propTemp[itk,i][0])), "\n", " LEVENSHTEIN for Slot :" ,'%.2f' % percent_diff(lmas,string.lower(pure_name)), "\n"
                slot_Threshold=percent_diff(lmas,string.lower(pure_name))

            else:
                # print "Lemma: ",lmas, "SLOT [",itk,"][",i,"]",propTemp[itk,i][1]," CLass Name:",Qvar.boundedSlot[itk,i][0], "\t"," LEVENSHTEIN for class :",'%.2f' % percent_diff(lmas,string.lower(propTemp[itk,i][0])), "\n", " LEVENSHTEIN for Slot :" ,'%.2f' % percent_diff(lmas,pure_name), "\n"
                slot_Threshold=percent_diff(lmas,pure_name)

            if slot_Threshold > 0.45:
                # print "Accept Threshold for Slot:",propTemp[itk,i][1],pure_name, slot_Threshold

                Qvar.boundedSlot[itk,i][0]=propTemp[itk,i][0]
                Qvar.boundedSlot[itk,i][1]=propTemp[itk,i][1]
                i=i+1

        # print "NO. of Properties for Lemma:",lmas,"is:", i



def allinstances4Sentence(s,WorkingDirectory):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    pathgraph=WorkingDirectory + "graphsentence/"

    instanceList={}
    instanceTemp={}
    classTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    tks=s._get_tokens()
    for itk in range(len(tks)):
        Flag=0
        itemdig=""
        seq1=str(itk)
        itemdig=itemdig.join(seq1)
        intitem=int(itemdig)

        tk = tks[itk]
        wrd=tk._word()
        pos=tk._pos()
        lma=tk._lemma()
        if lma=="s":
            continue
        lmas=string.lower(lma)
        if wrd.isupper() or wrd[0].isupper():
            lmas=wrd
            Flag=1
            # print "\t","This is Uppercase word", wrd, lmas

        if lmas=="be" or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue
        if Flag!=1:

            qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?class ?property ?instance
            WHERE  {
                ?a ?property   ?instance ;
                   rdf:type ?class .
                FILTER (CONTAINS ( LCASE(str(?instance)), '"""+lmas+"""'))

            }""")
        else:
            qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  Distinct ?class ?property ?instance
            WHERE  {
                ?a ?property   ?instance ;
                   rdf:type ?class .
                FILTER (CONTAINS ( str(?instance), '"""+lmas+"""'))

            }""")

        i=0
        for row in qSubClass:
            instanceList[itk,i]=str(row)
            instanceTemp[itk,i]=instanceList[itk,i].split('),')
            strTemp=str(instanceTemp[itk,i])
            if (strTemp.find("rdf-schema#label")!=-1) or (strTemp.find("#type")!=-1) :
                continue
            # if i==0:
            #     print "The result of INSTANCES  with SPARQL for Token:",itk, "(",wrd, ") are: *****************","\n"

            instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rsplit('/rdf')[-1]
            instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rsplit('/rdf')[-1]
            instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u'")[-1]
            instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rsplit("(u")[-1]

            instanceTemp[itk,i][0]=instanceTemp[itk,i][0].rstrip("'),)")
            instanceTemp[itk,i][1]=instanceTemp[itk,i][1].rstrip("'),)")
            instanceTemp[itk,i][2]=instanceTemp[itk,i][2].rstrip("'),)")
            if Flag!=1:
                # print "  Instance[",itk,"][",i,"]",instanceTemp[itk,i][0],"\t",instanceTemp[itk,i][1],"\t",instanceTemp[itk,i][2]
                # print "\t"," Class LEVENSHTEIN :",'%.2f' % percent_diff(lmas,string.lower(instanceTemp[itk,i][0])),"\t"," Slot LEVENSHTEIN :",'%.2f' % percent_diff(lmas,string.lower(instanceTemp[itk,i][1])),"\t"," Instance LEVENSHTEIN :",'%.2f' % percent_diff(lmas,string.lower(instanceTemp[itk,i][2])),"\n"
                ins_Threshold=percent_diff(lmas,string.lower(instanceTemp[itk,i][2]))
            else:
                # print "  Instance[",itk,"][",i,"]",instanceTemp[itk,i][0],"\t",instanceTemp[itk,i][1],"\t",instanceTemp[itk,i][2]
                # print "\t"," Class LEVENSHTEIN :",'%.2f' % percent_diff(lmas,instanceTemp[itk,i][0]), "\t"," Slot LEVENSHTEIN :",'%.2f' % percent_diff(lmas,instanceTemp[itk,i][1]),"\t"," Instance LEVENSHTEIN :",'%.2f' % percent_diff(lmas,instanceTemp[itk,i][2]),"\n"
                ins_Threshold=percent_diff(lmas,instanceTemp[itk,i][2])

            if ins_Threshold >= 0.30:
                print "ins_Threshold >= 0.30:  before if",instanceTemp[itk,i], ins_Threshold
                classTemp[intitem,i]=instanceTemp[itk,i]
                classTemp[intitem,i][0]=instanceTemp[itk,i][0]
                classTemp[intitem,i][1]=instanceTemp[itk,i][1]

                if Qvar.addBoundedInstance(instanceTemp[itk,i],itk,i):
                    # print "ins_Threshold >= 0.30:  After if",instanceTemp[itk,i],itk,i
                    if Qvar.addBoundedClass(classTemp[intitem,i][0],str("I")+ str(intitem),i):
                        add_Cls_Graph(Qvar,classTemp,intitem,i)
                    # if Qvar.addBoundedClass(classTemp[intitem,i][1],str("S")+ str(intitem),i):
                    #     add_Cls_Graph(Qvar,classTemp,intitem,i)

                    add_Ins_Graph(Qvar,instanceTemp,itk,i)
                    i=i+1

            elif 0.1 < ins_Threshold < 0.30:
                classTemp[intitem,i]=instanceTemp[itk,i]
                classTemp[intitem,i][0]=instanceTemp[itk,i][0]
                print "0.1 < ins_Threshold < 0.30:  Before if",classTemp[intitem,i], ins_Threshold
                if Qvar.addBoundedClass(classTemp[intitem,i][0],str("I")+ str(intitem),i):
                    # print "0.1 < ins_Threshold < 0.30:  After if:  classTemp[itk,i],itk,i,intitem",classTemp[intitem,i],itk,i,intitem
                    add_Cls_Graph(Qvar,classTemp,intitem,i)
                    i=i+1

        # print "NO. of INSTANCES for Token:",itk,"is:", i
    dot=Qvar.currentDGraph
    gen_graph(dot,pathgraph)
    Qvar.describeBoundedOntology()



def class4Instance(s,WorkingDirectory):
    global currentRule
    QvarTemp={}
    from rule import currentRule
    Qvar=currentRule
    # graph = Graph(Qvar.currentGraph)

    Qvar=currentRule
    QvarTemp=Qvar.boundedInstance
    instanceList={}
    instanceTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdf"
    g = rdflib.Graph()
    g.parse(path)
    tks=s._get_tokens()
    Flag=0
    for item in QvarTemp.keys():
        # print "Item for calss  Bunded are;",item,"\t", QvarTemp[item][0],QvarTemp[item][1]
        instanceNo=str(QvarTemp[item][0])
        instance=str(QvarTemp[item][1])
        qSubClass = g.query("""
                    PREFIX ot: <http://www.opentox.org/api/1.1#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    SELECT ?className ?varslbl ?slotNo
                    WHERE  {
                        ?varclass rdf:type  ?className ;
                                  rdfs:label ?varslbl .
                        ?slotNo rdfs:label ?slotlb .
                        FILTER (CONTAINS ( str(?slotNo), '"""+instanceNo+"""') && CONTAINS(str(?varslbl), '"""+instance+"""'))

                    }""")
                                                            # rdf:about="""+instanceNo+""" .

                                # rdf:about """+instanceNo+""" .
                        # FILTER (CONTAINS ( str(?varslot), '"""+instance+"""'))
                        #         rdfs:label="""+instance+""" ;
                        #         rdf:about  ?varslot .
        i=0
        for row in qSubClass:
            # if i==0:
            #     print "The result of Class  for Instance:",instance, " are: *****************","\n"
            instanceList[i]=str(row)
            # print "New Class : ",instanceList[i]
            # instanceTemp[i]=instanceList[i].split('),')
            # Qvar.boundedInstance[item]=instanceTemp[i]
            # instanceTemp[i][0]=instanceTemp[i][0].rsplit('/rdf')[-1]
            # instanceTemp[i][1]=instanceTemp[i][1].rsplit("(u'")[-1]
            #
            # instanceTemp[i][0]=instanceTemp[i][0].rstrip("'),)")
            # instanceTemp[i][1]=instanceTemp[i][1].rstrip("'),)")
            #
            # Qvar.boundedClassInstance[item][0]=instanceTemp[i][0]
            # Qvar.boundedClassInstance[item][1]=instanceTemp[i][1]
            # print "Class of Instance",instance, Qvar.boundedClassInstance[item][0],Qvar.boundedClassInstance[item][1]
            # graph.add_edge_instance_of(slot,instanceTemp[i][1])
            i=i+1

        # print "NO. of Class for Instance:",instance,"is:", i


def add_Cls_Graph(Qvar,classGTemp,itk,i):

    str1=""
    seq=(str('C'),str(itk),str(i))
    str2=str1.join(seq)
    # print "\t","Bounded classTemp,classTemp[itk,i],itk,i,str2",classTemp[itk,i][0],itk,i,str2

    add_Node_Class(Qvar.currentDGraph,str2,classGTemp[itk,i][0])


def add_SubClass_Graph(Qvar,subClassTemp,itemG,i):

    # print "\t","Bounded",subClassTemp

    strCls=""
    strsubCls=""
    seqCls=(str('C'),str(itemG))
    seqsubCls=(str('CC'),str(itemG),str(i))
    strCls2=strCls.join(seqCls)
    strsubCls2=strsubCls.join(seqsubCls)
    print "strCls2, strsubCls2,subClassTemp[itemG,i][0]",strCls2, strsubCls2,subClassTemp[itemG,i][0]
    add_Node_Class(Qvar.currentDGraph,strsubCls2,subClassTemp[itemG,i][0])
    add_Node_Class(Qvar.currentDGraph,strCls2,subClassTemp[itemG,i][1])

    e=(strCls2,strsubCls2)
    print "\n Class ------> Sub Class:",e
    add_Edge_Class2Class(Qvar.currentDGraph,e,"Isa")

def add_Ins_Graph(Qvar,instanceTemp,itk,i):

    strCls=""
    strClsIns=""
    strSlot=""
    strIns=""
    seqCls=(str('C'),str(itk),str(i))
    seqClsIns=(str('CI'),str(itk),str(i))
    seqSlot=(str('S'),str(itk),str(i))
    seqIns=(str('I'),str(itk),str(i))
    strCls2=strCls.join(seqCls)
    strClsIns2=strClsIns.join(seqClsIns)

    strIns2=strIns.join(seqIns)
    addedC=0
    addedCL=0
    addedClIns=0
    addedIns=0

    clsExist=0
    lblClsExist=0
    lblClsInsExist=0

    lblname=""
    cls=nx.get_node_attributes(Qvar.currentDGraph,'Class')
    for lbl in cls:
        # print "Label",lbl
        if cls[lbl]==instanceTemp[itk,i][0]:
            # print "was found Class in Instance!!!!", instanceTemp[itk,i][0],cls[lbl]
            clsExist=1
            if str(lbl)==str(strCls2):
                lblClsExist=1
                lblname=lbl
            elif str(lbl)==str(strClsIns2):
                lblClsInsExist=1
                lblname=lbl

            else:
                # print "Exception: lbl, lblClsExist,lblClsInsExist, lblSubClsExist...",lbl,lblClsExist,lblClsInsExist
                # print "Another class strCls2,strClsIns2,strSubCls2 .", strCls2,strClsIns2,
                strClsIns2=lbl
                lblClsInsExist=1
                lblname=lbl


    insExist=0
    ins=nx.get_node_attributes(Qvar.currentDGraph,'Instance')
    for lbl in ins:
        # print "Label",lbl
        if ins[lbl]==Qvar.boundedInstance[itk,i][2]:
            # print "was found Instance!!!!", instanceTemp[itk,i][2],ins[lbl]
            insExist=1
            strIns2=lbl

    if clsExist!=1 :
        # print "Label class or sub class is not Exist !!!",lblname
        add_Node_Class(Qvar.currentDGraph,strClsIns2,instanceTemp[itk,i][0])
        addedClIns=1
    if lblClsExist==1 :
        # print "Label class or sub class Exist with format C, CC... !!!",lblname
        add_Node_Class(Qvar.currentDGraph,strClsIns2,instanceTemp[itk,i][0])
        addedClIns=1
        remove_Node_Class(Qvar.currentDGraph,lblname)

    # if lblClsInsExist==1:
        # print "Label class Exist with format CIII... !!!",lblname


    if insExist!=1:
        add_Node_Instance(Qvar.currentDGraph,strIns2,instanceTemp[itk,i][2])

    if addedClIns==1 and insExist!=1:
        e=(strClsIns2,strIns2)
        add_Edge_Class2Inst(Qvar.currentDGraph,e,instanceTemp[itk,i][1])

    if lblClsInsExist==1:
        e=(strClsIns2,strIns2)
        add_Edge_Class2Inst(Qvar.currentDGraph,e,instanceTemp[itk,i][1])


def pure_class_name(class_name):
    try:
        cls_name=str(class_name)
    except:
        # print "is not formal string!!!",
        return class_name

    if cls_name.startswith("i_en_proper_"):
        # print "Split  i_en_proper_:",cls_name.split("i_en_proper_",1)
        cls_name=cls_name.split("i_en_proper_",1)
        return cls_name[1]
    elif cls_name.startswith("i_en_"):
        # print "Split i_en:",cls_name.split("i_en_",1)
        cls_name=cls_name.split("i_en_",1)
        return cls_name[1]
    else:
        return class_name



def pure_slot_name(slot_name):
    slt_name=str(slot_name)
    if slt_name.endswith("_name"):
        # print "Split  _name:",slt_name.split("_name",1)
        slt_name=slt_name.split("_name",1)
        return slt_name[0]
    elif slt_name.endswith("_title"):
        # print "Split _title:",slt_name.split("_title",1)
        slt_name=slt_name.split("_title")
        return slt_name[0]
    elif slt_name.startswith("has_"):
        # print "Split has_:",slt_name.split("has_",1)
        slt_name=slt_name.split("has_")
        return slt_name[1]
    elif slt_name.endswith("_for"):
        # print "Split  _for:",slt_name.split("_for",1)
        slt_name=slt_name.split("_for",1)
        return slt_name[0]
    elif slt_name.startswith("Org_"):
        # print "Split  Org_:",slt_name.split("_for",1)
        slt_name=slt_name.split("_for",1)
        return slt_name[0]

    else:
        return slot_name



def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]


def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings."""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
       distance_matrix[i][0] = i
    for j in range(second_length):
       distance_matrix[0][j]=j
    for i in xrange(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]

def percent_diff(first, second):
    return (100-(100 * levenshtein_distance(first, second) / float(max(len(first), len(second)))))/100


