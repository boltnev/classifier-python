#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# config
DBNAME = 'sqlite:///index.sqlite'

engine = create_engine(DBNAME, echo=False)

Base = declarative_base()

from document import Document
from word_feature import WordFeature
from word import Word

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
