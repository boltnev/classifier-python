import 	bm

from sklearn.linear_model import  LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

(documents, benchmark_documents) = bm.get_documents()
(corpus,y) = bm.build_corpus_and_categories(documents)
(test_corpus, test_y) = bm.build_corpus_and_categories(benchmark_documents)

#vectorizer = CountVectorizer(min_df=1)
vectorizer = TfidfVectorizer(min_df=1)

clf =  LogisticRegression()

bm.run(vectorizer, clf, corpus, y, test_corpus, test_y)