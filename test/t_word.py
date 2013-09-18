#/usr/bin/env python
# coding :utf-8
from test_db_conf import TEST_DBCONF
from indexer.indexer import *
from classifier.naivebayes import *
import unittest
import math 
text1 = """This is test text. This text is for text classifier test"""
text2 = """software testing is good and useful for all mankind"""
category1 = "Testing"

text3 = """To be or not to be? that is the text question"""
category2 = "Shakespeare"
 
test_text = """I'm doing text processing unit test in python. I think it is very good""" # cat1
DBInterface.recreate_base(TEST_DBCONF)

document1 = Document({'text':text1, 'category':category1, 'doc_type':'TRAIN'})
document2 = Document({'text':text2, 'category':category1, 'doc_type':'TRAIN'})
document3 = Document({'text':text3, 'category':category2, 'doc_type':'TRAIN'})
s = DBInterface.get_session()
s.add_all([document1, document2, document3])
s.commit()
s.expunge_all()
s.close()
Document.index_all() 

class TestWord(unittest.TestCase):
    def test_idf(self):
        s = DBInterface.get_session()
        word = s.query(Word).filter_by(word="this").one()
        s.close()
        self.assertEqual(word.calculate_idf(), math.log( float(3) / 2) )
   
if __name__ == '__main__':
    unittest.main()
