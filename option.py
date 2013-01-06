#!/usr/bin/env python
#coding=utf-8

import sys
from optparse import OptionParser
from optparse import OptionGroup


#解决中文帮助乱码
reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

def SpiderOption():
    USAGE='usage: %prog [option] args\n%prog -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5”'
    parser=OptionParser(USAGE)


