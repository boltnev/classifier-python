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
      attributes['category'] = ",".join(categories)
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

def load_modapte_document(document, doc_type):
  attributes = dict()
  categories = list()
  if doc_type.find("train") >= 0:  
    attributes['doc_type'] = "TRAIN"
  elif doc_type.find("test") >= 0:
    attributes['doc_type'] = "TEST"

  for element in document: 
    if element.tag == 'category':
      st = element.text
      categories.append(st[st.find(".") + 1:])
    if element.tag == 'date':
      attributes['date'] = element.text
    if element.tag == 'title':
      attributes['title'] = element.text[0:127]
    if element.tag == 'author':
      attributes['author'] = element.text
    if element.tag == 'text':
      attributes['text'] = element.text
   
  attributes['category'] = ",".join(categories)
  s = DBInterface.get_session()
  document = Document(attributes)
  s.add(document)
  s.commit()
  s.close()

def load_corpus():
  i = 0
  for filename in filenames:
    tree = ET.parse(directory + filename)
    root = tree.getroot()
    for child in root:
      load_document(child)
      i = i + 1
  print i

def load_modapte():
  i = 0
  for filename in ['modapte/train.xml', 'modapte/test.xml']:
    tree = ET.parse(directory + filename)
    root = tree.getroot()
    print len(root)
    for child in root:
      load_modapte_document(child, filename)
      i = i + 1
  print i

 
