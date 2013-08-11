from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class WordFeature(Base):
    __tablename__ = 'word_features'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))  
    document_id =  Column(Integer, ForeignKey('documents.id'))

    count = Column(Integer, default=1)
    document = relationship("Document", backref=backref('words'))
    word = relationship("Word")
   
    def __init__(self, document, word):
        self.document_id = document.id
        self.word_id = word.id
    