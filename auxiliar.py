#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        auxiliar.py
#
# Author:      Horacio
#
# Created:     2008/08/03
# classes used by RTE 
#-----------------------------------------------------------------------------


import re
left_context_window=2
right_context_window=2

character_equivalences = {'`':'"',
                          'PPh.D.':'Ph.D.',
                          '((':'(',
                          'etc.)':'etc).',
                          '\xc2\xa1':'!',
                          '\xc2\xa2':'cent',
                          '\xc2\xa3':'pound',
                          '\xe2\x82\xa4':'pound',
                          '\xc2\xa5':'yen',
                          '\xc2\xb0':'degree',
                          'xe2\x82\xac':'euro',
                          '\xc2\xb9':'1',
                          '\xc2\xb2':'2',
                          '\xc2\xb3':'3',
                          '\xc2\xb7':'.',
                          '\xc2\xbc':'1/4',
                          '\xc2\xbd':'1/2',
                          '\xc2\xbe':'3/4',
                          '\xc2\xbf':'?',
                          '\xc3\x80':'A',
                          '\xc3\x81':'A',
                          '\xc3\x82':'A',
                          '\xc3\x83':'A',
                          '\xc3\x84':'A',
                          '\xc3\x85':'A',
                          '\xc3\xa0':'a',
                          '\xc3\xa1':'a',
                          '\xc3\xa2':'a',
                          '\xc3\xa3':'a',
                          '\xc3\xa4':'a',
                          '\xc3\xa5':'a',
                          '\xc3\xa6':'a',
                          '\xc3\xa8':'e',
                          '\xc3\xa9':'e',
                          '\xc3\x87':'C',
                          '\xc3\xa7':'c',
                          '\xc3\x90':'E',
                          '\xc3\x88':'E',
                          '\xc3\x89':'E',
                          '\xc3\x8a':'E',
                          '\xc3\x8b':'E',
                          '\xc3\xb0':'e',
                          '\xc3\xa8':'e',
                          '\xc3\xa9':'e',
                          '\xc3\xaa':'e',
                          '\xc3\xab':'e',
                          '\xc3\x8c':'I',
                          '\xc3\x8d':'I',
                          '\xc3\x8e':'I',
                          '\xc3\x8f':'I',
                          '\xc3\xac':'i',
                          '\xc3\xad':'i',
                          '\xc3\xae':'i',
                          '\xc3\xaf':'i',
                          '\xc3\x91':'N',
                          '\xc3\xb1':'n',
                          '\xc3\x92':'O',
                          '\xc3\x93':'O',
                          '\xc3\x94':'O',
                          '\xc3\x95':'O',
                          '\xc3\x96':'O',
                          '\xc3\x98':'O',
                          '\xc3\xb2':'o',
                          '\xc3\xb3':'o',
                          '\xc3\xb4':'o',
                          '\xc3\xb5':'o',
                          '\xc3\xb6':'o',
                          '\xc3\xb8':'o',
                          '\xc3\x99':'U',
                          '\xc3\x9a':'U',
                          '\xc3\x9b':'U',
                          '\xc3\x9c':'U',
                          '\xc3\xb9':'u',
                          '\xc3\xba':'u',
                          '\xc3\xbb':'u',
                          '\xc3\xbc':'u',
                          '\xc3\x9d':'Y',
                          '\xc3\xbd':'y',
                          '\xc3\xbf':'y',
                          '\xe2\x80\x93':'-',
                          '\\':''}


##classes



class ENTAILMENT:
    
    def __init__(self):
        self._init_vars()
        
    def __init__(self,t,h,res,ref):
        self._init_vars(t,h,res,ref)

    def _init_vars(self):
        self._t=[]
        self._h=[]
        self._res=''
        self._ref=''

    def _init_vars(self,t,h,res,ref):
        self._t=t
        self._h=h
        self._res=res
        self._ref=ref



class TOKEN:
    
    def __init__(self):
        self._init_vars()
    
    def __init__(self,sent):
        self._init_vars(sent)
    
    def _init_vars(self):
        self._content=['','','','','',[]]

    def _init_vars(self,sent):
        self._content=[sent[0],sent[1],sent[2],sent[3],sent[4]]
        if sent[5]:
            self._content.append(sent[5].split(','))
        else:
            self._content.append([])
        
    def _word(self):
        return self._content[0]

    def _lemma(self):
        return self._content[1]
    
    def _pos(self):
        return self._content[2]
    
    def _ne(self):
        return self._content[3]
    
    def _ne_2(self):
        return self._content[4]
    
    def _synsets(self):
        return self._content[5]

    def _recover_word(self):
        return 'word("'+self._content[0].replace('"','_')+'")'

    def _recover_lemma(self):
        return 'lema("'+self._content[1].replace('"','_')+'")'
    
    def _recover_pos(self):
        return 'pos("'+self._content[2]+'")'
    
    def _recover_ne(self):
        if self._content[3] == '' or self._content[3] == '0':
            return '\'nil\''
        else:
            return '\''+self._content[3]+'\''
    
    def _recover_ne_2(self):
        if self._content[4] == '' or self._content[4] == '0':
            return '\'nil\''
        else:
            return '\''+self._content[4]+'\''
    
    def _recover_synsets(self):
        if self._content[5] == '':
            return '[]'
        j=''
        for i in self._content[5]:
            j+=('\''+str(i)+'\''+',')
        return '['+j[0:-1]+']'

    def tk2Prolog(self):
        tk='['+self._recover_word()+','+self._recover_lemma()+','+self._recover_pos()+','+self._recover_ne()+','+self._recover_ne_2()+','+self._recover_synsets()+']'
        return tk

    def describe(self, verbose = True):
        if verbose:
            print 'word: ',self._recover_word()
            print 'lemma: ',self._recover_lemma()
            print 'pos: ',self._recover_pos()
            print 'ne: ',self._recover_ne()
            print 'ne_2: ',self._recover_ne_2()
            print 'synsets: ',self._recover_synsets()

        else:
            print self._word(), self._lemma(), self._pos(), self._ne(), self._ne_2()
            print self._synsets()

class NE:
    
    def __init__(self,sent,index):
        self._init_vars(sent,index)

    def _init_vars(self,sent,index):
        self._tk=sent._content[index]
        self._lc=[]
        for i in range(1,left_context_window+1):
            if index-i >= 0:
                self._lc.append(sent._content[index-i])
        self._rc=[]
        for i in range(1,right_context_window+1):
            if index+i < len(sent._content):
                self._rc.append(sent._content[index+i])
        

class ATTRIBUTE:
    
    def __init__(self,lu,tk):
        self._init_vars(lu,tk)
    
    def _init_vars(self,lu,tk):
        self._content=tk
        self._lu=int(lu)

    def _recover_attribute(self,tu):
        return str(tu)+'_'+str(self._lu)+' '+self._content

    def _text(self):
        return patr5.match(self._content).group(1)


class DOC:
    
    def __init__(self):
        self._init_vars()
    
    def _init_vars(self):
        self._content=[]

    def _update(self,attr):
        self._content.append(attr)

    def _recover_doc(self,tu):
        r=[]
        for i in self._content:
            r.append(i._recover_attribute(tu))
        return r

    def _text(self):
        r=''
        for i in self._content:
            r+=i._text()+' '
        return r
                     
    

class SENT:

    
    def __init__(self):
        self._init_vars()
    
    def __init__(self,cs,co):
        self._init_vars()
        self._set_current_sent(cs,co)
    
    def _init_vars(self):
        self._content=[]
        self._size=0

    def _set_current_sent(self,cs,co):
        self._current_sent=cs
        self._current_offset=co

    def _get_token(self,tk):
        try:
            return self._content[tk]
        except:
            return None

    def _get_tokens(self):
        return self._content

    def _put_token(self,tk):
        self._size+=1
        self._content.append(tk)

    def sint2Prolog(self):
        s = 'sint('+str(self._current_sent)+','+self.sint.chunks2Prolog()+','+self.sint.dependencies2Prolog()+').\n'
        return s

    def sent2Prolog(self):
        t='['
        for i in self._content:
            t+='('+i._recover_word()+','+i._recover_lemma()+','+i._recover_pos()+','+i._recover_ne()+','+i._recover_ne_2()+'),'
        return 'sent('+str(self._current_sent)+','+str(self._current_offset)+','+t[0:-1]+']).\n'

    def _text(self):
        t=''
        for i in self._content:
            t+=i._word()+' '
        return t

    def _get_NEs(self):
        nes=[]
        for i in range(0,len(self._content)):
            if self._content[i]._recover_ne() != 'nil':
                nes.append((i,NE(self,i)))
        return nes

    def describe(self, verbose = True):
        print 'sentence: ', self._current_sent
        for i in range(0,len(self._get_tokens())):
            print i
            self._get_tokens()[i].describe(verbose)
        self.sint.describe(verbose)
                       
class PRED:
    
    def __init__(self):
        self._init_vars()
    
    def __init__(self,sent):
        self._init_vars(sent)
    
    def _init_vars(self):
        self._pred=''
        self._args=[]

    def _init_vars(self,sent):
        self._pred=sent[0]
        self._args=[]
        for i in sent[1].split(','):
            self._args.append(i)
        
    def _get_pred(self):
        return self._pred

    def _get_args(self):
        return self._args
    
    def _get_arg(self,arg):
        return self._args[arg]

class SINT:

    def __init__(self):
        self._init_vars()

    def _init_vars(self):
        self._chunks=[]
        self._dependencies=None
        self._constituents=None

    def dependencies2Prolog(self):
        deps = '['
        for d in self._dependencies:
            f, t, tag = d
            deps += tag.lower()+'('+str(f+1)+','+str(t+1)+'),'
        deps = deps[:-1]+']'
        return deps

    def describe(self, verbose = True):
        print 'chunks: '
        for c in self._chunks:
            c.describe()
        print 'dependencies: ', self._dependencies
        print 'constituents: ', self._constituents

    
    def chunks2Prolog(self):
        chunks = {}
        covered = set([])
        minToken = 1000
        maxToken = -1000
        for i in self._dependencies:
            x1, x2, tag = i
            if x1 < minToken:
                minToken = max(x1,0)
            if x2 < minToken:
                minToken = max(x2,0)
            if x1 > maxToken:
                maxToken = x1
            if x2 > maxToken:
                maxToken = x2
            if tag == 'root':
                if x1 == -1:
                    head = x2
                else:
                    head = x1
        for iCh in range(len(self._chunks)):
            if self._chunks[iCh].first in chunks:
                chunks[self._chunks[iCh].first].append((self._chunks[iCh].last, iCh))
            else:
                chunks[self._chunks[iCh].first]=[(self._chunks[iCh].last, iCh)]
        for ch in chunks:
            chunks[ch].sort(reverse=True)
            covered = covered.union(set(range(ch, chunks[ch][0][0]+1)))
        chunksKeys = chunks.keys()
        chunksKeys.sort()
        noncovered = list(set(range(minToken,maxToken+1)).difference(covered))
        noncovered.sort()
        chs='[ch('+str(minToken+1)+','+str(maxToken+1)+','+'\'root\''+','+str(head+1)+',['
        icurrentChunk = 0
        currentToken = 0
        while icurrentChunk < len(chunks) or currentToken < len(noncovered):
            if currentToken == len(noncovered):
                currentTokenValue = 1000
            else:
                currentTokenValue = noncovered[currentToken]
            if icurrentChunk == len(chunks):
                currentChunkValue = 1000
            else:
                currentChunk = chunks[chunksKeys[icurrentChunk]][0][1]
                currentChunkValue = self._chunks[currentChunk].first
            if currentTokenValue < currentChunkValue:
                currentToken+=1
                chs+='tk('+str(currentTokenValue+1)+'),'
            else:
                chs+=self._chunks[currentChunk].chunk2Prolog()+','
                icurrentChunk+=1
        chs = chs[:-1]+'])]'
        return chs

        
class CHUNK:

    def __init__(self, head=None, type=None, first=None, last= None):
        self._init_vars(head, type, first, last)

    def _init_vars(self, head, type, first, last):
        self.head = head
        self.type = type
        self.first = first
        self.last = last

    def describe(self, verbose = True):
        print self.head, self.type, self.first, self.last

    def chunk2Prolog(self):
        ch='ch('+str(self.first+1)+','+str(self.last+1)+',\''+self.type+'\','+str(self.head+1)+',['
        for i in range(self.first+1,self.last+2):
            ch+='tk('+str(i)+'),'
        ch = ch[:-1]+'])'
        return ch
        
    
class ENV:

    def __init__(self):
        self._init_vars()

    def __init__(self,cs):
        self._init_vars()
        self._set_current_sent(cs)
    
    def _init_vars(self):
        self._content=[]
        self._size=0

    def _set_current_sent(self,cs):
        self._current_sent=cs

    def _get_pred(self,pr):
        return self._content[pr]

    def _put_pred(self,pr):
        self._size+=1
        self._content.append(pr)

    def _get_preds(self,types):
        preds=[]
        for i in range(0,self._size):
            if self._content[i]._get_pred() in types:
                preds.append(int(self._content[i]._get_arg(0)))
        return preds

    def _get_preds_matching(self,pattern):
        preds=[]
        for i in range(0,self._size):
            if re.match(pattern, self._content[i]._get_pred()):
                preds.append(int(self._content[i]._get_arg(0)))
        return preds


