import json,os
import numpy as np
import pandas as pd
import pickle
import walker

class Node(object):

    def __init__(self,id_node,id_father,data_i):
        self.descendants=None
        self.data=data_i
        self.i_id =id_node
        self.father = id_father


class Collection_object(object):

    def __init__(self):
        self.authore={}
        self.threads={}
        self.subReddit={}


def scaner(root_path):
    print ""
    obj_scanner =  walker.walker(root_path)
    out_file = obj_scanner.walk("RC")
    return out_file


def build_tree(gTree):
    for key in gTree:
        parent = gTree[key].father
        if parent in gTree:
            node_j = gTree[parent]
            if node_j.descendants is None:
                node_j.descendants={}
                node_j.descendants[key]=gTree[key]
            else:
                node_j.descendants[key] = gTree[key]


def data_handler(data_string,threads,d_collection):
    data = json.loads(data_string) #warp in try and catch
    name_subreddit = data['subreddit']
    id = str(data['link_id'][3:])
    permalink = data['permalink'] #need to contain the link id
    if id in threads:
        insert_data(data,d_collection)
    #build_tree(d_collection)


def branching_factor(gTree):
    print ""
    d_factor={}
    for key_i in gTree:
        descendants = gTree[key_i].descendants
        if descendants is not None:
            d_factor[key_i] = len(descendants)
        else:
            d_factor[key_i]=0
    return d_factor


def insert_data(data_json,d_coll):
    thread_ID = str(data_json['link_id'][3:])
    comment_ID = str(data_json['id'])
    id_author = str(data_json['author'])
    sub_reddit_id = str(data_json['subreddit_id'][3:])
    parent_id = str(data_json['parent_id'][3:])
    if thread_ID not in d_coll.threads:
        d_coll.threads[thread_ID ]={}
    d_coll.threads[thread_ID][comment_ID]=Node(id,parent_id,data_json)
    #Authors Data
    if id_author not in d_coll.authore:
        d_coll.authore[id_author]={'threads':{},'sub_reddit':{}}
    if thread_ID not in d_coll.authore[id_author]['threads']:
        d_coll.authore[id_author]['threads'][thread_ID ]=[]
    d_coll.authore[id_author]['threads'][thread_ID].append(comment_ID)
    if sub_reddit_id not in d_coll.authore[id_author]['sub_reddit']:
        d_coll.authore[id_author]['sub_reddit'][sub_reddit_id]={thread_ID:0}
    d_coll.authore[id_author]['sub_reddit'][sub_reddit_id][thread_ID]+=1
    # inset to Sub-Reddit
    if sub_reddit_id not in d_coll.subReddit:
        d_coll.subReddit[sub_reddit_id]=set()
    d_coll.subReddit[sub_reddit_id].add(thread_ID)


def dump_pickle(object,path):
    if os.path.isdir(path):
        pickle.dump(object, open( "{}/save.p".format(path), "wb" ))
    else:
        print "[Error] dir path is not valid , {}".format(path)

def load_pickle(path_file):
    if os.path.isfile(path_file):
        return pickle.load(open(path_file, "rb"))
    else:
        print "[Error] path file is not valid , {}".format(path)


def init_function(p_path_root,threads_target,d=None):
    if d is None:
        d_collection = Collection_object()
    else:
        d_collection = d
    ctr=0
    files = scaner(p_path_root)
    files = [p_path_root]
    for p in files:
        with open(p) as f:
            for line in f:
                data_handler(line,threads_target,d_collection)
                ctr+=1
                print ctr
        break
    for ky in d_collection.threads:
        build_tree(d_collection.threads[ky])
    dump_pickle(d_collection,'/home/ise/NLP/')


if __name__ == "__main__":
    path = '/home/ise/NLP/data_reddit/RC_2018-01-29'
    target_threads=['7tu0ft','7tiliz','7tktlm']
    d = load_pickle('/home/ise/NLP/save.p')
    print ""
    init_function(path,target_threads)
