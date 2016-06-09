__author__ = 'majid'
# coding=utf-8
from math import ceil
import os
import string
import sys
import subprocess
import datetime as dt
import xml.etree.ElementTree as ET

##################
#
# Formatting to CoNLL from XML format
#
##################

infile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\stanford-corenlp-full-2015-01-29\data\QaldConll2013.conll", 'r')
outfile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\stanford-corenlp-full-2015-01-29\data\QaldConll2013-xml.conll", 'r')
conllfile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\stanford-corenlp-full-2015-01-29\data\QalddepConll2013.conll", 'w')


       #for dependent in zip(element.findall(".//dependent")):
         #  print (i)
         #  outfile.write("\t%s" % (dependent.text))

while True:
    text1=infile.readline()
    if len(text1) == 0:
        break
    print (text1)
    if text1=="\n":
        text1=infile.readline()
    text2=outfile.readline()
    if len(text2) == 0:
        break
    print (text2)
    newtxt1=string.split(text1,None)
    newtxt2=string.split(text2,None)
    print (newtxt1,"\n")
    newtxt1[0]=newtxt2[0]
    newtxt1[1]=newtxt2[1]
    newtxt1[2]=newtxt2[2]
    newtxt1[3]=newtxt2[3]
    newtxt1[4]=newtxt2[4]

    deptxt=string.join(newtxt1,"\t")
    print (deptxt)
       #lengt=len(text)-4
    conllfile.write(deptxt)
    conllfile.write("\n")
       #Clear this section of the XML tree
      # element.clear()

       # if string.find(text,'VBP	')== 1:
        #   print("find")

infile.close()
outfile.close()
conllfile.close()

