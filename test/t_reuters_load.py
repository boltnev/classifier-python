#!/usr/bin/env python
# coding: utf-8
from indexer.input.reuters21578 import Reuters21578  
from indexer.indexer import DBInterface, Document
import unittest

class TestIndex(unittest.TestCase):
  def setUp(self):
    DBInterface.recreate_base()
            
  def test_load_corpus(self):
    Reuters21578.load_corpus()
    count = DBInterface.get_session().query(Document).count()
    self.assertEqual(count, 21578)
        
if __name__ == '__main__':
  unittest.main()
