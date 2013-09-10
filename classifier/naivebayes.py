#!/usr/bin/env python 
# coding :utf-8
from indexer.indexer import *

class NaiveBayes():

    def max_aposteriory(document):
        pass

    def aposteriory(category, document):
        pass

    @staticmethod
    def apriory(category_name):
        s = DBInterface.get_session()
        all_doc_count = s.query(Document).count()    
        category_count = s.query(Document).filter_by(category=category_name).count()
        result = float(category_count) / all_doc_count
        s.close()
        return result  
    
    @staticmethod
    def likelihood(word, category_name):
        s = DBInterface.get_session()
      
        sql = "select sum(`word_features`.count) from word_features " +  \
              "join `documents` on `documents`.id = `word_features`.document_id " + \
              "join `words` on `words`.id =`word_features`.word_id " + \
              "where word_id = %d and category='%s'; " % (word.id, category_name)

        word_category_count = s.execute(sql).scalar()
        
        sql = "select sum(`word_features`.count) from word_features " +  \
              "join `documents` on `documents`.id = `word_features`.document_id " + \
              "join `words` on `words`.id =`word_features`.word_id " + \
              "where category='%s'; " % (category_name,)

        all_category_count = s.execute(sql).scalar()

        result = float(word_category_count) / float(all_category_count) 
        
        s.close()
        return result 
