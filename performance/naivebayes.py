#!/usr/bin/env python 
# coding :utf-8

from indexer.indexer import *
from classifier.naivebayes import NaiveBayes
import cProfile

s = DBInterface.get_session()
doc = s.query(Document).filter_by(doc_type="TEST").first()
s.close()


# prepare words for classifier
cProfile.run( 'result = NaiveBayes.aposteriory(doc.category, doc)' )

print result

