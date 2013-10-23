from indexer.indexer import DBInterface
from sqlalchemy import text


class Cache():
    def __init__(self):
        self.words = []
        self.categories = []
        self.storage = {}

    def set_categories(self, categories):
        self.categories = categories

    def set_words(self, words):
        self.words = words

    def build_word_cache(self):
        words_in_brackets = "(" + ", ".join([str(int(word.id)) for word in self.words]) + ")"

        cache_sql = \
            "SELECT sum(`word_features`.count) as word_count, word_id FROM `documents` " \
            "JOIN `word_features` on `documents`.id = `word_features`.document_id " \
            "WHERE word_id IN %s AND " \
            "doc_type='TRAIN' AND " \
            "category LIKE :category GROUP BY `word_features`.word_id" % (words_in_brackets,)

        e = DBInterface.engine

        overall_word_count = 0
        for category in self.categories:
            self.storage[category] = {}
            all_category_words = 0
            sql_result = e.execute(text(cache_sql), category="%" + category + "%")
            for row in sql_result:
                row_dict = dict(row)
                all_category_words += long(row_dict[u'word_count'])
                self.storage[category][row_dict[u'word_id']] = long(row_dict[u'word_count'])
            self.storage[category]["all"] = all_category_words
            overall_word_count += all_category_words
        self.storage["overall_word_count"] = long(overall_word_count)

    def build_doc_cache(self):
        e = DBInterface.engine
        cache_sql = "SELECT * FROM `documents` " \
                    "WHERE doc_type='TRAIN' AND " \
                    "category LIKE :category"
        self.storage["overall_doc_count"] = 0
        for category in self.categories:
            sql_result = e.execute(text(cache_sql), category="%" + category + "%")
            self.storage[category]["doc_count"] = sql_result.rowcount
            self.storage["overall_doc_count"] += sql_result.rowcount

    def build(self):
        self.build_word_cache()
        self.build_doc_cache()
        return self.storage

    def rebuild(self):
        self.storage = {}
        self.build()