''' List of helper functions for CCD server '''

import hashlib
import time

def generate_key():
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))

    return hash.hexdigest()

if __name__ == '__main__':
    generate_apikey()
