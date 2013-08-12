#!/usr/bin/env python
from indexer.indexer import *
import unittest

test_text = """This is test text. This text is for text classifier test"""
    # text 3
    # text 2
    # is 2
    # this 2
    # for 1
    # classifier 1
test_class = "Testing"

class TestIndex(unittest.TestCase):
    def setUp(self):
        DBInterface.drop_base()
        DBInterface.create_base()
            
    def test_document(self):
        document = Document(test_text, test_class)
        s = DBInterface.start_session()
        s.add(document)
        s.commit()
        document.index()
        self.assertEqual(len(document.words), 6)

if __name__ == '__main__':
    unittest.main()