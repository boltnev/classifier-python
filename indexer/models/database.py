#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# config
DBNAME ='mysql+mysqldb://tclass:tclass@localhost/tclassifier'
# another options
#'sqlite:///index.sqlite'

engine = create_engine(DBNAME, echo=False)

Base = declarative_base()

class DBInterface():
    session = None
    @staticmethod
    def get_session():
        if DBInterface.session is None:
          s = sessionmaker(bind=engine)
          DBInterface.session = s()
        return DBInterface.session
    
    @staticmethod
    def stop_session():
        DBInterface.session = None
        
    @staticmethod
    def create_base():
        Base.metadata.create_all(engine)
    
    @staticmethod    
    def drop_base():
        Base.metadata.drop_all(engine)
        
    @staticmethod    
    def recreate_base():
        DBInterface.get_session().close()
        DBInterface.drop_base()
        DBInterface.create_base()