#==========================================================================================================
# Program:    Automated Disk Sanitiser
# Author:     Vedant Dhamal
# Purpose:    Find and delete duplicate files using MD5 checksum
#==========================================================================================================

import hashlib
import os
import sys

#----------------------------------------------------------------------------------------------------------
# Function Name : CalculateChecksum
# Description   : Returns the MD5 checksum of a file
#----------------------------------------------------------------------------------------------------------

def CalculateChecksum(FileName):

    fobj = open(FileName, "rb")

    hobj = hashlib.md5()

    Buffer = fobj.read(1000)

    while(len(Buffer) > 0):
        hobj.update(Buffer)
        Buffer = fobj.read(1000)

    fobj.close()

    return hobj.hexdigest()

#----------------------------------------------------------------------------------------------------------
# Function Name : FindDuplicate
# Description   : Finds duplicate files inside a directory
#----------------------------------------------------------------------------------------------------------

def FindDuplicate(DirectoryName = "Marvellous"):

    Ret = os.path.exists(DirectoryName)

    if(Ret == False):
        print("There is no such directory")
        return

    Ret = os.path.isdir(DirectoryName)

    if(Ret == False):
        print("It is not a directory")
        return

    Duplicate = {}

    for FolderName, SubFolderName, FileName in os.walk(DirectoryName):

        for fname in FileName:

            fname = os.path.join(FolderName, fname)

            Checksum = CalculateChecksum(fname)

            if Checksum in Duplicate:
                Duplicate[Checksum].append(fname)
            else:
                Duplicate[Checksum] = [fname]

    return Duplicate

#----------------------------------------------------------------------------------------------------------
# Function Name : DeleteDuplicate
# Description   : Deletes duplicate files and keeps only one original copy
#----------------------------------------------------------------------------------------------------------

def DeleteDuplicate(Path = "Marvellous"):

    MyDict = FindDuplicate(Path)

    if(MyDict == None):
        return

    Result = list(filter(lambda x : len(x) > 1, MyDict.values()))

    Count = 0
    Cnt = 0

    for value in Result:

        Count = 0

        for subvalue in value:

            Count = Count + 1

            if(Count > 1):
                print("Deleted file :", subvalue)
                os.remove(subvalue)
                Cnt = Cnt + 1

    print("--------------------------------")
    print("Total deleted files :", Cnt)
    print("--------------------------------")

#----------------------------------------------------------------------------------------------------------
# Function Name : main
# Description   : Entry point of program
#----------------------------------------------------------------------------------------------------------

def main():

    if(len(sys.argv) != 2):
        print("Usage : python DiskSanitiser.py DirectoryName")
        return

    DeleteDuplicate(sys.argv[1])

#----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()