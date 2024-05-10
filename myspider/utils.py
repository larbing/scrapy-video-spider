import os
import time
import threading
import itertools
from hashlib import md5

from myspider.settings import IDDIR

"""
    Calculate the MD5 hash of the input string.

    Parameters:
    string (str): The input string to calculate the MD5 hash for.

    Returns:
    str: The MD5 hash of the input string.
"""
def md5_hash(string:str):
    return md5(string.encode('utf-8')).hexdigest()

class IncrementalIdGenerator:
    def __init__(self,max=5000, file_path=IDDIR):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.id_max   = max
        self.id_count = max
        self.id_index = int(time.time())
        self.id_step  = 1

        with self.lock:
            self.preallocate_ids()

    def preallocate_ids(self):
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
        if self.id_count < 1:
            self.preallocate_ids()

        self.id_count -=1
        return next(self.producer)
        
idGenerator = IncrementalIdGenerator()