#!/usr/bin/env python
#from nltk import tokenize
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

#/* Base */
class Word(Base):
  __tablename__ = 'words'
  id = Column(Integer, primary_key=True)
  word  = Column(String)
  count = Column(Integer)
  
  def __init__(self, word):
    self.word = word
    self.count = 1
  
  def __repl__(self):
    return self.word

