__author__ = 'majid'
# coding=utf-8
from math import ceil
import os
import sys
import subprocess
import datetime as dt
import xml.etree.ElementTree as ET

##################
#
# Formatting to CoNLL from XML format
#
##################

#infile = open("D:\PhD\PhD Tesis\Project\Enterprise Lexical\stanford-parser-full-2013-06-20\data\input.xml", 'r')
outfile = open("D:\PhD\PhD Tesis\Project\RepresentingSentences\stanford-corenlp-full-2015-01-29\data\QaldConll2013.conll", 'w')
XMLparhfile="D:/PhD/PhD Tesis/Project/RepresentingSentences/stanford-corenlp-full-2015-01-29/data/"
       #Create iterator over XML elements, don't store whole tree
xmlroot= ET.parse(XMLparhfile + 'Qald-inputstr2013.xml')
root = xmlroot.getroot()
#root= ET.fromstring(xmlroot)
print (root.tag)

for child in root:
    if child.tag == "document":
        root.tag="document"
        root = child
        print (root.tag)
        break

for child in root:
    print (child.tag)
    if child.tag == "sentences":
        root.tag="sentences"
        root = child
        print (root.tag)
        break



for element in root:
    print (element.tag)
    if element.tag == "sentence": #If we've read an entire sentence
      i = 1
      print (element.tag)
      #Output CoNLL style
      for word, lemma, pos, ner in zip(element.findall(".//word"),
                                                 element.findall(".//lemma"),
                                                 element.findall(".//POS"),
                                                 element.findall(".//NER")):


       outfile.write("%s\t%s\t%s\t%s\t%s" % (
                        i, word.text.encode('utf8'), lemma.text.encode('utf8'),
                        pos.text, ner.text))
       i += 1
       outfile.write("\n")
       #Clear this section of the XML tree
       element.clear()



