#!/usr/bin/env python
# coding :utf-8

from indexer.indexer import *
from classifier import naivebayes
from cache import simple
from config import gconf

import cProfile

# ModApte Split corpus must be loaded at this moment

s = DBInterface.get_session()
docs = s.query(Document).filter_by(doc_type="TEST").all()
words = s.query(Word).all()
s.close()

cache = simple.Cache()

cache.set_categories(["earn", "acq", "money-fx",
                      "grain", "crude", "trade",
                      "interest", "ship", "wheat", "corn"])
cache.set_words(words)

cache.build()

naivebayes.cache = cache

naivebayes.use_apriori = False

right_answ = 0.0
i = 0
for doc in docs:
    i += 1
    category = naivebayes.max_aposteriori(doc)
    if doc.category.find(category) >= 0:
        right_answ += 1.0
    print i, " of ", len(docs), " ", category, " => ", doc.category, " accuracy: ", right_answ / i

print "Result accuracy: ", right_answ / len(docs)