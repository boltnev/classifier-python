#!/usr/bin/env python
from indexer.indexer import *
from test_db_conf import TEST_DBCONF
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        DBInterface.recreate_base(TEST_DBCONF)
                            
    def test_create_document(self):
        document = Document({'text':"text is text", 'category':"Test", 'date':"17" })
        document.train = True
        s = DBInterface.get_session()
        s.add(document)
        s.commit()
        documents = s.query(Document).filter_by(text="text is text", category="Test").all()
        count = len(documents)
        self.assertEqual(count, 1)
        doc = documents[0]
        self.assertEqual(doc.train, True)
        self.assertEqual(document.word_count, 3)
        self.assertEqual(document.uniq_words, 2)        
        s.close()

    def test_create_word_feature(self):
        document = Document({'text':"text is text", 'category':"Test", 'date':"17" })
        s = DBInterface.get_session()
        word = Word("text")
        s = DBInterface.get_session()
        s.add_all([word, document])
        s.commit()
        wfeature = WordFeature(document, word)
        s.add(wfeature)
        s.commit()
        self.assertEqual(document.words[0], wfeature)
        self.assertEqual(word, wfeature.word)        
        s.close()

    def test_create_word(self):
        word = Word("test")
        s = DBInterface.get_session()
        s.add(word)
        s.commit()
        count = s.query(Word).filter_by(word="test").count()
        self.assertEqual(count, 1)
        s.close()
        
    def test_inc_word_count(self):
        word = Word("test")
        s = DBInterface.get_session()
        s.add(word)
        s.commit()
        word.count_inc()
        s.commit()
        testword = s.query(Word).filter_by(word="test").first()
        self.assertEqual(testword.count, 2)    
        s.close()

if __name__ == '__main__':
    unittest.main()
