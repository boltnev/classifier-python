#!/usr/bin/env python
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from indexer.indexer import *
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        DBInterface.drop_base()
        DBInterface.create_base()
            
    def test_create_word(self):
        word = Word("test")
        s = DBInterface.start_session()
        s.add(word)
        s.commit()
        count = s.query(Word).filter_by(word="test").count()
        self.assertEqual(count, 1)
        
    def test_inc_word_count(self):
        word = Word("test")
        s = DBInterface.start_session()
        s.add(word)
        s.commit()
        word.count_inc()
        s.commit()
        testword = s.query(Word).filter_by(word="test").first()
        self.assertEqual(testword.count, 2)
    
        
    def test_create_document(self):
        document = Document("text is text", "Test")
        s = DBInterface.start_session()
        s.add(document)
        s.commit()
        count = s.query(Document).filter_by(text="text is text", category="Test").count()
        self.assertEqual(count, 1)
        
    def test_create_word_feature(self):
        document = Document("text is text", "Test")
        s = DBInterface.start_session()
        word = Word("text")
        s = DBInterface.start_session()
        s.add_all([word, document])
        s.commit()
        wfeature = WordFeature(document, word)
if __name__ == '__main__':
    unittest.main()