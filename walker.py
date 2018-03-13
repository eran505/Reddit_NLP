import os,re

class walker:
    def __init__(self, root):
        self._root = root

    def walk(self,rec="", file_t=True, lv=-1, full=True):
        size = 0
        ctr = 0
        class_list = []
        if lv == -1:
            lv = float('inf')
        for path, subdirs, files in os.walk(self._root):
            if lv < ctr:
                break
            ctr += 1
            if file_t:
                for name in files:
                    tmp = re.compile(rec).search(name)
                    if tmp == None:
                        continue
                    size += 1
                    if full:
                        class_list.append(os.path.join(path, name))
                    else:
                        class_list.append(str(name))
            else:
                for name in subdirs:
                    tmp = re.compile(rec).search(name)
                    if tmp == None:
                        continue
                    size += 1
                    if full:
                        class_list.append(os.path.join(path, name))
                    else:
                        class_list.append(str(name))
        return class_list


def mkdir_system(path_root,name,is_del=True):
    if path_root is None:
        raise Exception("[Error] passing a None path --> {}".format(path_root))
    if path_root[-1]!='/':
        path_root=path_root+'/'
    if os.path.isdir("{}{}".format(path_root,name)):
        if is_del:
            os.system('rm -r {}{}'.format(path_root,name))
        else:
            print "{}{} is already exist".format(path_root,name)
            return '{}{}'.format(path_root, name)
    os.system('mkdir {}{}'.format(path_root,name))
    return '{}{}'.format(path_root,name)
