#/usr/bin/env python
# coding :utf-8
from indexer.indexer import *
from classifier.naivebayes import *
import unittest

test_text1 = """This is test text. This text is for text classifier test"""
test_text2 = """software testing is good and useful for all mankind"""
test_category1 = "Testing"

test_text3 = """To be or not to be? that is the text question"""
test_category2 = "Shakespeare"
 
DBInterface.recreate_base()

document1 = Document({'text':test_text1, 'category':test_category1})
document2 = Document({'text':test_text2, 'category':test_category1})
document3 = Document({'text':test_text3, 'category':test_category2})
s = DBInterface.get_session()
s.add_all([document1, document2, document3])
s.commit()
s.expunge_all()
s.close()
 

class TestNaiveBayes(unittest.TestCase):
            
    def test_apriory(self):
        self.assertEqual(NaiveBayes.apriory(test_category1), float(2) / 3)
        self.assertEqual(NaiveBayes.apriory(test_category2), float(1) / 3)


if __name__ == '__main__':
    unittest.main()
