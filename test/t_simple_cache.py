#/usr/bin/env python
# coding :utf-8
from test_db_conf import TEST_DBCONF
from indexer.indexer import *
from cache import simple
import unittest

text1 = """This is test text. This text is for text classifier test"""
text2 = """software testing is good and useful for all mankind"""
category1 = "Testing"

text3 = """To be or not to be? that is the text question"""
category2 = "Shakespeare"

test_text = """I'm doing text processing unit test in python. I think it is very good""" # cat1

class TestSimpleCache(unittest.TestCase):
    database_prepared = False

    def setUp(self):
        if not TestSimpleCache.database_prepared:
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
        TestSimpleCache.database_prepared = True

    def test_set_words(self):
        cache = simple.Cache()
        words = ["word1", "word2", "word3"]
        cache.set_words(words)
        self.assertEqual(cache.words, words)

    def test_set_categories(self):
        cache = simple.Cache()
        categories = ["cat1", "cat2", "cat3"]
        cache.set_categories(categories)
        self.assertEqual(cache.categories , categories )

    def test_build_cache(self):
        cache = simple.Cache()
        cache.set_categories([category1, category2])
        s = DBInterface.get_session()
        words = s.query(Word).all()
        s.close()
        cache.set_words(words)
        cache.build()
        self.assertEqual(cache.storage["overall_word_count"], 31)
        self.assertEqual(cache.storage["overall_doc_count"], 3)
        self.assertEqual(cache.storage["Shakespeare"]["all"], 11)
        self.assertEqual(cache.storage["Shakespeare"]["doc_count"], 1)
        self.assertEqual(cache.storage["Testing"]["doc_count"], 2)
        self.assertEqual(cache.storage["Testing"]["all"], 20)
        self.assertEqual(cache.storage["Testing"][1], 2)
        self.assertEqual(cache.storage["Testing"][4], 3)

    def test_rebuild(self):
        cache = simple.Cache()
        cache.set_categories([category1, category2])
        s = DBInterface.get_session()
        words = s.query(Word).all()
        s.close()
        cache.set_words(words)
        cache.rebuild()
        self.assertEqual(cache.storage["overall_word_count"], 31)
        self.assertEqual(cache.storage["overall_doc_count"], 3)
        self.assertEqual(cache.storage["Shakespeare"]["all"], 11)
        self.assertEqual(cache.storage["Shakespeare"]["doc_count"], 1)
        self.assertEqual(cache.storage["Testing"]["doc_count"], 2)
        self.assertEqual(cache.storage["Testing"]["all"], 20)
        self.assertEqual(cache.storage["Testing"][1], 2)
        self.assertEqual(cache.storage["Testing"][4], 3)



if __name__ == '__main__':
    unittest.main()
