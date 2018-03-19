# encoding=utf8
import json,os
import numpy as np
import pandas as pd
import pickle,hashlib
import walker

class Node(object):

    def __init__(self,id_node,id_father,data_i):
        self.descendants=None
        self.data=data_i
        self.i_id =id_node
        self.father = id_father

    def node_to_json(self):
        json_d={}
        json_d['father']=str(self.father)
        #json_d['i_id'] = str(self.i_id)
        json_d['data'] = self.data
        arr=[]
        if self.descendants is not None:
            for ky in self.descendants.keys():
                arr.append(ky)
        json_d['descendants'] = arr
        return json_d


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
    parent_id = str(data_json['parent_id'][3:])
    if thread_ID not in d_coll.threads:
        d_coll.threads[thread_ID ]={}
    d_coll.threads[thread_ID][comment_ID]=Node(id,parent_id,data_json)
    if id_author not in d_coll.authore:
        d_coll.authore[id_author]={'threads':{},'sub_reddit':{}}
    if thread_ID not in d_coll.authore[id_author]:
        d_coll.authore[id_author][thread_ID]=[]
    d_coll.authore[id_author][thread_ID].append(comment_ID)

def dump_pickle(object,path):
    if os.path.isdir(path):
        pickle.dump(object, open( "{}/save.p".format(path), "wb" ))
    else:
        print "[Error] dir path is not valid , {}".format(path)

def load_pickle(path_file):
    if os.path.isfile(path_file):
        return pickle.load(open(path_file, "rb"))
    else:
        print "[Error] path file is not valid , {}".format(path_file)


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
    return d_collection
    #dump_pickle(d_collection,'/home/ise/NLP/')


def root_lookup(ids,path_files,out_p=None):
    d_res={}
    for p in path_files:
        with open(p) as f:
            for line in f:
                try:
                    data = json.loads(line)
                except Exception:
                    print "Error: can\'t read data --> {}".format(line)
                else:
                    name_subreddit = data['subreddit_id']
                    id = str(data['id'])
                    if id in ids:
                        if id not in d_res:
                            d_res[id]=data
                        else:
                            #print "The ID: {} filed in path: {} i not unique ".format(id,p)
                            raise Exception("The ID: {} filed in path: {} i not unique ".format(id,p))
    for k in d_res:
        print "Key: {}".format(k)
        print "data: {}".format(str(d_res[k]))
    if out_p is None:
        return d_res
    out_root_path = walker.mkdir_system(out_p,'roots',False)
    for ky in d_res:
        write_disk(out_root_path,d_res[ky],ky)
    return d_res



def merge_root_tree(root_path,file_id,dico):
    data_line = None
    if os.path.isfile(root_path+file_id+'.txt') is False:
        print "{}{}.txt is not exist".format(root_path,file_id)
        return
    with open(root_path+file_id+'.txt') as f:
        for line in f:
            data_line = read_json_data(line)
            break
    root_tree = Node(data_line['id'],None,data_line)
    root_tree.descendants = {}
    if file_id in dico.threads:
        if file_id in dico.threads[file_id]:
            raise Exception("Error in merge_root_tree id: {}".format(file_id))
        dico.threads[file_id][file_id] = root_tree
        for key in dico.threads[file_id]:
            if dico.threads[file_id][key].father == file_id:
                root_tree.descendants[key]=dico.threads[file_id][key]
    #TODO:fix it
    #if data_line['author'] in dico.authore:
    #    dico.authore[data_line['author']].append(file_id)
    #else:
    #    dico.authore[data_line['author']]=[]
    #    dico.authore[data_line['author']].append(file_id)



def write_disk(path,data,file_name):
    if os.path.isdir(path) is False:
        print "the path: {} is not valid".format(path)
        return False
    if path[-1] !='/':
        path = path +'/'
    with open('{}{}.txt'.format(path,file_name), 'w') as outfile:
        json.dump(data, outfile)
    return True


def read_json_data(str_data):
    try:
        data = json.loads(str_data)
    except Exception:
        print "Error: can\'t read data --> {}".format(str_data)
    else:
        return data


def travel_on_tree(d,id,out_path):
    out=walker.mkdir_system(out_path,'id_{}_paths'.format(id))
    if id not in d.threads:
        print "no tree id: {} in the given collection".format(id)
        return
    if id not in d.threads[id]:
        print "no root in tree:{} in the given collection".format(id)
        return
    dump_tree_json(d.threads[id],out_path,"t_{}".format(str(id)))
    root = d.threads[id][id]
    recurse(root,[],d.threads[id],out)


def dump_tree_json(tree,path,file_name):
    d_tree={}
    for ky in tree.keys():
        res = tree[ky].node_to_json()
        d_tree[ky] =res
    with open('{}{}.txt'.format(path,file_name), 'w') as outfile:
        json.dump(d_tree, outfile)


def load_tree_json(path_file):
    tree_dict={}
    data_res = None
    if os.path.isfile(path_file) is False:
        raise Exception("the path: {} is not valid".format(path_file))
    with open('{}'.format(path_file), 'r') as file_handler:
        for line in file_handler:
            data_res = read_json_data(line)
    for ky in data_res :
        if data_res[ky]['father'] == 'None':
            node = Node(ky, None, data_res[ky]['data'])
        else:
            node = Node(ky,data_res[ky]['father'],data_res[ky]['data'])
        if len(data_res[ky]['descendants'])>0:
            node.descendants=data_res[ky]['descendants']
        else:
            node.descendants=None
        tree_dict[ky]=node
    for key in tree_dict.keys():
        list_node={}
        arr = tree_dict[key].descendants
        if arr is not None:
            for x in arr:
                list_node[x]=tree_dict[x]
            tree_dict[key].descendants=list_node
    return tree_dict

def recurse(node,path_tree_ids,tree,out_p):
    path_tree_ids.append(str(node.data['id']))
    if node.descendants is None:
        make_file_path(path_tree_ids,tree,out_p)
        return
    for node_i in node.descendants.keys():
        recurse(node.descendants[node_i],path_tree_ids,tree,out_p)

def make_file_path(list_ids,tree,out_path):
    if len(list_ids)==0:
        print "the list of ids is len:0"
        return
    id_tree = list_ids[0]
    string_data ='\n'
    str1 = ''.join(list_ids)
    hash_str = int(hashlib.sha1(str1).hexdigest(), 16) % (10 ** 8)
    self_text = clean_string_text(tree[id_tree].data['selftext'])
    title_str =clean_string_text(tree[id_tree].data['title'])
    author_root = tree[id_tree].data['author']
    string_comment = "title__{}\n\n{}__{}".format(str(title_str),str(author_root),str(self_text))
    append_to_file(out_path,hash_str,string_comment,True)
    for id in list_ids[1:]:
        data_json = tree[id].data
        txt_i  = clean_string_text(data_json['body'])
        author_i = str(data_json['author'])
        string_comment = "{}__{}\n".format(author_i, txt_i)
        append_to_file(out_path, hash_str, string_comment)


def clean_string_text(txt):
    #print txt
    #print "-"*30
    str_x = unicode(txt).encode('utf-8')
    str_x = str(str_x).replace('\n','<LINE>')
    str_x = str(str_x).replace('\t', '<TAB>')
    str_x = str(str_x).replace('&lt;', '<LT>')
    str_x = str(str_x).replace('&gt;', '<GT>')
    return str_x


def append_to_file(path,file_name,data_string,new_file=False):
    if new_file:
        with open('{}/{}.txt'.format(path,file_name), 'w') as file_handler:
            file_handler.write("{}\n".format(data_string))
    else:
        with open('{}/{}.txt'.format(path,file_name), "a") as file_handler:
            file_handler.write("{}\n".format(data_string))

def test():
    path = '/home/ise/NLP/data_reddit/RC_2018-01-29'
    target_threads = ['7tu0ft']
    d=init_function(path, target_threads)
    path = '/home/ise/NLP/data_reddit/RC_2018-01-30'
    d=init_function(path,target_threads,d)
    ids=target_threads
    paths = ['/home/ise/NLP/data_reddit/RS_2018-01']
    root_lookup(ids, paths, '/home/ise/NLP/test/')
    merge_root_tree('/home/ise/NLP/test/roots/', '7tu0ft', d)
    travel_on_tree(d, '7tu0ft', '/home/ise/NLP/test/')
    exit()

if __name__ == "__main__":
    test()
