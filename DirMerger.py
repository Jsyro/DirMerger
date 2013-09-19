#   MusicMerger.py

#       moves files from one folder to another
#       ignoring duplicates  

import os
import os.path
import sys
import time 

argc = len(sys.argv)

if argc < 2:
    print "Provide folder name you wish to merge"
    print "This folder must be in the current directory"
    sys.exit(1)

# print sys.argv[1] 
debug = 1
MergeStatus = dict()
path1 = os.getcwd()
path2 = os.getcwd() + '/' + sys.argv[1]
    
contents1 = os.listdir(path1)
contents2 = os.listdir(path2)  


for filename in contents1:
    ext = filename[-4:]
    filename = filename[:-4]
    MergeStatus[filename + ext] = "ORIGINAL"
   
for filename in contents2:
    ext = filename[-4:]
    filename = filename[:-4]
    if (filename + ext) in MergeStatus:
        MergeStatus[filename + ext] = "DUPLICATE"
    else:
        MergeStatus[filename + ext] = "MERGE"

print MergeStatus


        
for x in MergeStatus:
    
    if MergeStatus[x]== "ORIGINAL": 
        continue
    
    filepath1 = path1 + "/" + x
    filepath2 = path2 + "/" + x
    
    if MergeStatus[x]== "MERGE": 
        print x + " => " + MergeStatus[x]
        os.rename(filepath2, filepath1)
    
    
for x in MergeStatus:
    if MergeStatus[x]== "ORIGINAL": 
        continue
        
    filepath1 = path1 + "/" + x
    filepath2 = path2 + "/" + x
    filepathdup = filepath1 + "1"
   
    if MergeStatus[x] == "DUPLICATE":
        print x + " => " + MergeStatus[x]
        if x[-4] is not ".":
            os.rename(filepath2, filepathdup)
            MergStatus[x] == "DUPLICATE_FOLDER"
        
