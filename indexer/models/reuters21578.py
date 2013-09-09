#!/usr/bin/env python
# coding: utf-8
import xml.etree.ElementTree as ET
from indexer.indexer import Document, DBInterface

filenames = ['reut2-00' + str(i) + '.xml' for i in xrange(10)] + ['reut2-0' + str(i) + '.xml' for i in xrange(10, 22)]
directory = 'test/reuters21578/'

def load_document(document):
  attributes = dict()
  categories = list()
  attributes['doc_type'] = document.attrib['LEWISSPLIT']
  
  for child in document.findall("TEXT"):
    for element in child:
      if element.tag == 'TITLE':
        attributes['title'] = element.text
      if element.tag == 'AUTHOR':
        attributes['author'] = element.text
      if element.tag == 'BODY':
        attributes['text'] = element.text

  for element in document: 
    if element.tag == 'TOPICS':
      for topic in element:
        categories.append(topic.text)
      attributes['categories'] = ",".join(categories)
    if element.tag == 'DATE':
      attributes['date'] = element.text
  try:
    if attributes['text'] == "":
      return False
    
    s = DBInterface.get_session()
    document = Document(attributes)
    s.add(document)
    s.commit()
    s.close()
  except:
    return False    

def load_corpus():
  i = 0
  for filename in filenames:
    tree = ET.parse(directory + filename)
    root = tree.getroot()
    for child in root:
      load_document(child)
      i = i + 1
  print i
