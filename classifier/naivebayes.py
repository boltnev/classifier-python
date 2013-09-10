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

    def likelihood(document, category):
        pass
