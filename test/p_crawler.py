#!/usr/bin/env python
from indexer.indexer import *
from test_db_conf import TEST_DBCONF
from indexer.bin.crawler import Crawler 
import unittest
import cProfile


test_path = 'test/test_data'

class TestProfileCrawler(unittest.TestCase):
    def setUp(self):
        DBInterface.recreate_base(TEST_DBCONF)
        
    def test_create(self):
        cProfile.run('Crawler(test_path).crawl()')
        

if __name__ == '__main__':
    unittest.main()
