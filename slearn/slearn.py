#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from indexer.indexer import *
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

s = DBInterface.get_session()
documents = s.query(Document).filter_by(doc_type="TRAIN")
benchmark_documents = s.query(Document).filter_by(doc_type="TEST")
s.close()


def build_corpus_and_categories(documents):
    corpus_dict = {}
    for doc in documents:
        for category in doc.category.split(","):
            corpus_dict[doc.text] = category

    corpus = [text for text in corpus_dict]


    y = np.array([corpus_dict[text] for text in corpus_dict])

    return (corpus, y)

(corpus,y) = build_corpus_and_categories(documents)
(test_corpus, test_y) = build_corpus_and_categories(benchmark_documents)
print len(y)


vectorizer = CountVectorizer(min_df=1)

X = vectorizer.fit_transform(corpus)
TEST_X = vectorizer.transform(test_corpus)

clf = MultinomialNB(alpha=1)
clf.fit(X, y)

right_answ = 0.0

for i in xrange(0, len(test_corpus)):
    if test_y[i] in clf.predict(TEST_X[i]):
        right_answ += 1.0

    print i, " of ", len(test_corpus), " ", test_y[i], " => ", clf.predict(TEST_X[i]), " accuracy: ", right_answ / (i + 1)

print "Result accuracy: ", right_answ / len(test_corpus)
