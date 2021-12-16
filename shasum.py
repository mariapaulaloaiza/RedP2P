import hashlib

def shasum(data):
    
    sha1 = hashlib.sha1()

    shaNum = sha1.hexdigest()

    return int(shaNum,16)
