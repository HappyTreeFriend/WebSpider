#!/usr/bin/env python
#coding=utf-8

import argparse,textwrap
from WebSpider import *
init_dir = ['db','dict','local','log','tmp']
global ncount
class SpiderOpt(object):
	'''命令行参数处理模块
	usage: %prog [option] args\n%prog -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5”
	'''
	def __init__(self):
		global ncount
		ncount = 0
		self.parser=argparse.ArgumentParser(
				argument_default=None,
				formatter_class=argparse.RawDescriptionHelpFormatter,
				description=textwrap.dedent('''\
						爬虫工具使用文档
						================
						'''),
			)
		self.add_args()
	def add_args(self):
		self.parser.add_argument('-u', dest='url', help='指定爬虫开始的地址')
		self.parser.add_argument('-d', type=int, dest='deep', help='指定爬虫深度')
		self.parser.add_argument('--key', help='页面内的关键词，获取满足该关键词的网  页，可选参数，默认为所有页面')
		self.parser.add_argument('--thread', type=int, default=10, metavar='NUMBER', help='指定线程池大小，多线程爬取页面，可选参数，(default:%(default)s)')
		self.parser.add_argument('--localpath', help='爬取完成将数据转换为本地镜像，指定路径或默认')
		self.parser.add_argument('-f', default='spider.log', dest='logfile', help='指定保存日志文件，(default:%(default)s)')
		self.parser.add_argument('-l', type=int, choices=xrange(1,6), default=5, dest='loglevel', help='日志记录文件记录详细程度，数字越大记  录越详细,loglevel(1-5)')
		self.parser.add_argument('--dbfile', metavar='FILEPATH', default='spider.db', dest='dbfile', help='存放结果数据到指定的数据库（sqlite）文  件中，(default:%(default)s)')
		self.parser.add_argument('--testself', action='store_const', const=self.test_self, help='程序自测，可选参数')
		self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='程序版本信息')
		
	def run(self):
		try:
			self.args=self.parser.parse_args()
			#print self.args
			#self.check()
			if self.args.testself():
				self.set_log(self.args.logfile, self.args.loglevel)
				WebSpider(self.args.url, self.args.deep, self.args.dbfile, self.args.thread)
				test_local(self.args.dbfile)
				dir().show_tree(self.args.dbfile)
				log.pbar.finish()
		except:
			self.error('选项值格式错误')
		
	def check(self):
		'''检查选项值格式'''
		if self.args.url[:4]!='http':
			self.error('-u URL格式错误  ex:-u http(s)://www.example.com')
		if not self.args.test_self:
			if not (self.args.url or self.args.deep):
				self.error('必须传入-u -d选项参数')

	def test_self(self):
		'''程序自测'''
		print self.test_self.__doc__
		self.set_log(self.args.logfile, self.args.loglevel)
		WebSpider('http://www.jslndq.com/', 1, 'www_jslndq_com.db', 10)
		test_local('www_jslndq_com.db')
		dir().show_tree('www_jslndq_com.db')
		#WebSpider('http://172.4.16.168/', 2, '172_4_16_168.db', 5)
		#test_local('172_4_16_168.db')
		#dir().show_tree('172_4_16_168.db')
		log.pbar.finish()
		return
	def exit(self):
		self.parser.exit()
	def error(self,msg):
		self.parser.error(msg)
	def nothing(self):
		pass
	def help(self):
		self.parser.print_help()
	def process_bar(self):
		global ncount
		print
		log.pbar.update()
		ncount = (100+(ncount+1))%500
	def set_log(self, logfile, level):
		level = log.log_level.get(level)+':'+log.log_level.get(level)
		log.set_logger(filename=logfile, level=level)
		#将日志信息加入队列，每个10秒读取打印
		#import threading
		#p = threading.Timer(3,self.process_bar)
		#t = threading.Timer(3,log.ex_log)
		#p.start()
		#t.start()
		#for i in range(0):
			#log.add_log(log.g_logger.info('hello, world'))

		
if __name__=='__main__':
	SpiderOpt().run()
