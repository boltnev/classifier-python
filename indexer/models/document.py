from sqlalchemy import Column, Text, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import exists
from indexer.indexer import *
from nltk.tokenize import RegexpTokenizer

VARCHARL = 256

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text =  Column(Text)
    category = Column(String(VARCHARL))  
    title = Column(String(VARCHARL))
    author = Column(String(VARCHARL))
    date  = Column(String(VARCHARL))
    indexed = Column(Boolean, default=False) 
    doc_type = Column(String(VARCHARL))

    def __init__(self, attributes):
        self.text = attributes.get('text', None)
        self.category = attributes.get('category', None)
        self.title = attributes.get('title', None)
        self.author = attributes.get('author', None)
        self.date  = attributes.get('date', None)
        self.doc_type = attributes.get('doc_type', None)

    def tokenize(self):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(self.text.decode('utf-8').lower())
    
    def word_dict(self):
        tokens = self.tokenize()
        token_dictionary = dict()
        for token in tokens:
            if token not in token_dictionary:
                token_dictionary[token] = 1
            else:
                token_dictionary[token] += 1
        return token_dictionary
        
    def word_to_index(self):
        s = DBInterface.get_session()
        token_dictionary = self.word_dict()
    
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
                    
    def index(self):
        s = DBInterface.get_session()
    
        self.word_to_index()
        self.indexed = True       
        s.commit()
        
        return self.indexed    
        
    @staticmethod
    def index_all():
        documents = DBInterface.get_session().query(Document).filter_by(indexed=False).all()
        for document in documents:
            document.index()
        
        
    
