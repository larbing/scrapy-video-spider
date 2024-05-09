import os
import time
import threading
from hashlib import md5

from myspider.settings import ID_PATH

"""
    Calculate the MD5 hash of the input string.

    Parameters:
    string (str): The input string to calculate the MD5 hash for.

    Returns:
    str: The MD5 hash of the input string.
"""
def md5_hash(string:str):
    return md5(string.encode('utf-8')).hexdigest()

def generate_incremental_id(file_path=ID_PATH):
    lock = threading.Lock()

    def get_current_id():
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                current_id = int(file.read())
        else:
            current_id = int(time.time())
        return current_id

    def update_id(new_id,inc=1):
        new_id += inc
        with open(file_path, 'w') as file:
            file.write(str(new_id))

    with lock:
        current_id = get_current_id()
        update_id(current_id)

    return current_id