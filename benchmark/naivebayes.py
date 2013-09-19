#!/usr/bin/env python 
# coding :utf-8

from indexer.indexer import *
from classifier.naivebayes import NaiveBayes
import cProfile
# prepare words for classifier
cProfile.run( 'Word.idf_all()' )


