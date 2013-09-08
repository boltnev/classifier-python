from indexer.indexer import DBInterface
from indexer.models import reuters21578 

class Reuters21578:     
    @staticmethod
    def load_corpus():
        reuters21578.load_corpus()
    
    def index_corpus():
        pass        
        
if __name__ == '__main__':
    DBInterface.recreate_base()
    Reuters21578.load_corpus()