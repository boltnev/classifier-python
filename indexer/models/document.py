from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import exists
from indexer.indexer import *
from nltk.tokenize import RegexpTokenizer

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text =  Column(Text)
    category = Column(String)  

    def __init__(self, text, category):
        self.text = text
        self.category = category

    def tokenize(self):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(self.text.decode('utf-8').lower())
        
    def index(self):
        tokens = self.tokenize()
        token_dictionary = dict()
        for token in tokens:
            if token not in token_dictionary:
                token_dictionary[token] = 1
            else:
                token_dictionary[token] += 1
        s = DBInterface.start_session()
        
        for token in token_dictionary.keys():
            if(s.query(Word).filter_by(word=token).count() == 0 ):
                word = Word(token, token_dictionary[token])
                s.add(word)
            else:
                word = s.query(Word).filter_by(word=token).first()
                word.count_inc(token_dictionary[token])
            s.commit()            
            word_feature = WordFeature(self, word, token_dictionary[token])
            
            s.add(word_feature)
        s.commit()
    