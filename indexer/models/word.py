from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

VARCHARL = 64

#/* Base */
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word  = Column(String(VARCHARL), index=True, unique=True)
    count = Column(Integer, default=1, index=True)

    def __init__(self, word, count = 1):
        self.word = word
        self.count = count

    def __repl__(self):
        return self.word

    def count_inc(self, n=1):
        self.count += n
