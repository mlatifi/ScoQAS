__author__ = 'majid'

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

