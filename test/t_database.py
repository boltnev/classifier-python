#!/usr/bin/env python
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
        document.train = True
        s = DBInterface.start_session()
        s.add(document)
        s.commit()
        documents = s.query(Document).filter_by(text="text is text", category="Test").all()
        count = len(documents)
        self.assertEqual(count, 1)
        doc = documents[0]
        self.assertEqual(doc.train, True)

    def test_create_word_feature(self):
        document = Document("text is text", "Test")
        s = DBInterface.start_session()
        word = Word("text")
        s = DBInterface.start_session()
        s.add_all([word, document])
        s.commit()
        wfeature = WordFeature(document, word)
        s.add(wfeature)
        s.commit()
        self.assertEqual(document.words[0], wfeature)
        self.assertEqual(word, wfeature.word)        

if __name__ == '__main__':
    unittest.main()
