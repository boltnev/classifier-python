#!/usr/bin/env python
from indexer.indexer import *
from test_db_conf import TEST_DBCONF
from indexer.bin.crawler import Crawler 
import unittest

test_path = 'test/test_data'

class TestCrawler(unittest.TestCase):
    def setUp(self):
        DBInterface.recreate_base(TEST_DBCONF)
        
    def test_create(self):
        crawler = Crawler(test_path)
        crawler.crawl()

if __name__ == '__main__':
    unittest.main()
