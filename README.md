WebSpider
=========

##概述
爬虫工具对指定站点，深度，关键字的页面信息进行指定线程数的抓取，并将数据保存到sqlite数据库中，同时分等级的保存工作时的信息到日志中，亦可按需求将页面转换为本地文件进行浏览。关键字格式参考google hacking格式，可进行特色个性化的抓取，工作时可按需求将数据信息保存，便于今后的分析和再次利用。

##设计思路
利用python的客户端库模拟浏览器访问url，并分析url的域名，深度等信息；正则表达式模块分析页面信息；多线程模块提高抓取效率；数据库操作模块保存页面数据；日志模块分等级保存和显示日志信息；本地文件操作模块保存页面数据。

##模块设计
![模块设计图](1.jpg)

##功能设计
###交互与控制
用户与程序的交互：生成命令行帮助，从命令行获取用户参数指令。
程序流程的调用与控制的功能，将用户的指令参数通过一些必要的处理交给程序相应的函数执行。
<pre><code>import argparse,textwrap
class SpiderOpt(object):
    '''命令行参数处理模块
    usage: %prog [option] args\n%prog -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5”
    '''
    def add_args(self):
        ……
    def check(self):
        '''检查选项值格式'''
        ……</code></pre>