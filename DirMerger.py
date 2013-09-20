#   DirMerger.py
#   Jason Syrotuck
#   Sept 18 2013

#   ASSUMPTIONS:
#       1) File names must match exactly to them to be considered duplicates 
 
#       2) This file is in the same directory as the destination and 
#          and the source directory is 1 level down from this one 


#   Description:
#       Compares the Contents of one folder to another
#       Moves Files and folders of different names
#       Ignores duplicate files
#       Moves duplicate folders and add a suffix to the file name 
#       Writes a log file of how things were identified

import os
import os.path
import sys

def usage():
    print "provide folder name you wish to merge, this folder must be in the current directory"
    sys.exit(1)

def init ():
  
    argc = len(sys.argv)
    global MergeStatus
    global MergeFlag
    global MergeStats
    
    if argc < 2:
        usage()
        
    if argc == 3 and sys.argv[2] == "-m":
        MergeFlag = 1
    else:
        MergeFlag = 0
    MergeStats = {'Merged Items': 0,
                  'Duplicates Files': 0,
                  'Duplicate Folders': 0,
                  'Original Files': 0, 
                  'Original Folders': 0
                  }
                  
    MergeStatus = dict()

#   DictToList:
#   Iterates through the dictionary and creates a formatted
#   list of strings. Then sorts this list and returns   
def DictToList(DICT):
    List = []
    for x,y in DICT.iteritems():
        List.append(repr(x) + "  =>  " + repr(y) + "\n")    # build the list
    List.sort()
    return List
    
    
#   isFile:  
#   Iterates through the last 5 char's in the string
#   searching for a '.' if none is found then it is a folder
def isFile(path, filename):
    newpath = path + "/" + filename
    if os.path.isfile(newpath):
        return 1
    else:
    return 0
    
#   logFile:
#   Creates lists from MergeStatus and MergeStats 
#   sorts said lists and writes it into log.txt
def logFile():
    log = open('log.txt', 'w')
    MergeList = DictToList(MergeStatus)
    StatList = DictToList(MergeStats)    
    
    for str in StatList:
        log.write(str)                          # write the sorted list to log.txt
    log.write("\nMergeStatus:\n")
    for str in MergeList:
        log.write(str)                          # write the sorted list to log.txt
    
#   getCurrPath:
#   return the current working directory
#   used when moving files to CWD
def getCurrPath ():
    return os.getcwd()                          #get current working directory

#   makePath:
#   appends a file name of directory as a path from the 
#   current directory used to amke the path to the src dir
def makePath (string):
    return os.getcwd() + "/" + string

#   checkPath:
#   checks to make sure either the path leads to a file 
#   or a folder, if it points to neither the program quits
def checkPath(path):
    if not os.path.isdir(path) or os.path.isfile(path):
        print "File does not exist "
        print "Filepath given = " + path
        sys.exit(1)
 
#   buildMergeStat: 
#   calls getContents and matchContents     
def buildMergeStat(path1, path2):
    getContents(path1)
    matchContents(path2)
     
#   getContents:
#   adds all the items in the list to the dict MergeStatus
#   distinguishes between files and folders and sets the value
#   accordingly
def getContents (path):
    list = os.listdir(path)
    for filename in list:
        if isFile(path, filename):
            MergeStatus[filename] = "OrgFile"
            MergeStats['Original Files']+= 1  
        else:    
            MergeStatus[filename] = "OrgDir"
            MergeStats['Original Folders']+= 1  
            
            
#   matchContents:
#   compares the list of items in the given path with MergeStatus
#   1) If item is in this list but not already in the dictionary then
#       will need to be moved as is.
#   2) if a file is in both lists the key is given the value 'DupFile'
#       and it will not be moved or renamed
#   3) if a directory is in the both lists the key is given the value
#       "DupDir" and will be moved but renamed   
def matchContents(path):   
    list = os.listdir(path)
    for z in list:
        if MergeStatus.has_key(z):
            if MergeStatus[z] == "OrgFile":
                MergeStatus[z] = "DupFile"
                MergeStats['Duplicate Files']+= 1  
                MergeStats['Original Files']-= 1  
               
            if MergeStatus[z] == "OrgDir":
                MergeStatus[z] = "DupDir"
                MergeStats['Duplicate Folders']+= 1 
                MergeStats['Original Folders']-= 1 
        else:
                MergeStatus[z] = "MERGE"
                MergeStats['Merged Items']+= 1 

                
#   merge:
#   interprets the values of the keys and acts accordingly
#   1) "OrgDir" or "OrgFile", some file or directory exists in the
#       destination folder so there is nothing to move
#   2) "DupFile" the same file exists in both directories and it 
#       will not be moved
#   3) "DupDir" the same directory exists in both locations so the
#       folder is moved but renamed to "<name>-1"
#   4) "MERGE" the file or folder does not exist in the destination 
#       but does exist in the source, so it is moved.
def merge(path1, path2):        
    for x in MergeStatus:    
        if MergeStatus[x] == ("OrgDir" or "OrgFile"):  #Do Nothing
            continue
    
        filepath1 = path1 + "/" + x      #build src path
        filepath2 = path2 + "/" + x      #build dest path
    
        if MergeStatus[x]== "MERGE":     
            os.rename(filepath2, filepath1) #move the file 
    for x in MergeStatus:               # check again for dups
        if MergeStatus[x]== "ORIGINAL":  #Do Nothing
            continue
        
        filepath1 = path1 + "/" + x      #build src path
        filepath2 = path2 + "/" + x      #build dest path
   
        if MergeStatus[x] == "DupFile":
            continue
            
        if MergeStatus[x] == "DupDir":                    
                os.rename(filepath2, (filepath1 + "-1")) # move with new name 

if __name__ == '__main__':    
    init()
      
    srcPath = getCurrPath()
    destPath = makePath(sys.argv[1])

    checkPath(srcPath)
    checkPath(destPath)
    
    buildMergeStat(srcPath, destPath)
    
    if MergeFlag == 1:
        merge(srcPath, destPath)
        print "\nMerge successful"
        print "Results written in log.txt"
    else:
        print "\nNo files or folders moved, add '-m' option"
        print "Predicted results written in log.txt"
    logFile()
    print "\nComplete"
