import string
import hashlib
import random


def randomString(size=20):
    chars= string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))

def randomName(n=30):
    s=randomString(n)
    hash_object = hashlib.sha1(s.encode())
    name=hash_object.hexdigest()
    #print("{} -> {}".format(s,name))
    nameAsNum=int(name,16)
    #print("number -> {}".format(nameAsNum))
    return str(nameAsNum)