#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# config
DBNAME ='mysql+mysqldb://tclass:tclass@localhost/tclassifier'
# another options
#'sqlite:///index.sqlite'

engine = create_engine(DBNAME, echo=True)

Base = declarative_base()

class DBInterface():
    session = None
    @staticmethod
    def start_session():
        if DBInterface.session is None:
          DBInterface.session = sessionmaker(bind=engine) 
        return DBInterface.session()
    
    @staticmethod
    def create_base():
        Base.metadata.create_all(engine)
    
    @staticmethod    
    def drop_base():
        Base.metadata.drop_all(engine)
