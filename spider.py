#!/usr/bin/env python
#coding=utf-8

class Common(object):
	def test():
		pass
	def pdb():
		import pdb
		pdb.set_trace()

import argparse,textwrap
class SpiderOption(object):
	'''
	命令行参数处理模块
	usage: %prog [option] args\n%prog -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5”
	'''
	def __init__(self):
		self.parser=argparse.ArgumentParser(
				argument_default=self.nothing,
				formatter_class=argparse.RawDescriptionHelpFormatter,
				description=textwrap.dedent('''\
						爬虫工具使用文档
						================
						'''),
			)
		self.add_args()
	def add_args(self):
		self.parser.add_argument('-u', required=True, dest='url', help='指定爬虫开始的地址')
		self.parser.add_argument('-d', type=int, required=True, dest='deep', help='指定爬虫深度')
		self.parser.add_argument('--key', help='页面内的关键词，获取满足该关键词的网  页，可选参数，默认为所有页面')
		self.parser.add_argument('-f', default='spider.log', dest='logfile', help='指定保存日志文件，(default:%(default)s)')
		self.parser.add_argument('-l', type=int, choices=xrange(1,6), dest='loglevel', help='日志记录文件记录详细程度，数字越大记  录越详细,loglevel(1-5)')
		self.parser.add_argument('--dbfile', metavar='FILEPATH', help='存放结果数据到指定的数据库（sqlite）文  件中')
		self.parser.add_argument('--thread', type=int, default=10, metavar='NUMBER', help='指定线程池大小，多线程爬取页面，可选参数，(default:%(default)s)')
		self.parser.add_argument('--testself', action='store_const', const=self.test_self, help='程序自测，可选参数')
		self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='程序版本信息')
		
	def run(self):
		self.args=self.parser.parse_args()
		#print args
		self.check()
		self.args.testself()
	def check(self):
		'''检查选项值格式'''
		if self.args.url[:4]!='http':
			self.error('-u URL格式错误  ex:-u http(s)://www.example.com')

	def test_self(self):
		'''
		程序自测
		'''
		print self.test_self.__doc__
	def exit(self):
		self.parser.exit()
	def error(self,msg):
		self.parser.error(msg)
	def nothing(self):
		pass
	def test(self):
		self.parser.print_help()


import re,urllib,urllib2,cookielib
from BeautifulSoup import *
class WebSpider(object):
	'''
	网络爬虫功能模块
	'''
	def __init__(self, url, deep):
		self.cj=cookielib.CookieJar()
		self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(self.opener)
		self.url=url
		self.deep=deep
	def find_link(self):
		now_url=self.url
		content=urllib2.urlopen(now_url).read()
		soup=BeautifulStoneSoup(content)
		find_a=soup.findAll('a')	#[a,a,...]
		obj_href=list()
		for cnt in range(len(find_a)):
			tmp={'href':find_a[cnt]['href'],'statu
			a_href.append(find_a[cnt]['href'])

	def active(self):
		'''检查连接状态'''
		pass
	def deep(self):
		'''检查连接深度'''
		pass


class SpiderLogging(object):
	'''
	日志处理模块
	'''
	pass


class SpiderData(object):
	'''
	数据库存储模块
	'''
	pass

if __name__=='__main__':
	#SpiderOption().run()
	WebSpider('http://www.baidu.com',1).find_link()
