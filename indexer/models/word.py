from sqlalchemy import Column, Text, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from indexer.models.database import DBInterface
from database import Base
import math
import indexer.models.document 
VARCHARL = 64
import threading

#/* Base */
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word  = Column(String(VARCHARL), index=True, unique=True)
    count = Column(Integer, default=1, index=True)
    idf   = Column(Float) 
    doc_count = Column(Integer, default=0, index=True)

    def __init__(self, word, count = 1):
        self.word = word
        self.count = count
        self.doc_count = 0

    def __repl__(self):
        return self.word

    def count_inc(self, n=1):
        self.count += n
    
    def calculate_idf(self):
        D = indexer.models.document.Document
        s = DBInterface.get_session()
        all_docs_count = s.query(D).filter(D.indexed == True, D.doc_type=='TRAIN').count()
        this_word_count = s.execute("select count(*) from word_features where word_id = %s" % self.id).scalar()
        self.idf = math.log(float(all_docs_count) / int(this_word_count))
        s.add(self)
        s.commit()
        s.close()
        return self.idf
    
    @staticmethod
    def idf_all():
      # s = DBInterface.get_session()
      #   words = s.query(Word).all()
      #   s.close()
      #   
      #   for word in words:
      #       word.calculate_idf()
        s = DBInterface.get_session()
        words = s.query(Word).all()
        s.close()
        thread_list = []
        for word in words:
          if len(thread_list) < 40:    
              th = threading.Thread(target=word.calculate_idf)
              th.start()
              thread_list.append(th)    
          else:
              for thread in thread_list:
                  thread.join()
                  thread_list = []
          for thread in thread_list:
              thread.join()
