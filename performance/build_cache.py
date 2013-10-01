#!/usr/bin/env python
# coding :utf-8

from indexer.indexer import *
from classifier.naivebayes import NaiveBayes
import cProfile

DBInterface.get_session()

NaiveBayes.set_categories(["earn", "acquisitions", "money-fx",
                           "grain", "crude", "trade",
                           "interest", "ship", "wheat", "corn"])

cProfile.run( 'result = NaiveBayes.build_cache()' )