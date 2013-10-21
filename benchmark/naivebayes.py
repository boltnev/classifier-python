#!/usr/bin/env python
# coding :utf-8

from indexer.indexer import *
from classifier.naivebayes import NaiveBayes
import cProfile

# ModApte Split corpus must be loaded at this moment

s = DBInterface.get_session()
docs = s.query(Document).filter_by(doc_type="TEST").all()
s.close()

NaiveBayes.set_categories(["earn", "acq", "money-fx",
                           "grain", "crude", "trade",
                           "interest", "ship", "wheat", "corn"])

NaiveBayes.build_cache()

right_answ = 0.0
i = 0
for doc in docs:
    i += 1
    category = NaiveBayes.max_aposteriory(doc)
    if (doc.category.find(category) >= 0):
        right_answ += 1.0
    print i, " of ", len(docs), " ", category, " => ", doc.category, " accuracy: ", right_answ / i

print "Result accuracy: ", right_answ / len(docs)