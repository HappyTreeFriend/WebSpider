#!/usr/bin/env python
#coding=utf-8

import sqlite3 		#内存/本地数据库
import StringIO 	#内存文件对象
class SpiderData(object):
	'''数据库存储模块
	'''
	def __init__(self, dbfile):
		self.conn_mem = sqlite3.connect(':memory:')
		self.cur_mem = self.conn_mem.cursor()
		self.dbfile = dbfile
	def __cmd__(self, str_sql):
		self.cur_mem.executescript(str_sql)
		self.conn_mem.commit()
		return self.cur_mem
	def __create__(self, site):
		'''数据库表的字段
		id：页面id,site：站点域名,src_url：目标url
		href：页面上爬取的url,url：请求时真实访问的url,deep：url深度
		status：返回状态码,msg：返回状态信息,key：关键字信息
		content：页面内容,child：子级目录id,brother：同级目录id'''
		str_sql = '''CREATE TABLE '%s' (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		site TEXT,
		src_url TEXT,
		href TEXT,
		url TEXT,
		deep INTEGER,
		status INTEGER,
		msg TEXT,
		key TEXT,
		content TEXT,
		child INTEGER DEFAULT -1,
		brother INTEGER DEFAULT -1
		);''' % (site)
		print str_sql
		self.__cmd__(str_sql)
	def __insert__(self, **data):
		'''插入数据'''
		import pdb
		pdb.set_trace()
		str_sql = '''
		INSERT INTO '%s' 
		(site,src_url,href,url,deep,
		status,msg,key,content,child,brother)
		values(%s,%s,%s, %s, %d,%d, %s, %s, %s, %d, 
		%d);''' % (
				data['site'],data['src_url'],data['href'],data['url'],
				data['deep'],
				data['status'],
				data['msg'], data['key'], data['content'],
				data['child'],
				data['brother'])
		print str_sql
		self.__cmd__(str_sql)
	def __update__(self, **data):
		str_sql = "UPDATE %s SET site='%s',src_url='%s',url='%s',deep=%d,status=%d,msg='%s',key='%s',content='%s',child=%d,brother=%d WHERE href='%s';" % (data['site'],data['site'],data['src_url'],data['url'], data['deep'], data['status'],data['msg'], data['key'], data['content'], data['child'],data['brother'],data['href'])
		print str_sql
		self.__cmd__(str_sql)
	def __close__(self, conn):
		conn.commit()
		conn.close()
	def add_data(self, **data):
		site = data['site']
		if not self.find_table(site):
			self.__create__(site)
		if not self.find_href(site, data['href']):
			self.__insert__(**data)
		else:
			self.__update__(**data)
	def find_table(self, tbname):
		'''查询数据库是否有tbname这个表'''
		str_sql = '''SELECT * FROM '%s' LIMIT 0,1;''' % (tbname)
		print str_sql
		try:
			if not self.__cmd__(str_sql).fetchone().__len__():
				return False
			else:
				return True
		except:
			return False
	def find_href(self, tbname, href):
		'''在插入数据之前，查询是否存在该数据'''
		str_sql = "SELECT * FROM '%s' WHERE href='%s';" % (tbname, href)
		print str_sql
		try:
			if not self.__cmd__.fetchone().__len__():
				return False
			else:
				return True
		except:
			return False
	def get_men_script(self):
		str_buf = StringIO.StringIO()
		for line in self.conn_mem.iterdump():
			str_buf.write('%s\n' % line)
		return str_buf
	def end_data(self):
		'''工作结束时将内存数据库保存到本地'''
		str_sql = self.get_men_script().getvalue()
		self.__close__(self.conn_mem)
		#本地数据库
		conn_file = sqlite3.connect(self.dbfile)
		cur_file = self.conn_file.cursor()
		cur_file.executescript(str_sql)
		self.__close__(conn_file)

from Common import *
from urlparse import urlparse
import os
class CTnode(object):
	def __init__(self, child, data, brother):
		'''只有子叶才有真正的页面
		其他的节点都是存路径'''
		self.child = child
		self.data = data
		self.brother = brother
class CTBox(object):
	def __init__(self, root_data):
		self.root = CTnode(-1, root_data, -1)
		self.list_node = list()
		self.list_data = list()
		self.list_data.append(comm.get_hash(root_data))
	def get_scheme_netloc_path_(self, url):
		return urlparse(url)
	def get_file(url):
		return os.path.basename(self.get_scheme_netloc_path_(url).path)
	def split_data(self, url):
		'''根据url分割出data'''
		return self.get_scheme_netloc_path_(url).path.split('/')[1:]
	def find_node(self, find_data, nodeid=0):
		'''先序找到了数据，返回id'''
		node = self.list_node[nodeid]
		if node.data == find_data:
			return nodeid
		if node.child != -1:
			self.find_node(find_data, node.child)
		if node.brother != -1:
			self.find_node(find_data, node.brother)
	def add_node(self, data):
		self.list_node.append(CTnode(-1, data, -1))
		self.list_data.append(comm.get_hash(data))
	def add_child(self, data, par):
		'''加入数据到孩子节点'''
		self.add_node(data)
		par.child = self.list_node.__len__()-1
	def add_brother(self, data, pre):
		'''加入数据到兄弟节点'''
		self.add_node(data)
		pre.brother = self.list_node.__len__()-1
	def add_data(self, data):
		'''传入href'''
		data = self.split_data(data)
		for d in data:
			if comm.get_hash(d) not in self.list_data:
				#添加节点



if __name__=='__main__':
	db = SpiderData('test.db')
	data = {'href':'http://www.baidu.com/1/2/3','url':'http://www.baidu.com/1/2/3','status':200, 'content':'<p>123</p>', 'msg':'OK', 'deep':3, 'key':'ALL', 'src_url': 'http://www.baidu.com', 'site':'www.baidu.com','child':0,'brother':0}
	db.add_data(**data)
	import time
	time.sleep(3)
	db.end_data()
