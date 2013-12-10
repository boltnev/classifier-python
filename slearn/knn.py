import 	bm

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

(documents, benchmark_documents) = bm.get_documents()
(corpus,y) = bm.build_corpus_and_categories(documents)
(test_corpus, test_y) = bm.build_corpus_and_categories(benchmark_documents)

vectorizer = TfidfVectorizer()
clf = KNeighborsClassifier()

bm.run(vectorizer, clf, corpus, y, test_corpus, test_y)