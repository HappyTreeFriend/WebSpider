#!/usr/bin/env python
#coding=utf-8
import os,time
import sqlite3 		#内存/本地数据库
import StringIO 	#内存文件对象
import threading,SpiderLog as log
class SpiderData(object):
	'''数据库存储模块
	'''
	def __init__(self, dbfile):
		self.conn_mem = sqlite3.connect(':memory:')
		self.cur_mem = self.conn_mem.cursor()
		self.dbfile = 'db/' + dbfile
		self.mutex = threading.Lock()
		#self.ctbox = CTBox(os.path.splitext(self.dbfile)[0]+'_tr.db')
	def test(self):
		#'''遍历所有表名'''
		tbname = '172_4_16_168'
		str_sql = '''SELECT name FROM sqlite_master WHERE type='table' order by name'''
		log.add_log(log.g_logger.debug(self.__cmd__(str_sql)))
		#'''显示这张表所有数据'''
		str_sql = '''SELECT * FROM '%s' ''' % (tbname)
		#print str_sql
		log.add_log(log.g_logger.debug(self.__cmd__(str_sql)))
		str_sql = "PRAGMA table_info('%s')" % (tbname)
		log.add_log(log.g_logger.debug(self.__cmd__(str_sql)))

	def __cmd__(self, str_sql):
		if self.mutex.acquire():
			try:
				#import pdb
				#pdb.set_trace()
				self.cur_mem.execute(str_sql)
				self.conn_mem.commit()
				self.mutex.release()
			except:
				self.mutex.release()
		return self.cur_mem.fetchall()
	def create_tree(self, site):
		site = comm.site2db(site)
		self.dbTree.__cmd__(str_sql)
	def __create__(self, site):
		'''数据库表的字段
		id：页面id,site：站点域名,src_url：目标url
		href：页面上爬取的url,url：请求时真实访问的url,deep：url深度
		status：返回状态码,msg：返回状态信息,key：关键字信息
		content：页面内容,child：子级目录id,brother：同级目录id'''
		str_sql = '''CREATE TABLE '%s' (site TEXT,src_url TEXT,href TEXT,url TEXT,deep INTEGER,status INTEGER,msg TEXT,key TEXT,content TEXT) ''' % (site)
		#print str_sql
		self.__cmd__(str_sql)
		#self.test()
	def __insert__(self, **data):
		'''插入数据'''
		site = comm.site2db(data['site'])
		str_sql = '''INSERT INTO '%s' (site,src_url,href,url,msg,key,content,deep,status) values ('%s','%s','%s', '%s', '%s','%s','%s',%d, %d) ''' % (site,data['site'],data['src_url'],data['href'],data['url'],data['msg'],data['key'],data['content'], data['deep'], data['status'])
		#print str_sql
		self.__cmd__(str_sql)
		return self.find_id(site, data['href'])
	def __update__(self, **data):
		site = comm.site2db(data['site'])
		str_sql = "UPDATE '%s' SET site='%s',src_url='%s',url='%s',deep=%d,status=%d,msg='%s',key='%s',content='%s' WHERE href='%s' " % (site,data['site'],data['src_url'],data['url'], data['deep'], data['status'],data['msg'], data['key'], data['content'], data['href'])
		#print str_sql
		self.__cmd__(str_sql)
		return self.find_id(site, data['href'])
	def __close__(self, conn):
		conn.commit()
		conn.close()
	def add_data(self, ctbox, **data):
		log.add_log(log.g_logger.info('页面数据加入数据库'))
		site = comm.site2db(data['site'])
		if not self.find_table(site):
			self.__create__(site)
		if not self.find_col(site, 'href', data['href']).__len__():
			reid = self.__insert__(**data)
		else:
			reid = self.__update__(**data)
		data = {'href':data['href']}
		ctbox.add_data(**data)
	def find_table(self, tbname):
		'''查询数据库是否有tbname这个表'''
		str_sql = '''SELECT name FROM sqlite_master WHERE type='table' order by name'''
		#print str_sql
		try:
			ret = self.__cmd__(str_sql)
			if ret.__len__():
				return False
			else:
				return True
		except:
			return False
			
	def find_deep(self, tbname, colval):
		try:
			ret = self.find_col(comm.site2db(tbname), 'deep', colval)
			return ret
		except ValueError:
			log.add_log(log.g_logger.error(ValueError))
			return []
	def find_href(self, tbname, colval):
		try:
			ret = self.find_col(comm.site2db(tbname), 'href', colval)
			return ret
		except ValueError:
			log.add_log(log.g_logger.error(ValueError))
			return []
	def find_id(self, tbname, colval):
		str_sql = '''SELECT rowid FROM '%s' WHERE href='%s' ''' % (tbname, colval)
		cid = self.__cmd__(str_sql)
		#print cid
		if not cid.__len__():
			return cid
		else:
			return cid[0][0]
	def find_col(self, tbname, colname, colval):
		'''在插入数据之前，查询是否存在该数据'''
		str_sql = '''SELECT * FROM '%s' WHERE %s='%s' ''' % (tbname, colname, colval)
		#print str_sql
		#self.test()
		try:
			ret = self.__cmd__(str_sql)
			if ret.__len__():
				return ret
			else:	raise
		except:
			return []
	def get_men_script(self):
		str_buf = StringIO.StringIO()
		for line in self.conn_mem.iterdump():
			str_buf.write('%s\n' % line)
		return str_buf
	def end_data(self):
		'''工作结束时将内存数据库保存到本地'''
		log.add_log(log.g_logger.info('将内存中的数据保存到本地数据库中'))
		str_sql = self.get_men_script().getvalue()
		#import pdb
		#pdb.set_trace()
		self.cur_mem.close()
		self.__close__(self.conn_mem)
		#本地数据库
		try:
			os.remove(self.dbfile)
		except:
			pass
		conn_file = sqlite3.connect(self.dbfile)
		cur_file = conn_file.cursor()
		cur_file.executescript(str_sql)
		cur_file.close()
		self.__close__(conn_file)


from Common import *
from urlparse import urlparse
class CTBox(object):
	def __init__(self, dbT):
		'''再建立一张表来存放目录索引'''
		self.list_data = list()
		self.dbTree = SpiderData(dbT)
		self.par_id = 0
		self.dir = dir()
	def get_scheme_netloc_path_(self, url):
		return urlparse(url)
	def get_file(url):
		return os.path.basename(self.get_scheme_netloc_path_(url).path)
	def split_data(self, url):
		'''根据url分割出data'''
		data = self.get_scheme_netloc_path_(url)
		return ''.join(data.netloc + data.path).split('/')
	def add_node(self,site, data, deep, par_id):
		log.add_log(log.g_logger.info('加入目录树结点'))
		cid = self.insert_data(site, data,deep, par_id)
		self.list_data.append(comm.get_hash(data))
		return cid
	def add_data(self, **data):
		'''传入href'''
		try:
			site = self.get_scheme_netloc_path_(data['href']).netloc
			self.create_tree(site)
		except:
			pass
		href = self.split_data(data['href'])
		log.add_log(log.g_logger.debug('分割url '+str(href)))
		#import pdb
		#pdb.set_trace()
		for i in range(len(href)):
			if i == 0:
				self.par_id = 0
			log.add_log(log.g_logger.debug('加入路径'+str(i)+str(href[i])))
			d_hash = comm.get_hash(href[i])
			try:
				if d_hash not in self.list_data:
					#未加入的路径
					#test = self.dbTree.find_href(site, href[i])
					#print test
					#if href[i] not in test:
					self.par_id = self.add_node(site, href[i], i,self.par_id)
				else:
					self.par_id = self.dbTree.find_id(comm.site2db(site), href[i])
			except:
				pass
			log.add_log(log.g_logger.debug(str(self.par_id)+'父节点'))
			#self.dbTree.test()
		#self.dir.show_now_tree(data['href'])
	def insert_data(self, site, data, deep, par_id):
		site = comm.site2db(site)
		#print site, data, deep, par_id
		str_sql = '''INSERT INTO '%s' (href, deep, par_id) values ('%s', %d, %d)''' % (site, data, deep, par_id)
		self.dbTree.__cmd__(str_sql)
		return self.dbTree.find_id(site, data)
	def create_tree(self, site):
		site = comm.site2db(site)
		str_sql = '''CREATE TABLE '%s' ( href TEXT, deep INTEGER, par_id INTEGER)''' % (site)
		self.dbTree.__cmd__(str_sql)

from BeautifulSoup import *
class LocalData(object):
	def __init__(self, dbfile):
		self.dbfile = 'db/' + dbfile
		self.conn_file = sqlite3.connect(self.dbfile)
		self.cur_file = self.conn_file.cursor()
	def close_db(self):
		self.cur_file.close()
		self.conn_file.close()	
	def all_table(self):
		'''遍历所有表名'''
		str_sql = '''SELECT name FROM sqlite_master WHERE type='table' order by name'''
		return self.__cmd__(str_sql)
	def show_table(self, tbname):
		'''显示这张表所有数据'''
		str_sql = '''SELECT * FROM '%s' ''' % (tbname)
		#print str_sql
		return self.__cmd__(str_sql)
	def show_group(self, tbname):
		str_sql = "PRAGMA table_info('%s')" % (tbname)
		return self.__cmd__(str_sql)
	def show_href(self, tbname, href_val):
		'''显示某一个href的信息'''
		str_sql = '''SELECT * FROM '%s' WHERE href='%s' ''' % (tbname, href_val)
		return self.__cmd__(str_sql)
	def __cmd__(self, str_sql):
		self.cur_file.execute(str_sql)
		self.conn_file.commit()
		return self.cur_file.fetchall()
	def end_data(self):
		self.cur_file.close()
		self.conn_file.close()
	def get_dirpath_file(self,url):
		path = urlparse(url).path
		dir_file = []
		dir_file.append(os.path.dirname(path))
		dir_file.append(os.path.basename(path))
		return dir_file
	def save_file(self, row_data):
		path = 'local/' + row_data[0]
		if not os.path.exists(path):
			#根目录不存在
			os.makedirs(path)
		dir_file = self.get_dirpath_file(row_data[2])
		path += dir_file[0]
		if not os.path.exists(path):
			os.makedirs(path)
		path += '/' + dir_file[1]
		if not dir_file[1]:
			path += 'index.html'
		#文件不存在
		fd = open(path,'w')
		fd.write(comm.db2content(row_data[8]))
		fd.close()
	def save_table(self, tbname):
		for row_data in self.show_table(tbname):
			#print row_data
			self.save_file(row_data)
	def save_local(self,**select):
		'''参数格式
		select = {'dbfile':'test.db','tbname':'www_baidu_com','href':'http://www.baidu.com/1'}'''
		log.add_log(log.g_logger.info('正在将数据库中数据转换到本地目录下'))
		if select['href'] is not None:
			self.save_file(self.show_href(select['tbname'], select['href']))
			return
		if select['tbname'] is not None:
			self.save_table(select['tbname'])
			return
		if select['dbfile'] is not None:
			try:
				for tb in self.all_table()[0]:
					self.save_table(tb)
			except:
				pass
		self.close_db()
		log.add_log(log.g_logger.info('完成转换：%s' % os.path.abspath('local/'+''.join(select['dbfile'].split('.')[:-1]))))
		return
	def url2local(self, content):
		soup = BeautifulStoneSoup(content)
		#获取页面的所有连接,检查url格式，是否同一域名
		self.tran_url(soup.findAll(attrs={'src':True}),'src')
		self.tran_url(soup.findAll(attrs={'href':True}),'href')
		#list_url.append(soup.findAll(attrs={'action':True}))
	def tran_url(self, tags, attr):
		for tag in tags:
			tag['attr'] = self.re_localpath(tag['attr'])
	def re_localpath(self, url):
		abs_local = os.path.abspath('local/')
		url_pack = urlparse(url)
		url = urlunparse(ParseResult(scheme='file', netloc=abs_local+url_pack.netloc, path=path, params=url_pack.params, query=url_pack.query, fragment=url_pack.fragment))
		return url

class dir(object):   
	def __init__(self):   
		self.SPACE = ""   
		self.list = []
	def show_now_tree(self, find_txt):
		try:
			self.read_lines(find_txt)
		except:
			pass	
	def show_tree(self, dbfile):
		log.add_log(log.g_logger.info('正在生成目录树...'))
		tr_db = os.path.splitext(dbfile)[0]+'_tr.db'
		self.ld = LocalData(tr_db)
		par_id = 0
		for tb in self.ld.all_table()[0]:
			self.getDirList(par_id, tb)
		self.ld.close_db()
		self.writeList()
	def list_dir(self, row_id, tb):
		list_dir = []
		for row_data in self.find_col(tb,'par_id',row_id):
			list_dir.append({'row_id':self.find_id(tb,row_data[0]),'path':row_data[0]})
		return list_dir
	def find_col(self, tbname, colname, colval):
		'''在插入数据之前，查询是否存在该数据'''
		str_sql = '''SELECT * FROM '%s' WHERE %s='%s' ''' % (tbname, colname, colval)
		#print str_sql
		#self.test()
		try:
			ret = self.ld.__cmd__(str_sql)
			if ret.__len__():
				return ret
			else:	raise
		except:
			return []
	def find_id(self, tbname, colval):
		str_sql = '''SELECT rowid FROM '%s' WHERE href='%s' ''' % (tbname, colval)
		cid =  self.ld.__cmd__(str_sql)
		#print cid
		if not cid.__len__():
			return cid
		else:
			return cid[0][0]
	def getCount(self, row_id,tb):  
		return self.list_dir(row_id,tb).__len__() 
	def getDirList(self, row_id, tbname):   
		files = self.list_dir(row_id,tbname)   
		fileNum = self.getCount(row_id, tbname)  
		tmpNum = 0  
		log.add_log(log.g_logger.debug(files))
		for file in files: 
			myfile = self.find_id(tbname,file['path'])
			size = self.getCount(myfile, tbname)
			file = file['path']
			if not size:   
				tmpNum = tmpNum +1  
				if (tmpNum != fileNum):  
					self.list.append(str(self.SPACE) + "|--" + file + "\n")  
				else:  
					self.list.append(str(self.SPACE) + "`--" + file + "\n")  
			if size:   
				self.list.append(str(self.SPACE) + "|--" + file + "\n")   
				# change into sub directory  
				self.SPACE = self.SPACE + "|   "   
				self.getDirList(myfile, tbname)   
				# if iterator of sub directory is finished, reduce "│  "   
				self.SPACE = self.SPACE[:-4]   
		return self.list   
	def writeList(self):   
		f = open('tmp/tmp.tr','w')   
		f.writelines(self.list)   
		log.add_log(log.g_logger.info('完成目录树，保存至tmp/tmp.tr文件中'))
		f.close()
		for line in self.list:
			print line,
	def read_lines(self, find_txt, count=3):
		for i in range(self.list.__len__()):
			if lines[i].find(find_txt) >= 0:
				for j in range(count):
					try:
						print lines[i-(count-j-1)],
					except:
						pass



def test_db():
	db = SpiderData('test.db')
	data = {'href':'http://172.4.16.168/wp-login.php','url':'http://172.4.16.168/wp-login.php','status':200, 'content':'<p>123</p>', 'msg':'OK', 'deep':3, 'key':'ALL', 'src_url': 'http://172.4.16.168/wp-login.php', 'site':'172.4.16.168'}
	ctbox = CTBox('test_tr.db')
	db.add_data(ctbox,**data)
	db.add_data(ctbox,**data)
	db.add_data(ctbox,**data)
	#import time
	#time.sleep(1)
	db.end_data()
	ctbox.dbTree.end_data()

def test_tree():
	'''将数据库中href，site，id'''
	ctbox = CTBox('test_tr.db')
	data = {'href':'http://172.4.16.168/wp-login.php'}
	ctbox.add_data(**data)

def test_local(dbfile):
	ld = LocalData(dbfile)
	#print ld.all_table()
	#print ld.show_table('www_baidu_com')
	#print ld.show_group('www_baidu_com')
	#print ld.show_href('www_baidu_com', 'http://www.baidu.com/1')
	cmd = {'dbfile':ld.dbfile,'href':None,'tbname':None}
	ld.save_local(**cmd)

if __name__=='__main__':
	pass
	level = log.log_level.get(5)+':'+log.log_level.get(5)
	log.set_logger(filename='test.log', level=level)
	test_db()
	test_tree()
	test_local('test.db')
	d = dir()
	d.show_tree('test')
	#d.read_lines('job.asp',3)
