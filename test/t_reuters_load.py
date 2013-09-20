#!/usr/bin/env python
# coding: utf-8
from test_db_conf import TEST_DBCONF
from indexer.input.reuters21578 import Reuters21578  
from indexer.indexer import DBInterface, Document
import unittest

class TestIndex(unittest.TestCase):
  def setUp(self):
    DBInterface.recreate_base(TEST_DBCONF)
            
  def xtest_load_corpus(self):
    Reuters21578.load_corpus()
    count = DBInterface.get_session().query(Document).count()
    self.assertEqual(count, 21578)
       
  def test_load_modapte(self):
    Reuters21578.load_modapte()
    count = DBInterface.get_session().query(Document).count()
    self.assertEqual(count, 10788)
 
if __name__ == '__main__':
  unittest.main()
