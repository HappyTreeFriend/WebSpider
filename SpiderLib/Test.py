#!/usr/bin/env python
# encoding: utf-8  

import os   
class dir(object):   
    def __init__(self):   
        self.SPACE = ""   
        self.list = []  

    def getCount(self, url):  
        files = os.listdir(url)  
        count = 0;  
        for file in files:  
            myfile = url + "/" + file  
            if os.path.isfile(myfile):  
                count = count + 1  
        return count  
    def getDirList(self, url):   
        files = os.listdir(url)   
        fileNum = self.getCount(url)  
        tmpNum = 0  
        for file in files:   
            myfile = url + "/" + file   
            size = os.path.getsize(myfile)   
            if os.path.isfile(myfile):   
                tmpNum = tmpNum +1  
                if (tmpNum != fileNum):  
                    self.list.append(str(self.SPACE) + "|--" + file + "\n")  
                else:  
                    self.list.append(str(self.SPACE) + "`--" + file + "\n")  
            if os.path.isdir(myfile):   
                self.list.append(str(self.SPACE) + "|--" + file + "\n")   
                # change into sub directory  
                self.SPACE = self.SPACE + "|  "   
                self.getDirList(myfile)   
                # if iterator of sub directory is finished, reduce "©¦  "   
                self.SPACE = self.SPACE[:-4]   
        return self.list   
    def writeList(self, url):   
        f = open(url, 'w')   
        f.writelines(self.list)   
        print "ok"   
        f.close()   
#if __name__ == '__main__':   
    #d = dir()   
    #d.getDirList("/home/natsuki/www") # input directory  
    #d.writeList("/home/natsuki/www/1.txt") # write to file 

import sys
import time

# Output example: [=======   ] 75%
# width defines bar width
# percent defines current percentage

def progress(width, percent):
    print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * '='), percent),
    if percent >= 100:
        print
        sys.stdout.flush()

# Simulate doing something ...
for i in xrange(100):
    progress(50, (i + 1))
    time.sleep(0.1) # Slow it down for demo
