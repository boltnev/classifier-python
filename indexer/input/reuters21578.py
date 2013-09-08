from indexer.indexer import DBInterface, Document
from indexer.models import reuters21578 
import time

class Reuters21578:     
    @staticmethod
    def load_corpus():
        reuters21578.load_corpus()
    
    @staticmethod
    def index_corpus():
        Document.index_all()        
        
if __name__ == '__main__':
    DBInterface.recreate_base()
    start = time.time()
    Reuters21578.load_corpus()
    Reuters21578.index_corpus()
    print 'Reuters corpus loading and indexing took ', time.time() - start, ' seconds'