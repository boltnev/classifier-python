#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# config
DBCONF_DEFAULT = 'mysql+mysqldb://tclass:tclass@localhost/tclassifier'
# another options
#'sqlite:///index.sqlite'

Base = declarative_base()

class DBInterface():
    session = None
    engine = None
    
    @staticmethod
    def get_session(baseconf = DBCONF_DEFAULT):
        if DBInterface.engine is None:
            DBInterface.engine = create_engine(baseconf, echo=False)
        s = sessionmaker(bind=DBInterface.engine, expire_on_commit=False)
        Session = scoped_session(s)          
        DBInterface.session = Session()
        return Session()
    
    @staticmethod    
    def s_session(baseconf = DBCONF_DEFAULT):
        if DBInterface.engine is None:
            DBInterface.engine = create_engine(baseconf, echo=False)
        s = sessionmaker(bind=DBInterface.engine, expire_on_commit=False)
        Session = scoped_session(s)          
        return Session

    @staticmethod
    def stop_session(baseconf = DBCONF_DEFAULT):
        DBInterface.session = None
        
    @staticmethod
    def create_base(baseconf = DBCONF_DEFAULT):
        if DBInterface.engine is None:
            DBInterface.engine = create_engine(baseconf, echo=False) 
        Base.metadata.create_all(DBInterface.engine)
    
    @staticmethod    
    def drop_base(baseconf = DBCONF_DEFAULT):
        if DBInterface.engine is None:
            DBInterface.engine = create_engine(baseconf, echo=False) 
        Base.metadata.drop_all(DBInterface.engine)
        
    @staticmethod    
    def recreate_base(baseconf = DBCONF_DEFAULT):
        DBInterface.drop_base(baseconf)
        DBInterface.create_base(baseconf)
