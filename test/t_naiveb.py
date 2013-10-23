#/usr/bin/env python
# coding :utf-8
from test_db_conf import TEST_DBCONF
from indexer.indexer import *
from classifier import naivebayes
from config import gconf
import unittest

text1 = """This is test text. This text is for text classifier test"""
text2 = """software testing is good and useful for all mankind"""
category1 = "Testing"

text3 = """To be or not to be? that is the text question"""
category2 = "Shakespeare"
 
test_text = """I'm doing text processing unit test in python. I think it is very good""" # cat1

class TestNaiveBayes(unittest.TestCase):
    database_prepared = False

    def setUp(self):
        if not TestNaiveBayes.database_prepared:
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
            Word.idf_all()
            s = DBInterface.get_session()
            gconf.cache.set_words(s.query(Word).all())
            gconf.cache.set_categories([category1, category2])
            s.close
            gconf.cache.build()
        TestNaiveBayes.database_prepared = True


    def test_apriory(self):
        self.assertEqual(naivebayes.apriory(category1), float(2) / 3)
        self.assertEqual(naivebayes.apriory(category2), float(1) / 3)


    def test_likelihood(self):
        s = DBInterface.get_session()
        word = s.query(Word).filter_by(word="text").first()
        s.close()
        all_words_count = gconf.cache.storage["overall_word_count"]
        self.assertEqual(naivebayes.likelihood(word, category1), float(4) / (20 + all_words_count))
        self.assertEqual(naivebayes.likelihood(word, category2), float(2) / (11 + all_words_count))


    def test_aposteriory(self):
        s = DBInterface.get_session()
        document = Document({'text':test_text, 'category':'', 'doc_type':'TEST'})
        s.add(document)
        s.commit()
        s.close()
        document.index()
        self.assertGreater(naivebayes.aposteriory(category1, document), naivebayes.aposteriory(category2, document))

    def test_max_aposteriory(self):
        s = DBInterface.get_session()
        document = Document({'text':test_text, 'category':'', 'doc_type':'TEST'})
        s.add(document)
        s.commit()
        s.close()
        document.index()
        self.assertEqual(naivebayes.max_aposteriory(document), category1)

if __name__ == '__main__':
    unittest.main()
