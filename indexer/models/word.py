from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

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