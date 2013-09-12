#/usr/bin/env python
# coding :utf-8
from indexer.indexer import *
from classifier.naivebayes import *
import unittest

text1 = """This is test text. This text is for text classifier test"""
text2 = """software testing is good and useful for all mankind"""
category1 = "Testing"

text3 = """To be or not to be? that is the text question"""
category2 = "Shakespeare"
 
test_text = """I'm doing text processing unit test in python. I think it is very good""" # cat1
DBInterface.recreate_base()

document1 = Document({'text':text1, 'category':category1, 'doc_type':'TRAIN'})
document2 = Document({'text':text2, 'category':category1, 'doc_type':'TRAIN'})
document3 = Document({'text':text3, 'category':category2, 'doc_type':'TRAIN'})
s = DBInterface.get_session()
s.add_all([document1, document2, document3])
s.commit()
s.expunge_all()
s.close()
Document.index_all() 

class TestNaiveBayes(unittest.TestCase):
            
    def test_apriory(self):
        self.assertEqual(NaiveBayes.apriory(category1), float(2) / 3)
        self.assertEqual(NaiveBayes.apriory(category2), float(1) / 3)
    
    def test_likehood(self):
        s = DBInterface.get_session()
        word = s.query(Word).filter_by(word="text").first()
        all_words_count = s.query(Word).count()
        s.close()
        self.assertEqual(NaiveBayes.likelihood(word, category1), float(4) / (20 + all_words_count))
        self.assertEqual(NaiveBayes.likelihood(word, category2), float(2) / (11 + all_words_count))

    def test_aposteriory(self):
        s = DBInterface.get_session()
        document = Document({'text':test_text, 'category':'', 'doc_type':'TEST'})
        s.add(document)
        s.commit()
        s.close()
        document.index()
        self.assertGreater(NaiveBayes.aposteriory(category1, document), NaiveBayes.aposteriory(category2, document))
      
    def test_all_categories(self):
        self.assertEqual(NaiveBayes.all_categories(), [category1, category2])

if __name__ == '__main__':
    unittest.main()
