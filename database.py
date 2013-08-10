#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

# config
DBNAME = 'sqlite:///index.sqlite'

engine = create_engine(DBNAME, echo=True)

Base = declarative_base()

#/* Base */
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word  = Column(String, index=True)
    count = Column(Integer, default=1)

    def __init__(self, word):
        self.word = word
        self.count = 1

    def __repl__(self):
        return self.word

    def count_inc(self):
        self.count += 1

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text =  Column(Text)
    category = Column(String)  

    def __init__(self, text, category):
        self.text = text
        self.category = category

class WordFeature(Base):
    __tablename__ = 'word_features'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))  
    document_id =  Column(Integer, ForeignKey('documents.id'))

    count = Column(Integer, default=1)
    document = relationship("Document", backref=backref('words'))
    word = relationship("Word")
   
    def __init__(self, text, count):
        self.text = text
        self.count = count
    
class DBInterface():
    @staticmethod
    def start_session():
        Session = sessionmaker(bind=engine) 
        return Session()
    
    @staticmethod
    def create_base():
        Base.metadata.create_all(engine)
    
    @staticmethod    
    def drop_base():
        Base.metadata.drop_all(engine)
