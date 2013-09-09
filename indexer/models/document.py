from sqlalchemy import Column, Text, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from indexer.indexer import *
from nltk.tokenize import RegexpTokenizer
import threading

VARCHARL = 256

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text =  Column(Text)
    category = Column(String(VARCHARL), index=True)  
    title = Column(String(VARCHARL), index=True )
    author = Column(String(VARCHARL), index=True)
    date  = Column(String(VARCHARL), index=True)
    indexed = Column(Boolean, default=False, index=True) 
    word_count = Column(Integer)
    uniq_words = Column(Integer)
    doc_type = Column(String(VARCHARL), index=True)

    threads = []
    
    def __init__(self, attributes):
        self.text = attributes['text']
        self.category = attributes.get('category', None)
        self.title = attributes.get('title', None)
        self.author = attributes.get('author', None)
        self.date  = attributes.get('date', None)
        self.doc_type = attributes.get('doc_type', None)
        self.word_count = len(self.tokenize())
        self.uniq_words = len(set(self.tokenize()))
        
    def tokenize(self):
        tokenizer = RegexpTokenizer(r'\w+')
        if self.text:
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
        
    def get_word(self, s, token_dictionary, token):
        word = s.query(Word).filter_by(word=token).first() 
        if( word == None ):
            word = Word(token, token_dictionary[token])
            s.add(word)
            s.commit()
            
        return word

    def word_to_index(self, s):
        token_dictionary = self.word_dict()
    
        for token in token_dictionary.keys():
            word = self.get_word(s, token_dictionary, token)              
            
            word_feature = WordFeature(self, word, token_dictionary[token])
            
            s.add(word_feature)
        s.commit()
                    
    def index(self):
        if self.indexed:
          return True
        s_session = DBInterface.s_session()
        s = s_session()

        try:
            self.word_to_index(s)
        # Not obvious hack for avoiding of multithreading errors 
        except (IntegrityError, InvalidRequestError):
            return False
 
        self.indexed = True
        s.add(self)
        s.commit()
        
        s.expunge_all()
        s.close()
        s_session.remove()
        return self.indexed    
        
    @staticmethod
    def index_all():
        while(DBInterface.get_session().query(Document).filter_by(indexed=False).count() > 0):
           s_session = DBInterface.s_session()
           s = s_session
           documents = s.query(Document).filter_by(indexed=False).limit(120).all()
           s.expunge_all()
           s.close()
           s_session.remove()
           if len(documents) < 40:
               for document in documents:
                   document.index()
                   
           for document in documents:
               if len(Document.threads) < 40:    
                   th = threading.Thread(target=document.index)
                   th.start()
                   Document.threads.append(th)    
               else:
                   for thread in Document.threads:
                       thread.join()
                       Document.threads = []
           for thread in Document.threads:
               thread.join()
           Document.threads = []
        
      
 
