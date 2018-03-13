import json,os
import numpy as np
import pandas as pd
import pickle

import walker

def upload_data_thread(mod,p_path,data_txt):
    if mod == 'a':
        with open("{}.txt".format(p_path), "a") as myfile:
            myfile.write(str(data_txt))
    elif mod == 'new':
        with open("{}.txt".format(p_path), 'wb') as f:
            f.write(str(data_txt))

def fill_ram(r_path,reddit_data_dir='/home/eran/Desktop/reddit'):
    d={}
    ctr=0
    print ""
    files_list = scaner(r_path)
    for p_path in files_list:
        with open(p_path) as f:
            for line in f:
                if data_handler(line,d):
                    ctr += 1
                if ctr >5000:
                    flash_disk(d,reddit_data_dir)
                    ctr = 0
        break

def flash_disk(d,reddit_data):
    for ky_sub_reddit in d:
        for ky_thread in d[ky_sub_reddit]:
            out_path = '{}/{}'.format(reddit_data,ky_sub_reddit)
            if os.path.isdir('{}/{}'.format(reddit_data,ky_sub_reddit)) is False:
                out_path = walker.mkdir_system(reddit_data,ky_sub_reddit,False)
            if os.path.isfile("{}/{}".format(out_path,ky_thread)):
                upload_data_thread('a','{}/{}'.format(out_path,ky_thread),d[ky_sub_reddit][ky_thread])
            else:
                upload_data_thread('new','{}/{}'.format(out_path,ky_thread),d[ky_sub_reddit][ky_thread])



def scaner(root_path):
    print ""
    obj_scanner =  walker.walker(root_path)
    out_file = obj_scanner.walk("RC")
    return out_file


def data_handler(data_string,d):
    #print "data = {}".format(string_data)
    data = json.loads(data_string)
    name_subreddit = data['subreddit']
    sub_id= data['subreddit_id'][2:]
    name_subreddit=str(name_subreddit)+str(sub_id)
    permalink = str(data['link_id'][3:] )#need to contain the link id
    if name_subreddit not in d:
        d[name_subreddit]={}
        d[name_subreddit][permalink]=[data_string]
    else:
        if permalink in d[name_subreddit]:
            d[name_subreddit][permalink].append(data_string)
        else:
            d[name_subreddit][permalink] = [data_string]
    return True


if __name__ == "__main__":
    eran_path = '/home/eran/Downloads/'
    files=['RC_2018-01-29','RC_2018-01-30']
    fill_ram(eran_path)

