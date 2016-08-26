__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        Recursive_SPARQL_Person.py
#
# Author:      Majid
#
# Created:     2015/02/07
# Recursive SPARQL to detect Person Entity
#-----------------------------------------------------------------------------



def retrieveClassPerson(WorkingDirectory,startLOC,lma_Loc,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule

    classList={}
    classTemp={}

    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    inttk=int(tk)
    sLOC=str(startLOC)
    print "Location class started", sLOC
    qClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?varClass ?varProperty
            WHERE  {
                ?varClass rdf:type rdfs:Class .
                ?varProperty rdf:type ?propertyType ;
                             rdfs:domain ?varClass .

                FILTER (CONTAINS ( str(?varClass), '"""+sLOC+"""'))

            }""")


    i=0
    for row in qClass.result:
        if i==0:
            print "The result of CLASS for Startclass:",sLOC, ") are:----------------","\n"
        classTemp[inttk,i]=str(row)
        classTemp[inttk,i]=classTemp[inttk,i].split()
        classTemp[inttk,i][0]=classTemp[inttk,i][0].rsplit('/rdf')[-1]
        classTemp[inttk,i][1]=classTemp[inttk,i][1].rsplit('/rdf')[-1]

        classTemp[inttk,i][0]=classTemp[inttk,i][0].rstrip("'),)")
        classTemp[inttk,i][1]=classTemp[inttk,i][1].rstrip("'),)")

        pure_name=pure_class_name(classTemp[inttk,i][0])
        print "Before separation",classTemp[inttk,i][0]
        print "Pure name class",pure_name

        if Qvar.addBoundedClassPerson(classList[inttk,i],i):
            retrieveSubclassesPerson(WorkingDirectory,classTemp[inttk,i][0],lma_Loc,tk)
        i=i+1

    print "NO. of Classes for start class:",sLOC,"is:", i



def retrieveSubclassesPerson(WorkingDirectory,subClassPerson,subLOC,tk):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassList={}
    classListTemp={}
    subClassTemp={}
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    recLOC=str(subLOC)
    itemdig=""
    itemdig=str(tk)
    intitem=int(itemdig)
    classt=string.lower(subClassPerson)
    lenclasst=len(classt)

    print "Location class started and in tk", recLOC,classt,subClassPerson,lenclasst
    Flag=0

    qSubClass = g.query("""
            PREFIX ot: <http://www.opentox.org/api/1.1#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?varClass ?subclass
            WHERE  {
                ?subclass  rdfs:subClassOf ?varClass.
                FILTER ( CONTAINS( LCASE( str(?varClass)), '"""+classt+"""'))

            }""")

    i=0
    for row in qSubClass:
        subClassList[intitem,i]=str(row)
        subClassTemp[intitem,i]=subClassList[intitem,i].split()

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rsplit('/rdf')[-1]
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rsplit('/rdf')[-1]

        subClassTemp[intitem,i][0]=subClassTemp[intitem,i][0].rstrip("'),)")
        subClassTemp[intitem,i][1]=subClassTemp[intitem,i][1].rstrip("'),)")
        if (string.find(pure_class_name(subClassTemp[intitem,i][1]),subLOC)==0):
            if Qvar.addBoundedSubClassPerson(subClassTemp[intitem,i],subClassTemp[intitem,i][0],subClassTemp[intitem,i][1],intitem,i):
                print "OK!!,  Person FOUND  Class[",intitem,"][",i,"]",subClassTemp[intitem,i][0],subClassTemp[intitem,i],"has Subclass:",subClassTemp[intitem,i][1]
                Qvar.addBoundedClassPerson(subClassTemp[intitem,i][1],intitem,i)
            Flag=1

            # if retrieveSlotsPerson(WorkingDirectory,slotLOC,item0,item1,loc)
        else:
            subitemdig=""
            seq1=str(intitem),str(i)
            subitemdig=subitemdig.join(seq1)
            subitemdig=int(subitemdig)
            if retrieveSubclassesPerson(WorkingDirectory,subClassTemp[intitem,i][1],recLOC,subitemdig):
                Flag=1
        i=i+1
    print "NO. of SUBCLASSES for Start Class:",intitem,"is:", i

    if Flag==1:
        return True
    else:
        return False



def retrieveSlotsPerson_Lema(WorkingDirectory,startClass,persLema,itkPers):
    global currentRule
    from rule import currentRule
    Qvar=currentRule
    subClassListSlot={}
    classListTempSlot={}
    subClassTempSlot={}

    classPersonTemp=startClass
    path=WorkingDirectory + "QA-Enterprise.rdfs"
    g = rdflib.Graph()
    g.parse(path)
    propPersonList={}
    propPersonTemp={}
    classPersonListTemp={}
    lst_persLema=string.lower(persLema)
    Flag=0
    itemdig=""
    seq1=str(itkPers)
    itemdig=itemdig.join(seq1)
    intitem=str(itemdig)
    # intitem=int(itemdig)

    classPr=str(classPersonTemp)
    print "SLOT for Person item in synset for classPr",classPr,itkPers

    qClass = g.query("""
                PREFIX ot: <http://www.opentox.org/api/1.1#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT  ?varClass ?varProperty
                WHERE  {
                    ?varClass rdf:type rdfs:Class.
                    ?varProperty rdf:type ?propertyType;
                                 rdfs:domain ?varClass.
                    FILTER (CONTAINS (  str(?varClass), '"""+classPr+"""'))

                }""")

    i=0
    for row in qClass.result:
        # if i==0:
        #     print "The result of SLOTS for Person :",lst_persLema,  " are:----------------","\n"

        propPersonList[intitem,i]=str(row)
        propPersonTemp[intitem,i]=propPersonList[intitem,i].split()

        propPersonTemp[intitem,i][0]=propPersonTemp[intitem,i][0].rsplit('/rdf')[-1]
        propPersonTemp[intitem,i][1]=propPersonTemp[intitem,i][1].rsplit('/rdf')[-1]

        propPersonTemp[intitem,i][0]=propPersonTemp[intitem,i][0].rstrip("'),)")
        propPersonTemp[intitem,i][1]=propPersonTemp[intitem,i][1].rstrip("'),)")

        propPersonTemp[intitem,i][0]=Literal(propPersonTemp[intitem,i][0], datatype=XSD.string)
        propPersonTemp[intitem,i][0]=propPersonTemp[intitem,i][0].value
        propPersonTemp[intitem,i][0]=str(propPersonTemp[intitem,i][0])

        propPersonTemp[intitem,i][1]=Literal(propPersonTemp[intitem,i][1], datatype=XSD.string)
        propPersonTemp[intitem,i][1]=propPersonTemp[intitem,i][1].value
        propPersonTemp[intitem,i][1]=str(propPersonTemp[intitem,i][1])

        pure_ClassPerson_name=string.lower(pure_class_name(propPersonTemp[intitem,i][0]))
        pure_SlotPerson_name=string.lower(pure_slot_name(propPersonTemp[intitem,i][1]))
        if (string.find(pure_ClassPerson_name,lst_persLema)==0):
            # (lst_persLema in pure_ClassPerson_name):
            cls_Threshold=percent_diff(lst_persLema,pure_ClassPerson_name)
            if cls_Threshold > 0.75:
                Qvar.addBoundedClassPerson(propPersonTemp[intitem,i][0],intitem,i)
                Flag=1
        if (string.find(pure_SlotPerson_name,lst_persLema)==0):
                # (lst_persLema in pure_SlotPerson_name):
           slot_Threshold=percent_diff(lst_persLema,pure_SlotPerson_name)
           if slot_Threshold > 0.45:
               Qvar.addBoundedSlotPerson(propPersonTemp[intitem,i],propPersonTemp[intitem,i][0],propPersonTemp[intitem,i][1],intitem,i)
               retrieveInstancePerson_Lema(WorkingDirectory,propPersonTemp[intitem,i][0],propPersonTemp[intitem,i][1],"lst_persLema",intitem)
               Flag=1

        if retrieveInstancePerson_Lema(WorkingDirectory,propPersonTemp[intitem,i][0],propPersonTemp[intitem,i][1],lst_persLema,intitem):
            Flag=1
        i=i+1

        # if Flag!=1:
    qSubClassSlot = g.query("""
                            PREFIX ot: <http://www.opentox.org/api/1.1#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            SELECT  ?varClass ?subclass
                            WHERE  {
                                ?subclass  rdfs:subClassOf ?varClass.
                                FILTER ( CONTAINS( str(?varClass), '"""+classPr+"""'))

                            }""")
    j=0
    for row in qSubClassSlot:
        subClassListSlot[intitem,j]=str(row)
        subClassTempSlot[intitem,j]=subClassListSlot[intitem,j].split()

        subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rsplit('/rdf')[-1]
        subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rsplit('/rdf')[-1]

        subClassTempSlot[intitem,j][0]=subClassTempSlot[intitem,j][0].rstrip("'),)")
        subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].rstrip("'),)")
        subClassTempSlot[intitem,j][1]=Literal(subClassTempSlot[intitem,j][1], datatype=XSD.string)
        subClassTempSlot[intitem,j][1]=subClassTempSlot[intitem,j][1].value
        subClassTempSlot[intitem,j][1]=str(subClassTempSlot[intitem,j][1])
        if retrieveSlotsPerson_Lema(WorkingDirectory,subClassTempSlot[intitem,j][1],lst_persLema,intitem):
            return True
        j=j+1
    if (Flag==1):
        return True
    else:
        return False


def isPersonIn_Ont(s,WorkingDirectory,personSC):
    from rule import isVerb,isAdjective,isAdverb,isVerbAux,isNoun
    from rule import currentRule
    Qvar=currentRule
    list_tk_Pers=[]
    list_Cls_Pers=[]
    list_Slot_Pers=[]
    list_Inst_Pers=[]

    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if isVerb(s,itk) or isVerbAux(s,itk) or isAdjective(s,itk) or isAdverb(s,itk) or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos==".":
            continue

        if retrieveSlotsPerson_Lema(WorkingDirectory,personSC,lma,itk):
            list_tk_Pers.append(itk)
            Flag=1

    classWTemp=Qvar.boundedClassPerson
    for item in classWTemp.keys():
        print "Subclass Person Retrieved is :", classWTemp[item],item[0],item[1]
        print "\n","NOTE:    Person_Ont was found in Ontology, Qvar.boundedClassPerson,",Qvar.boundedClassPerson,"\n"
        print "\n","NOTE:    Person_Ont was found in Ontology, Qvar.boundedSlotPerson,",Qvar.boundedSlotPerson,"\n"
        print "\n","NOTE:    Person_Ont was found in Ontology, Qvar.boundedInstancePerson,",Qvar.boundedInstancePerson,"\n"
        print "\n","NOTE:    Person_Ont list_tk_Pers",list_tk_Pers,"\n"


    classWTemp=Qvar.boundedClassPerson
    for itemCls in classWTemp.keys():
        list_Cls_Pers.append(classWTemp[itemCls])
    if len(list_Cls_Pers)>0:
        Qvar.addBoundedVars('ont_PER_Cls',list_Cls_Pers)

    slotWTemp=Qvar.boundedSlotPerson
    for itemSlot0,itemSlot1 in Qvar.boundedSlotPerson:
        slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
        list_Slot_Pers.append(slotArg)
    if len(list_Slot_Pers)>0:
        Qvar.addBoundedVars('ont_PER_Slot',list_Slot_Pers)

    instWTemp=Qvar.boundedInstancePerson
    for itemInst0,itemInst1 in Qvar.boundedInstancePerson:
        instArg=str(instWTemp[itemInst0,itemInst1][2])
        list_Inst_Pers.append(instArg)
    if len(list_Inst_Pers)>0:
        Qvar.addBoundedVars('ont_PER_Inst',list_Inst_Pers)

    if Flag==1:
        ln=len(list_tk_Pers)
        if ln<=1:
            Qvar.addBoundedVars('tk_PER',list_tk_Pers[0])
        else:
            Qvar.addBoundedVars('tk_PER',list_tk_Pers)

        print "Person_Ont was found in Ontology,  Qvar.boundedVars", Qvar.boundedVars,"\n"
        return True
    else:
        return False


def bindPerson_Ont(s,WorkingDirectory,personSC):
    global currentRule
    from rule import currentRule
    from rule import isVerb,isAdjective,isAdverb,isVerbAux,isNoun
    Qvar=currentRule
    tks=s._get_tokens()
    Flag=0
    for itk in range(len(tks)):
        tk = tks[itk]
        wrd=tk._word()
        wrds=string.lower(wrd)
        lma=tk._lemma()
        lmas=string.lower(lma)
        pos=tk._pos()
        if isVerb(s,itk) or isVerbAux(s,itk) or isAdjective(s,itk) or isAdverb(s,itk) or pos=="DT" or pos=="IN" or pos=="CC" or pos=="CD" or pos=="MD" or pos=="PRP" or\
                        pos=="TO" or pos=="SYM" or pos=="WDT" or pos=="WP"or pos=="WP$" or pos=="WRB" or pos=="EX" or pos=="IN" or pos=="." :
            continue

        if retrieveSlotsPerson_Lema(WorkingDirectory,personSC,lma,itk):
            Flag=1
            Qvar.addBoundedVars('tk_PER',itk)


    classWTemp=Qvar.boundedClassPerson
    for item in classWTemp.keys():
        print "Subclass Person Retrieved is :", classWTemp[item],item[0],item[1]
        print "\n","NOTE:    Person_Ont was found in Ontology, Qvar.boundedClassPerson,",Qvar.boundedClassPerson,"\n"
        print "\n","NOTE:    Person_Ont was found in Ontology, Qvar.boundedSlotPerson,",Qvar.boundedSlotPerson,"\n"
        print "\n","NOTE:    Person_Ont was found in Ontology, Qvar.boundedInstancePerson,",Qvar.boundedInstancePerson,"\n"



    classWTemp=Qvar.boundedClassPerson
    k=0
    for itemCls in classWTemp.keys():
        Qvar.addBoundedVars('ont_PER_Cls_' + str(k),classWTemp[itemCls])
        k=k+1

    slotWTemp=Qvar.boundedSlotPerson
    l=0
    for itemSlot0,itemSlot1 in Qvar.boundedSlotPerson:
        slotArg=str(slotWTemp[itemSlot0,itemSlot1][1])
        Qvar.addBoundedVars('ont_PER_Slot_' +  str(l),slotArg)
        l=l+1

    instWTemp=Qvar.boundedInstancePerson
    m=0
    for itemInst0,itemInst1 in Qvar.boundedInstancePerson:
        instArg=str(instWTemp[itemInst0,itemInst1][2])
        Qvar.addBoundedVars('ont_PER_Inst_' +  str(m),instArg)
        m=m+1

    print "Person_Ont was found in Ontology,  Qvar.boundedVars", Qvar.boundedVars,"\n"

    if Flag==1:
        return True
    else:
        return False


