import json,os
import numpy as np
import pandas as pd

class Node(object):

    def __init__(self):
        self.descendants=None
        self.data=None
        self.name =''
        self.prefix=''




def readInChunks(fileObj, chunkSize=2048):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 2kB.
    """
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data

def data_handler(string_data,d):
    #print "data = {}".format(string_data)
    data = json.loads(string_data)
    name_subreddit = data['subreddit']
    if name_subreddit in d:
        d[name_subreddit]+=1
    else:
        d[name_subreddit] = 1
        print d

def main_fun(file_path):
    d={}
    ctr=0
    print ""
    if os.path.isfile(file_path) is False:
        raise "[Error] cant find the json file --> {}".format(file_path)
    with open(file_path) as f:
        for line in f:
            data_handler(line,d)
            print ctr
            ctr+=1
    print d


if __name__ == "__main__":
    path = '/home/eran/Downloads/RC_2018-01-23'
    main_fun(path)