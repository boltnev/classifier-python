from sqlalchemy import Column, Text, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from indexer.models.database import DBInterface
from database import Base
import math
import indexer.models.document 
VARCHARL = 64

#/* Base */
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word  = Column(String(VARCHARL), index=True, unique=True)
    count = Column(Integer, default=1, index=True)
    idf   = Column(Float) 

    def __init__(self, word, count = 1):
        self.word = word
        self.count = count

    def __repl__(self):
        return self.word

    def count_inc(self, n=1):
        self.count += n
    
    def calculate_idf(self):
        D = indexer.models.document.Document
        s = DBInterface.get_session()
        all_docs_count = s.query(D).filter(D.indexed == True, D.doc_type=='TRAIN').count()
        this_word_count = s.execute("select sum(count) from word_features where word_id = %s" % self.id).scalar()
        return math.log(float(all_docs_count) / int(this_word_count) )
