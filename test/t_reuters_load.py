#!/usr/bin/env python
# coding: utf-8
from indexer.models import reuters21578 
from indexer.indexer import DBInterface
import unittest

class TestIndex(unittest.TestCase):
  def setUp(self):
    DBInterface.drop_base()
    DBInterface.create_base()
            
  def test_document(self):
    reuters21578.load_corpus()
        
if __name__ == '__main__':
  unittest.main()
