#/usr/bin/env python
# coding :utf-8
from test_db_conf import TEST_DBCONF
from indexer.indexer import *
from classifier.naivebayes import *
import unittest

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
Word.idf_all()

class TestNaiveBayes(unittest.TestCase):

    def test_build_cache(self):
        NaiveBayes.set_categories([category1, category2])
        cache = NaiveBayes.build_cache()
        self.assertEqual(cache["overall_word_count"], 31)
        self.assertEqual(cache["overall_doc_count"], 3)
        self.assertEqual(cache["Shakespeare"]["all"], 11)
        self.assertEqual(cache["Shakespeare"]["doc_count"], 1)
        self.assertEqual(cache["Testing"]["doc_count"], 2)
        self.assertEqual(cache["Testing"]["all"], 20)
        self.assertEqual(cache["Testing"][1], 2) # word "for"
        self.assertEqual(cache["Testing"][4], 3) # word "is"

    def test_all_categories(self):
        self.assertEqual(NaiveBayes.all_categories().sort(), [category1, category2].sort())

    def test_apriory(self):
        self.assertEqual(NaiveBayes.apriory(category1), float(2) / 3)
        self.assertEqual(NaiveBayes.apriory(category2), float(1) / 3)

    def test_get_words(self):
        all_words_count = len(NaiveBayes.get_words())
        self.assertEqual(all_words_count, 30)

    def test_likelihood(self):
        s = DBInterface.get_session()
        word = s.query(Word).filter_by(word="text").first()
        s.close()
        all_words_count = len(NaiveBayes.get_words())
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


    def test_apriory_f(self):
        NaiveBayes.set_categories([category1, category2])
        NaiveBayes.build_cache()
        self.assertEqual(NaiveBayes.apriory_f(category1), float(2) / 3)
        self.assertEqual(NaiveBayes.apriory_f(category2), float(1) / 3)

    def test_likelihood_f(self):
        NaiveBayes.set_categories([category1, category2])
        NaiveBayes.build_cache()
        s = DBInterface.get_session()
        word = s.query(Word).filter_by(word="text").first()
        s.close()
        all_words_count = NaiveBayes.cache["overall_word_count"]

        self.assertEqual(NaiveBayes.likelihood_f(word, category1), float(4) / (20 + all_words_count))
        self.assertEqual(NaiveBayes.likelihood_f(word, category2), float(2) / (11 + all_words_count))

    def test_aposteriory_f(self):
        NaiveBayes.set_categories([category1, category2])
        s = DBInterface.get_session()
        document = Document({'text':test_text, 'category':'', 'doc_type':'TEST'})
        s.add(document)
        s.commit()
        NaiveBayes.build_cache()
        s.close()
        document.index()
        self.assertGreater(NaiveBayes.aposteriory_f(category1, document), NaiveBayes.aposteriory_f(category2, document))


    def test_max_aposteriory(self):
        NaiveBayes.set_categories([category1, category2])
        s = DBInterface.get_session()
        document = Document({'text':test_text, 'category':'', 'doc_type':'TEST'})
        s.add(document)
        s.commit()
        NaiveBayes.build_cache()
        s.close()
        document.index()
        self.assertEqual(NaiveBayes.max_aposteriory(document), category1)

if __name__ == '__main__':
    unittest.main()
