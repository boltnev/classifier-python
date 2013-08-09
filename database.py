#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, String
from sqlalchemy.orm import sessionmaker

# config
DBNAME = 'sqlite:///index.sqlite'

engine = create_engine(DBNAME, echo=True)

Base = declarative_base()

#/* Base */
class Word(Base):
  __tablename__ = 'words'
  id = Column(Integer, primary_key=True)
  word  = Column(String, index=True)
  count = Column(Integer)
  
  def __init__(self, word):
    self.word = word
    self.count = 1
  
  def __repl__(self):
    return self.word

  def count_inc():
    self.count += 1

#/* Base */
class Document(Base):
  __tablename__ = 'documents'
  id = Column(Integer, primary_key=True)
  text =  Column(Text)
  category = Column(String)

  def __init__(self, text, category):
    self.text = text
    self.category = category

class DBInterface():
  def start_session(self):
    Session = sessionmaker(bind=engine) 
    return Session()
    
  def create_base(self):
    Base.metadata.create_all(engine)

  def drop_base(self):
    Base.metadata.drop_all(engine)
