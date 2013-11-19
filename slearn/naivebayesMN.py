import 	bm

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer

(documents, benchmark_documents) = bm.get_documents()
(corpus,y) = bm.build_corpus_and_categories(documents)
(test_corpus, test_y) = bm.build_corpus_and_categories(benchmark_documents)

vectorizer = CountVectorizer(min_df=1)
clf = MultinomialNB(alpha=0.1)
#clf = BernoulliNB()
bm.run(vectorizer, clf, corpus, y, test_corpus, test_y)