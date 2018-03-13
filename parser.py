import json,os
import numpy as np
import pandas as pd

import walker

class Node(object):

    def __init__(self,id_node,id_father,n_author,data_i,text):
        self.descendants=None
        self.data=data_i
        self.i_id =id_node
        self.author=n_author
        self.father = id_father
        self.txt_data = text

gTree = {}
gAuthor = {}
def set_gTree(key,val):
    global gTree
    gTree[key]=val

def set_gAuthor(key,val):
    global gAuthor
    if key not in gAuthor:
        gAuthor[key]=[]
    gAuthor[key].append(val)



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
    id = data['link_id']
    permalink = data['permalink'] #need to contain the link id
    counter = 0
    if str(id).__contains__('7tu0ft'):
        tree_construct(data)
    return False


def main_fun(path): #7tu0ft
    d={}
    ctr=0
    print ""
    files_list = scaner(path)
    for p_path in files_list:
        with open(p_path) as f:
            for line in f:
                if data_handler(line,d):
                    ctr += 1
    make_tree()
    branc_dico = branching_factor()
    if 'ZeusThunder369' in gAuthor:
        list_comments = gAuthor['ZeusThunder369']
        for comm in list_comments:
            print gTree[comm].txt_data
            print '\n'*2
    print branc_dico
    print gTree
    print gAuthor

def tree_construct(json_data):
    parent_id = json_data['parent_id']
    link_data = json_data['permalink']
    author_name = json_data['author']
    id_link = json_data['link_id']
    id = json_data['id']
    text_data = json_data['body']
    node = Node(id,parent_id,author_name,json_data,text_data)
    if id in gTree:
        print "[Error] in {}".format(json_data)
    else:
        set_gTree(id, node)

def make_tree():
    for key in gTree:
        parent = gTree[key].father[3:]
        if parent in gTree:
            node_j = gTree[parent]
            if node_j.descendants is None:
                node_j.descendants={}
                node_j.descendants[key]=gTree[key]
            else:
                node_j.descendants[key] = gTree[key]
        author_name = gTree[key].author
        set_gAuthor(author_name,key)

def scaner(root_path):
    print ""
    obj_scanner =  walker.walker(root_path)
    out_file = obj_scanner.walk("RC")
    return out_file

def branching_factor():
    print ""
    d_factor={}
    for key_i in gTree:
        descendants = gTree[key_i].descendants
        if descendants is not None:
            d_factor[key_i] = len(descendants)
        else:
            d_factor[key_i]=0
    return d_factor



if __name__ == "__main__":
    path = '/home/ise/NLP/data_reddit/RC_2018-01-29'
    path = '/home/ise/NLP/data_reddit/'
    main_fun(path)