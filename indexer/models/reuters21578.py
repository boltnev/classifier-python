#!/usr/bin/env python
# coding: utf-8
import xml.etree.ElementTree as ET
from indexer.indexer import Document 

filenames = ['reut2-00' + str(i) + '.xml' for i in xrange(10)] + ['reut2-0' + str(i) + '.xml' for i in xrange(10, 22)]
directory = 'test/reuters21578/'

def load_document(document):
  print document.attrib
  for child in document.findall("TEXT"):
    for element in child:
      if element.tag == 'TITLE':
        print element.text
      
def load_corpus():
  i = 0
  for filename in filenames:
    tree = ET.parse(directory + filename)
    root = tree.getroot()
    for child in root:
      load_document(child)
      i = i + 1
  print i
