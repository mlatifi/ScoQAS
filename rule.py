__author__ = 'majid'

# !/pkg/ldc/bin/python2.7
#-----------------------------------------------------------------------------
# Name:        rule.py
#
# Author:      Majid
#
# Created:     2014/06/06
# classes used by RepresentingSentences for QAS
#-----------------------------------------------------------------------------


class QTclassrule(object):

    def __init__(self,id,t):
        self._init_vars(id,t)

    def _init_vars(self,id,t):
        global currentRule
        currentRule = self
        self.id=id
        self.workingDir = 'D:/PhD/PhD Tesis/Project/RepresentingSentences/data/'
        self.conds=[]
        self.actions=[]
        self.constraints=[]
        self.EATs=[]
        self.tk_indicators=[]

        self.type=t
        self.boundedVars={}
        self.boundedConsts={}
        self.boundedEATs={}

        self.boundedClass={}
        self.boundedSubClass={}
        self.boundedSlot={}
        self.boundedSlot4Class={}
        self.boundedInstance={}

        self.boundedGraphClass={}
        self.boundedGraphSubClass={}
        self.boundedGraphSlot={}
        self.boundedGraphSlot4Class={}
        self.boundedGraphInstance={}

        self.currentDGraph=nx.DiGraph()
        self.currentConsDGraph=nx.DiGraph()
        self.currentPrologDGraph=nx.DiGraph()
        self.currentMergeDGraph=nx.DiGraph()
        self.currentGraph_Inst={}

        self.boundedClassAnswer={}
        self.boundedSubClassAnswer={}
        self.boundedSlotAnswer={}
        self.boundedSlotTypeAnswer={}
        self.boundedInstanceAnswer={}
        self.boundedExactSlotAnswer={}
        self.boundedExactInstanceAnswer={}
        self.boundedExactAnswer={}

        self.boundedClassAction={}
        self.boundedSlotAction={}
        self.boundedSlotTypeAction={}
        self.boundedInstanceAction={}

        self.boundedClassWhere={}
        self.boundedSubClassWhere={}
        self.boundedSlotWhere={}
        self.boundedSlotTypeWhere={}
        self.boundedInstanceWhere={}


        self.boundedClassPerson={}
        self.boundedSubClassPerson={}
        self.boundedSlotPerson={}
        self.boundedSlotTypePerson={}
        self.boundedInstancePerson={}

    def addCondition(self,c):
        self.conds.append(c)

    def addAction(self,a):
        self.actions.append(a)

    def addConstraint(self,c):
        self.constraints.append(c)

    def addEAT(self,answT):
        self.EATs.append(answT)

    def addIndicators_tk(self,tk_ind):
        if not (tk_ind in self.tk_indicators):
            self.tk_indicators.append(tk_ind)

    def addIndicatorsList_tk(self,tkList_ind):
        tkList_Indicator=list(set(tkList_ind))
        for item in range(len(tkList_Indicator)):
            if not (tkList_Indicator[item] in self.tk_indicators):
                self.tk_indicators.append(tkList_Indicator[item])


    def addBoundedVars(self,item,bindVars):

        if not(self.existBoundedVars(item,bindVars)):
            self.boundedVars[item]=bindVars
            # print "This Vars added to bindVars,item: ",bindVars,item,self.boundedVars
            return True
        else:
            return False


    def addBoundedList_Vars(self,item,bindListVars):
        bListVars=list(set(bindListVars))
        if not(self.existBoundedVars(item,bListVars)):
            self.boundedVars[item]=bListVars
            # print "This Vars added to bindListVars,item: ",bListVars,item,self.boundedVars
            return True
        else:
            return False

    def addBoundedClass(self,bindClass,tk,i):
        if not(self.existBoundedClass(bindClass,tk,i)):
            self.boundedClass[tk,i]=bindClass
            # print "WOOW!!, This class added to list,itk,i",bindClass,tk,i
            return True
        else:
            return False


    def addBoundedClassItem(self,bindClassItem0,tk,i):
        if not(self.existBoundedClassItem(bindClassItem0,tk,1)):
            self.boundedClassItem[tk,i]=bindClassItem0
            return True
        else:
            return False


    def addBoundedClassAction(self,bindClassAction0,tk,i):
        if not(self.existBoundedClassAction(bindClassAction0,tk,1)):
            self.boundedClassAction[tk,i]=bindClassAction0
            return True
        else:
            return False


    def addBoundedClassAnswer(self,bindClassAnswer0,tk,i):
        if not(self.existBoundedClassAnswer(bindClassAnswer0,tk,1)):
            self.boundedClassAnswer[tk,i]=bindClassAnswer0
            return True
        else:
            return False

    def addBoundedClassWhere(self,bindClassW0,tk,i):
        if not(self.existBoundedClassWhere(bindClassW0,tk,1)):
            self.boundedClassWhere[tk,i]=bindClassW0
            return True
        else:
            return False

    def addBoundedClassPerson(self,bindClassP0,tk,i):
        if not(self.existBoundedClassPerson(bindClassP0,tk,1)):
            self.boundedClassPerson[tk,i]=bindClassP0
            return True
        else:
            return False

    def addBoundedClassMemb(self,bindClassMemb0,tk,i):
        if not(self.existBoundedClassMemb(bindClassMemb0,tk,1)):
            self.boundedClassMemb[tk,i]=bindClassMemb0
            return True
        else:
            return False

    def addBoundedSubClassPerson(self,bindSubClassP,bindSubClassP0,bindSubClassP1,tk,i):
        bindSubClasslocal=bindSubClassP
        if not(self.existBoundedSubClassPerson(bindSubClassP0,bindSubClassP1,tk,i)):
            self.boundedSubClassPerson[tk,i]=bindSubClasslocal
            self.boundedSubClassPerson[tk,i][0]=bindSubClassP0
            self.boundedSubClassPerson[tk,i][1]=bindSubClassP1

            return True

        else:
            return False

    def existBoundedClassWhere(self,ex_bindClassW0,tk,i):

        Flag=0
        for bndcls in self.boundedClassWhere:
            if str(self.boundedClassWhere[bndcls])==str(ex_bindClassW0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False

   
    def existBoundedClassPerson(self,ex_bindClassP0,tk,i):

        Flag=0
        for bndcls in self.boundedClassPerson:
            if str(self.boundedClassPerson[bndcls])==str(ex_bindClassP0):
                Flag=1
        if Flag==1:
            return True
        else:
            return False

   

    def executeConditions(self,con1,con2):
        i=0
        for c in self.conds:
            if not c.execute(con1,con2):
                return False

        return True

    def executeActions(self,act1,act2):
        for a in self.actions:
            a.execute(act1,act2)
        return (self.type, self.boundedVars)


    def describe(self):
        print 'ID : ', self.id
        print 'Result', self.type
        print len(self.conds), 'Conditions'
        for c in self.conds:
            c.describe()
        print len(self.a), 'Actions'
        for a in self.actions:
            a.describe()

    def describeBoundedOntology(self):
        print 'ID : ', self.id
        print 'Result', self.type
        print len(self.conds), 'Conditions'
        print "Bounded Class after looking in ontology is:","\n"
        for cls in self.boundedClass:
            print "\t",cls,"\t",self.boundedClass[cls]

        print "Bounded Sub Class after looking in ontology is:","\n"
        for subcls in self.boundedSubClass:
            print "\t",subcls,"\t",self.boundedSubClass[subcls][0],self.boundedSubClass[subcls][1]

        print "Bounded SLOT after looking in ontology is:","\n"
        for slot in self.boundedSlot:
            print "\t",slot,"\t", self.boundedSlot[slot][0],self.boundedSlot[slot][1]

        print "Bounded INSTANCE after looking in ontology is:","\n"
        for ins in self.boundedInstance:
            print "\t",ins,"\t", self.boundedInstance[ins]


        # self.boundedSlotTuple=()
        # self.boundedInstance={}
        # self.boundedClassInstance={}



class QTclasscondition(object):

    def __init__(self, id, condition):
        self._init_vars(id, condition)

    def _init_vars(self, id, condition):
        self.id=id
        self.condition=condition

    def execute(self,s,r):
        return eval(self.condition)

    def describe(self):
        print self.id, '\t',self.condition

class QTclassAction(object):

    def __init__(self, id, action):
        self._init_vars(id, action)

    def _init_vars(self, id, action):
        self.id=id
        self.action=action

    def execute(self,s,r):
        return eval(self.action)

    def describe(self):
        print self.id, '\t',self.action

##functions
# currentRule=QTclassrule('','')


def addtk_Type_Indicators(r,tk_list):
    if len(tk_list)==1:
        tkItem=tk_list.pop()
        # print "len(tk_list)==1: function addtk_Type_List of list is", tkItem
        r.addIndicators_tk(tkItem)
    elif len(tk_list)>1:
        # print "len(objList)>1: function addtk_Type_List of list is", tk_list
        lnIdx=len(tk_list)
        i=0
        while i<lnIdx:
            r.addIndicators_tk(tk_list.pop())
            i=i+1
        # print "after add tk_Type r.boundedVars.values()",r.boundedVars,r.boundedVars.values()

def getNoun_Obj_of_Sentence(s,r,obj):
    listNounObject=[]
    list_Dep=s.sint._dependencies
    # print "Object[0]",obj
    for lst_Dep in list_Dep:
        if (str(lst_Dep[2])=="nn" and  str(lst_Dep[0])==str(obj)):
            listNounObject.append(lst_Dep[1])
    # print "listNounObject is :",listNounObject
    return listNounObject

def getAdj_Obj_of_Sentence(s,r,obj):
    listAdjObject=[]
    list_Dep=s.sint._dependencies
    # print "Subject[0]",obj
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="amod" and str(lst_Dep[0])==str(obj):
            listAdjObject.append(lst_Dep[1])
    # print "listAdjective Object is :",listAdjObject
    return listAdjObject


def wordofTkIs(s,t,l):
    return s._get_token(t)._word()==l

def lemmaofTkIs(s,t,l):
    return s._get_token(t)._lemma()==l

def neofTkIs(s,t,ne):
    return s._get_token(t)._ne()==ne

def posofTkIs(s,t,p):
    return re.match(p,s._get_token(t)._pos())

def isVerb(s,t):
    return posofTkIs(s,t,'^V.*$')

def isVerbAux(s,t):
    return  posofTkIs(s,t,'MD')


def isVerbAux_Main(s,t):
    return (lemmaofTkIs(s,t,'be') or lemmaofTkIs(s,t,'have') or lemmaofTkIs(s,t,'has') or lemmaofTkIs(s,t,'do'))

def isBeVerb(s,t):
   tks=s._get_tokens()
   if t=="":
       for itk in range(len(tks)):
           if lemmaofTkIs(s,itk,'be'):
               return True
   else:
       if lemmaofTkIs(s,t,'be'):
           return True

   return False

def isNoun(s,t):
    return posofTkIs(s,t,'^N.*$')

def isAdjective(s,t):
    if lemmaofTkIs(s,t,'run') and wordofTkIs(s,t,'running'):
        return True
    return posofTkIs(s,t,'^J.*$')

def isAdverb(s,t):
    return posofTkIs(s,t,'^R.*$')

def isWhere(s,r,tk):
    listSubj=[]
    listObj=[]
    listNounSubj=[]
    listNounObj=[]
    listAdjSubj=[]
    listAdjObj=[]
    listSubj_itkType=[]
    listSubj_Type=[]
    listObj_itkType=[]
    listConjSubj=[]
    listConjObj=[]
    list_itkType=[]
    listSubjGEO_itkType=[]
    listObjGEO_itkType=[]
    listObj_det_itkType=[]
    listWhereIn_itkType=[]

    flagS=0
    flagSs=0
    flagNS=0
    flagAS=0
    flagCS=0
    flagO=0
    flagNO=0
    flagAO=0
    flagCO=0
    flagOd=0
    flagOo=0
    flag_in=0

    listSubj=getSubj_of_Sentence(s,r)
    if len(listSubj)>0:
        flagS=1
        listNounSubj=getNoun_Subj_of_Sentence(s,r,listSubj[0])
        print "listSubj,listNounSubj",listSubj,listNounSubj
        if len(listNounSubj)>0:
            flagNS=1
        listAdjSubj=getAdj_Subj_of_Sentence(s,r,listSubj[0])
        if len(listAdjSubj)>0:
            flagAS=1
            if len(listAdjSubj)>0:
                flagAS=1
                listConjSubj=getConj_and_Subj_of_Sentence(s,r,listAdjSubj)
                if len(listConjSubj)>0:
                    flagCS=1

    listObj=getObj_of_Sentence(s,r)
    if len(listObj)>0:
        flagO=1
        listNounObj=getNoun_Obj_of_Sentence(s,r,listObj[0])
        if len(listNounObj)>0:
            flagNO=1
        listAdjObj=getAdj_Obj_of_Sentence(s,r,listObj[0])
        if len(listAdjObj)>0:
            flagAO=1
            listConjObj=getConj_and_Obj_of_Sentence(s,r,listAdjObj)
            if len(listConjObj)>0:
                flagCO=1

    list_Dep=s.sint._dependencies
    for lst_Dep in list_Dep:
        if str(lst_Dep[2])=="prep_in":
            itkLoc=lst_Dep[1]
            flag_in=1
            listWhereIn_itkType=list(set(makeDetW_List(s,r,itkLoc)))
        if (str(lst_Dep[2])=="nsubj" or str(lst_Dep[2])=="nsubjpass") and isGEO_tk(s,r,lst_Dep[1]):
            itkSubj=lst_Dep[1]
            flagSs=1
            listSubjGEO_itkType=list(set(makeSubj_List(s,r,itkSubj)))
        if (str(lst_Dep[2])=="pobj" or str(lst_Dep[2])=="pobjpass") and isGEO_tk(s,r,lst_Dep[1]):
            itkObj=lst_Dep[1]
            flagOo=1
            listObjGEO_itkType=list(set(makeObj_List(s,r,itkObj)))
        if str(lst_Dep[2])=="det" and lemmaofTkIs(s,lst_Dep[1],"which") and isGEO_tk(s,r,lst_Dep[0]):
            flagOd=1
            itkObjd=lst_Dep[0]
            listObj_det_itkType=list(set(makeDetW_List(s,r,itkObjd)))


    # if flagSs==1:
    #     for lst_Dep in list_Dep:
    #         if str(lst_Dep[2])=="prep_of" and str(lst_Dep[0])==str(itkSubj):
    #             print "Prep_of",lst_Dep[1]
    #             listSubjGEO_itkType.append(lst_Dep[1])

    # print "flagS,flagAS,flagNS,flagCS",flagS,flagAS,flagNS,flagCS
    # print "flagO,flagAO,flagNO,flagCO",flagO,flagAO,flagNO,flagCO
    listSubj_itkType=list(set(listSubj+listNounSubj+listAdjSubj+listConjSubj))
    print "isWhat:flagS,flagAS,flagNS,flagCS,flagSs,flag_in, -listSubj_itkType-, -listWhereIn_itkType-: ",flagS,flagAS,flagNS,flagCS,flagSs,flag_in,listSubj_itkType,listWhereIn_itkType
    listObj_itkType=list(str(listObj+listNounObj+listAdjObj+listConjObj))

    if tk!="":
        t=tk
        if isWhere_tk(s,r,t) and flag_in==1:
            addtk_Type_Indicators(r,listWhereIn_itkType)
            return True
        elif isWhere_tk(s,r,t) and flagS==1:
            addtk_Type_Indicators(r,listSubj_itkType)
            return True
        elif posofTkIs(s,t,'DT') and flagSs==1:
            addtk_Type_Indicators(r,listSubjGEO_itkType)
            return True
        elif isInWhich(s,r,t):
            if flagOd==1:
                addtk_Type_Indicators(r,listObj_det_itkType)
                return True
            elif flagSs==1:
                addtk_Type_Indicators(r,listSubj_itkType)
                return True
        elif isWhich(s,r,t):
            if flagOd==1:
                addtk_Type_Indicators(r,listObj_det_itkType)
                return True
            if flagOo==1:
                addtk_Type_Indicators(r,listObjGEO_itkType)
                return True
            if t==0 and flagSs==1:
                addtk_Type_Indicators(r,listSubjGEO_itkType)
                return True
            elif t>1 and flagOd==1:
                addtk_Type_Indicators(r,listObj_det_itkType)
                return True
        elif isWhat_tk(s,r,t) and flagSs==1:
            addtk_Type_Indicators(r,listSubjGEO_itkType)
            return True
        return False

    else:
        tks=s._get_tokens()
        for itk in range(len(tks)):
            if isWhich(s,r,itk):
                return isWhere(s,r,itk)
        return False

def isWhere_tk(s,r,t):
    return lemmaofTkIs(s,t,'where')


def isPerson(s,r):
    flag=0
    itk=0
    listPerson=[]
    tks=s._get_tokens()
    lnItk=len(tks)
    # for itk in range(len(tks)):
    while itk <lnItk:
        lma_tk=s._get_token(itk)._lemma()
        if not(lma_tk.isdigit()):
            if itk+3<lnItk:
                if isNonPerson_3tk(s,r,itk):
                    itk=itk+3
                    continue

                elif isPerson_3tk(s,r,itk):
                    flag=1
                    listPerson.append(itk)
                    listPerson.append(itk+1)
                    listPerson.append(itk+2)
                    itk=itk+3
                    continue
            if ((isPerson_NonRelative(s,r,itk) or isPerson_tk(s,r,itk)) and flag==0):
                flag=1
                # r.addIndicators_tk(itk)
                listPerson.append(itk)
            elif ((isPerson_NonRelative(s,r,itk) or isPerson_tk(s,r,itk)) and flag!=0):
                # r.addIndicators_tk(itk)
                listPerson.append(itk)
                flag=2
        itk=itk+1

    print "content of listperson before remove",r.tk_indicators,listPerson
    listPerson=removeListA_listB(r.tk_indicators,listPerson)
    # print "content of listperson after remove",r.tk_indicators,listPerson
    lnIdx=len(listPerson)
    if lnIdx>0 and (flag==1 or flag==2):
        listIndicator=addListA_listB(r.tk_indicators,listPerson)
        # print "content of listIndicator after adding",r.tk_indicators,listIndicator,listPerson
        print "after removing repeated person in indicator ISPERSON()", listPerson
        return True
    return False


def isPerson_tk(s,r,itk):
    listNonPerson=['name','date','birth','Uzi','instrument','Berlin','frog','tree','Captain America','creator','Illinois','Minecraft']
    lmaItk=""
    lmaItk1=s._get_token(itk)._lemma()
    if itk>0:
        lmaItk0=s._get_token(itk-1)._lemma()
        lmaItk=lmaItk0 + " " +lmaItk1
        # print "Combined Person",lmaItk
    if isEntity_tk(s,r,itk):
        if (neofTkIs(s,itk,'PER') or isPersonInWN(s,r,itk)) and (not (lmaItk1 in listNonPerson) and not (lmaItk in  listNonPerson)):
            print "isPerson_tk!!!",lmaItk1
            return True

    return False

def isPerson_3tk(s,r,itk):
    cmpPersonName=['Lawrence of Arabia']
    tk_per=itk
    lma_tk1=s._get_token(tk_per)._lemma()
    lma_tk2=s._get_token(tk_per+1)._lemma()
    lma_tk3=s._get_token(tk_per+2)._lemma()
    lma_Cmp=lma_tk1 + " " + lma_tk2 + " " + lma_tk3
    if (lma_Cmp in cmpPersonName):
         return True
    return False

def isNonPerson_3tk(s,r,itk):
    cmpPersonName=['Bay of Pigs']
    tk_per=itk
    lma_tk1=s._get_token(tk_per)._lemma()
    lma_tk2=s._get_token(tk_per+1)._lemma()
    lma_tk3=s._get_token(tk_per+2)._lemma()
    lma_Cmp=lma_tk1 + " " + lma_tk2 + " " + lma_tk3
    if (lma_Cmp in cmpPersonName):
         return True
    return False


def isPersonInWN(s,r,itk):
    lsItem1=[]
    lsItem2=[]
    # ls=getSynsets(itk,pos='n')
    # ls=lemmalist(wrd)
    lma_tk=s._get_token(itk)._lemma()
    if isEntity_tk(s,r,itk):
        ls=entityList(lma_tk)
        # print "list in  Synset WN for Person:",lma_tk,ls
        for lsitem in range(len(ls)):
            lsItem1=ls[lsitem]
            lenitem=len(lsItem1)
            for subitem1 in range(len(lsItem1)):
                lsItem2=lsItem1[subitem1]
                for subitem2 in range(len(lsItem2)):
                    if lsItem2[subitem2]=="person" or lma_tk=="people":
                        # print "\n","was found Person in isPersonInWN:",lma_tk,lenitem,lsItem2[subitem2]
                        return True
                    # else:
                        # print "\n","item of list in  Synset WN for Person:",lma_tk,lenitem,lsItem2[subitem2]

    return False

def isAction(s,r):
    nonAction=['belong']
    listAction=[]
    listAction=getVerb_of_Sentence(s,r)
    for vrb in listAction:
        if s._get_token(vrb)._lemma() in nonAction:
            listAction.remove(vrb)
    for vrb in listAction:
        if isVerbAux_Main(s,vrb):
            listAction.remove(vrb)
            # print "isVerbAux_Main"
    print "len of Action", len(listAction),listAction
    # print "isAction: content of listAction before remove",r.tk_indicators,listAction
    listAction=removeListA_listB(r.tk_indicators,listAction)
    # print "isAction: content of listAction after remove",r.tk_indicators,listAction
    lnIdx=len(listAction)
    if lnIdx>0:
        print "find action"
        addtk_Type_Indicators(r,listAction)
        return True
    return False



def bindAction(s,r):
    nonAction=['belong']
    listConjAction=[]
    listAction=[]
    listAction=getVerb_of_Sentence(s,r)
    for vrb in listAction:
        if s._get_token(vrb)._lemma() in nonAction:
            listAction.remove(vrb)
    for vrb in listAction:
        # print "content of isAction:", vrb
        # if isVerbAux(s,vrb):
        #     print "isVerbAux"
        if isVerbAux_Main(s,vrb):
            listAction.remove(vrb)
    # print "len of Action", len(listAction),listAction
    listConjAction=getConj_and_Subj_of_Sentence(s,r,listAction)
    print "isAction: content of listAction before remove",r.tk_indicators,listAction,listConjAction
    addListA_listB(listAction,listConjAction)
    listAction=removeListA_listB(r.tk_indicators,listAction)
    print "isAction: content of listAction after remove",r.tk_indicators,listAction
    add_tkType_List(r,listAction,"tk_ACT","ont_ACT")

    return True
