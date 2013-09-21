#!/usr/bin/env python 
# coding :utf-8
from indexer.indexer import *

class NaiveBayes():
    words = None

    def max_aposteriory(document):
        pass
    
    @staticmethod
    def get_words():
        if NaiveBayes.words is None:
          s = DBInterface.get_session()
          NaiveBayes.words = s.query(Word).from_statement("select * from words where count > 1 order by idf desc limit 100").all()
          s.close()
        return NaiveBayes.words
    
    @staticmethod
    def aposteriory(category_name, document):
        s = DBInterface.get_session()
        s.add(document)
        result = 0
        apriory = NaiveBayes.apriory(category_name)
        
        for word in NaiveBayes.get_words():
            result += apriory * NaiveBayes.likelihood(word, category_name)
        s.close()
        return result

    @staticmethod
    def apriory(category_name):
        s = DBInterface.get_session()
        all_doc_count = s.query(Document).filter_by(doc_type='TRAIN').count()    
        category_count = s.query(Document).filter_by(category=category_name, doc_type='TRAIN').count()
        result = float(category_count) / all_doc_count
        s.close()
        return result  
    
    @staticmethod
    def likelihood(word, category_name):
        s = DBInterface.get_session()
        
        # count word in category 
        sql = "select sum(`word_features`.count) from word_features " +  \
              "join `documents` on `documents`.id = `word_features`.document_id " + \
              "join `words` on `words`.id =`word_features`.word_id " + \
              "where word_id = %d and category LIKE '%s' AND `documents`.doc_type = 'TRAIN'; " % (word.id,"%" + category_name + "%")

        word_category_count = s.execute(sql).scalar()
        if word_category_count is None:
            word_category_count = 0
        # count of all words in category
        sql = "select sum(`word_features`.count) from word_features " +  \
              "join `documents` on `documents`.id = `word_features`.document_id " + \
              "join `words` on `words`.id =`word_features`.word_id " + \
              "where category LIKE '%s' AND `documents`.doc_type = 'TRAIN'; " % ("%" + category_name + "%",)

        all_category_word_count = s.execute(sql).scalar()
        if all_category_word_count is None:
            all_category_word_count = 0

        # all words collection count
        all_words_count = s.query(Word).count()
        
        result = float(word_category_count + 1) / float(all_category_word_count + all_words_count ) 
        
        s.close()
        return result

    @staticmethod
    def all_categories():
        s = DBInterface.get_session()
        query_result = s.execute("select distinct(category) from documents where doc_type = 'TRAIN';")
       
        categories = [list(category)[0] for category in query_result ]

        s.close()
        return categories      

 
