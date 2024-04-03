from hashlib import md5


"""
    Calculate the MD5 hash of the input string.

    Parameters:
    string (str): The input string to calculate the MD5 hash for.

    Returns:
    str: The MD5 hash of the input string.
"""
def md5_hash(string:str):
    return md5(string.encode('utf-8')).hexdigest()