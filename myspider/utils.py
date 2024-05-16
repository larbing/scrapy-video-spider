import os
import time
import threading
import itertools
from hashlib import md5

from myspider.settings import IDDIR

def md5_hash(string:str):
    return md5(string.encode('utf-8')).hexdigest()

class IncrementalIdGenerator:
    def __init__(self,max=1000, file_path=IDDIR):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.id_max   = max
        self.id_index = int(time.time())
        self.id_step  = 1
        self.preallocate_ids()

    def preallocate_ids(self):
        with self.lock:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    self.id_index = int(file.read())
            
            with open(self.file_path, 'w') as file:
                file.write(str(self.id_index + self.id_max))
        
            self.producer = self.infinite_producer()

    def infinite_producer(self):
        for id in itertools.count(self.id_index,self.id_step):
            yield id
    
    def get_id(self):
        new_id = next(self.producer)
        if new_id >= self.id_index + self.id_max:
            self.preallocate_ids()
        return new_id
        
idGenerator = IncrementalIdGenerator()