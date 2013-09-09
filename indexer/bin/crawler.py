from indexer.indexer import *
from os import path, getcwd, listdir
from os.path import join, isdir, isfile
import threading

class Crawler:
    threads = []
    
    def __init__(self, path):
        self.crawl_path = path
 
    def crawl(self):    
        for element in listdir(self.crawl_path):
            pwd = getcwd()
            if(isdir( join(self.crawl_path, element) )):
                self.crawl_dir(join(pwd, self.crawl_path), element)
        Document.index_all()
        
    def crawl_dir(self, path, d_class):   
        for element in listdir( join(path, d_class) ):
            if(isdir( join(path, element) )):
                self.crawl_dir(join(path, d_class, element), d_class)
            else:
                self.create_document(join(path, d_class, element), d_class)

    def create_document(self, path, d_class):
        file = open(path, 'r')
        text = repr(file.read())
        document = Document({'text':text, 'category':d_class})
        s = DBInterface.get_session()
        s.add(document)
        s.commit()
