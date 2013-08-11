from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text =  Column(Text)
    category = Column(String)  

    def __init__(self, text, category):
        self.text = text
        self.category = category
