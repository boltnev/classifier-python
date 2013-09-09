from sqlalchemy import Column, Text, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from database import Base

class WordFeature(Base):
    __tablename__ = 'word_features'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'), index=True)  
    document_id =  Column(Integer, ForeignKey('documents.id'), index=True)

    count = Column(Integer, default=1)
    document = relationship("Document", backref=backref('words'))
    word = relationship("Word")
    
    UniqueConstraint("word_id", "document_id")
   
    def __init__(self, document, word, count=1):
        self.document_id = document.id
        self.word_id = word.id
        self.count = count
    
    def count_inc(self, n=1):
        self.count += n
