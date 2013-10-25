#!/usr/bin/env python 
# coding :utf-8
from indexer.indexer import *
import math
cache = None
use_apriori = True


def max_aposteriori(document):
    previous = None
    result = None
    for category in cache.categories:
        if not previous:
            previous = aposteriori(category, document)
            result = category
        else:                
            new_value = aposteriori(category, document)
            if new_value >= previous:
                result = category
                previous = new_value
    return result


def apriori(category_name):
    if use_apriori:
        return float(cache.storage[category_name]["doc_count"]) / cache.storage["overall_doc_count"]
    else:
        return 1


def aposteriori(category_name, document):
    s = DBInterface.get_session()
    s.add(document)
    result = 0
    category_apriori = apriori(category_name)

    for word_obj in document.words:
        result += math.log(likelihood(word_obj.word, category_name))

    result *= category_apriori
    s.close()
    return result


def likelihood(word, category_name):
    all_words_count = cache.storage["overall_word_count"]
    word_category_count = cache.storage[category_name].get(word.id, 0)
    all_category_word_count = cache.storage[category_name]["all"]
    return float(word_category_count + 1) / float(all_category_word_count + all_words_count )



