#!/usr/bin/env python
# coding :utf-8
import cProfile

from indexer.indexer import *
from classifier.naivebayes import NaiveBayes

s = DBInterface.get_session()
doc = s.query(Document).filter_by(doc_type="TEST").first()
s.close()

NaiveBayes.set_categories(["earn", "acquisitions", "money-fx",
                           "grain", "crude", "trade",
                           "interest", "ship", "wheat", "corn"])
NaiveBayes.build_cache()

# prepare words for classifier
cProfile.run( 'result = NaiveBayes.aposteriory_f(doc.category, doc)' )

print result