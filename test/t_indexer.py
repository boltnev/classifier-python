#!/usr/bin/env python
from indexer.indexer import *
import unittest

test_text = """This is test text. This text is for text classifier test"""
    # text 3
    # test 2
    # is 2
    # this 2
    # for 1
    # classifier 1
test_class = "Testing"

class TestIndex(unittest.TestCase):
    def setUp(self):
        DBInterface.recreate_base()
            
    def test_document(self):
        document = Document({'text':test_text, 'category':test_class})
        s = DBInterface.get_session()
        s.add(document)
        s.commit()
        s.expunge(document)
        self.assertEqual(document.index(), True)         
        
        document = s.query(Document).first()
        
        self.assertEqual(len(document.words), 6)
        
        for word_feature in document.words:
            if word_feature.word =="text":
                self.assertEqual(word_feature.count, 3)
            if word_feature.word =="test":
                self.assertEqual(word_feature.count, 2)
            if word_feature.word =="classifier":
                self.assertEqual(word_feature.count, 1)
        self.assertEqual(document.indexed, True)
        s.close()
        

    def test_locked_document(self):
        document = Document({'text':test_text, 'category':test_class})
        document.locked = True
        s = DBInterface.get_session()
        s.add(document)
        s.commit()
        s.expunge(document)
        self.assertEqual(document.index(), False)
        s.close()
        
    def test_index_all(self):
        document = Document({'text':test_text, 'category':test_class})
        s = DBInterface.get_session()
        s.add(document)      
        s.commit()
        s.expunge_all()                    
        
        s.close()
        s = DBInterface.get_session()        
        not_indexed = s.query(Document).filter_by(indexed=False).count()
        s.expunge_all()
        self.assertEqual(not_indexed, 1)
        
        Document.index_all()
        
        s.close()
        s = DBInterface.get_session()                
        not_indexed = s.query(Document).filter_by(indexed=False).count()
        s.expunge_all()
        s.close()
        self.assertEqual(not_indexed, 0)

    def test_test(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
