import os,sys
import hashlib
# from checksum import create_checksum
# from diskwalk import diskwalk
from os.path import getsize
import sys

class diskwalk(object):
    def __init__(self,path):
        self.path = path
    def paths(self):
        path=self.path
        path_collection=[]
        for dirpath,dirnames,filenames in os.walk(path):
            for file in filenames:
                fullpath=os.path.join(dirpath,file)
                path_collection.append(fullpath)
        return path_collection

def create_checksum(path):
    fp = open(path, 'rb')
    checksum = hashlib.md5()
    while True:
        buffer = fp.read(8192)
        if not buffer:break
        checksum.update(buffer)
    fp.close()
    checksum = checksum.digest()
    return checksum


def findDupes(path):
    record = {}
    dup = {}
    dup2=[]
    record2 = []
    d = diskwalk(path)
    files = d.paths()
    for file in files:
        # print(file)
        compound_key,_ = (getsize(file),create_checksum(file))
        # print(compound_key)
        if compound_key in record2:
            # print(i)
            # dup[file] = record[compound_key]
            dup2.append(file)
        else:
            lengthList = [i for i in range(compound_key - 5, compound_key + 5)]
            for i in lengthList:
                record2.append(i)
        # print(record2)
    # print(dup2)
    return dup2

class deletefile(object):
    def __init__(self,file):
        self.file=file
    def delete(self):
        print("Deleting %s" % self.file)
        os.remove(self.file)
    def dryrun(self):
        print("Dry Run: %s [NOT DELETED]" % self.file)
    def interactive(self):
        answer=input("Do you really want to delete: %s [Y/N]" % self.file)
        if answer.upper() == 'Y':
            os.remove(self.file)
        else:
            print("Skiping: %s" % self.file)
        return


if __name__ == '__main__':
    text_dir = 'divorce/'
    # filenames = os.listdir(text_dir)
    # for file in diskwalk(text_dir).paths():
    #     print(file)
    dup = findDupes(text_dir)
    print('duplicated file: ', dup)
    for file in dup:
        delete=deletefile(file)
        #delete.dryrun()
        delete.interactive()
