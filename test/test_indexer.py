#!/usr/bin/env python
import unittest
from indexer import *

class TestDatabase(unittest.TestCase):
    def setUp(self):
        DBInterface.drop_base()
        DBInterface.create_base()
            
    def test_document():
        "pending"

if __name__ == '__main__':
    unittest.main()