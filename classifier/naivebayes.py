#!/usr/bin/env python 
# coding :utf-8
from config.gconf import cache
from indexer.indexer import *


def max_aposteriory(document):
    previous = 0
    result = None
    for category in cache.categories:
        if aposteriory(category, document) >= previous:
            result = category
            previous = aposteriory
    return result


def apriory(category_name):
    return float(cache.storage[category_name]["doc_count"]) / cache.storage["overall_doc_count"]


def aposteriory(category_name, document):
    s = DBInterface.get_session()
    s.add(document)
    result = 0
    category_apriory = apriory(category_name)

    for word_obj in document.words:
        result += category_apriory * likelihood(word_obj.word, category_name)
    s.close()
    return result


def likelihood(word, category_name):
    all_words_count = cache.storage["overall_word_count"]
    word_category_count = cache.storage[category_name].get(word.id, 0)
    all_category_word_count = cache.storage[category_name]["all"]
    return float(word_category_count + 1) / float(all_category_word_count + all_words_count )



