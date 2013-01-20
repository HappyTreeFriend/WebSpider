#!/usr/bin/env python
#coding=utf-8
import os
import sqlite3 		#内存/本地数据库
import StringIO 	#内存文件对象
class SpiderData(object):
    '''数据库存储模块
    '''
    def __init__(self, dbfile):
        self.conn_mem = sqlite3.connect(':memory:')
        self.cur_mem = self.conn_mem.cursor()
        self.dbfile = 'db/' + dbfile
        #self.ctbox = CTBox(os.path.splitext(self.dbfile)[0]+'_tr.db')
    def __cmd__(self, str_sql):
        self.cur_mem.executescript(str_sql)
        self.conn_mem.commit()
        print self.cur_mem.fetchall()
        return self.cur_mem
    def create_tree(self, site):
        site = comm.site2db(site)
        self.dbTree.__cmd__(str_sql)
    def __create__(self, site):
        '''数据库表的字段
        id：页面id,site：站点域名,src_url：目标url
        href：页面上爬取的url,url：请求时真实访问的url,deep：url深度
        status：返回状态码,msg：返回状态信息,key：关键字信息
        content：页面内容,child：子级目录id,brother：同级目录id'''
        str_sql = '''CREATE TABLE '%s' (site TEXT,src_url TEXT,href TEXT,url TEXT,deep INTEGER,status INTEGER,msg TEXT,key TEXT,content TEXT);''' % (site)
        #print str_sql
        self.__cmd__(str_sql)
    def __insert__(self, **data):
        '''插入数据'''
        str_sql = '''INSERT INTO '%s' (site,src_url,href,url,msg,key,content,deep,status) values ('%s','%s','%s', '%s', '%s','%s','%s',%d, %d);''' % (data['site'],data['site'],data['src_url'],data['href'],data['url'],data['msg'],data['key'],data['content'], data['deep'], data['status'])
        #print str_sql
        self.__cmd__(str_sql)

    def __update__(self, **data):
        str_sql = "UPDATE '%s' SET site='%s',src_url='%s',url='%s',deep=%d,status=%d,msg='%s',key='%s',content='%s',child=%d,brother=%d WHERE href='%s';" % (data['site'],data['site'],data['src_url'],data['url'], data['deep'], data['status'],data['msg'], data['key'], data['content'], data['child'],data['brother'],data['href'])
        #print str_sql
        self.__cmd__(str_sql)
    def __close__(self, conn):
        conn.commit()
        conn.close()
    def add_data(self, ctbox, **data):
        site = comm.site2db(data['site'])
        if not self.find_table(site):
            self.__create__(site)
        if not self.find_col(site, 'href', data['href']):
            reid = self.__insert__(**data)
        else:
            reid = self.__update__(**data)
        data = {'href':data['href']}
        ctbox.add_data(**data)
    def find_table(self, tbname):
        '''查询数据库是否有tbname这个表'''
        str_sql = '''SELECT * FROM '%s' LIMIT 0,1;''' % (tbname)
        #print str_sql
        try:
            self.__cmd__(str_sql).fetchone()
            return True
        except:
            return False
    def find_deep(self, tbname, colval):
        return self.find_col(comm.site2db(tbname), 'deep', colval)
    def find_href(self, tbname, colval):
        return self.find_col(comm.site2db(tbname), 'href', colval)
    def find_col(self, tbname, colname, colval):
        '''在插入数据之前，查询是否存在该数据'''
        str_sql = '''SELECT * FROM '%s' WHERE %s='%s';''' % (tbname, colname, colval)
        #print str_sql
        try:
            import pdb
            pdb.set_trace()
            ret = self.__cmd__(str_sql).fetchall()
            if not ret.__len__():
                return False
            else:
                return ret
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
    def get_scheme_netloc_path_(self, url):
        return urlparse(url)
    def get_file(url):
        return os.path.basename(self.get_scheme_netloc_path_(url).path)
    def split_data(self, url):
        '''根据url分割出data'''
        data = self.get_scheme_netloc_path_(url)
        return ''.join(data.netloc + data.path).split('/')
    def add_node(self,site, data, deep, par_id):
        cid = self.insert_data(site, data,deep, par_id)
        self.list_data.append(comm.get_hash(data))
    def add_data(self, **data):
        '''传入href'''
        print data
        try:
            site = self.get_scheme_netloc_path_(data['href']).netloc
            self.create_tree(site)
        except:
            pass
        href = self.split_data(data['href'])
        par_id = 0
        for i in range(len(href)):
            d_hash = comm.get_hash(href[i])
            if d_hash not in self.list_data:
                try:
                    if href[i] in self.dbTree.find_deep(site, i):
                        if href[i] not in self.dbTree.find_href(site, href[i]):
                            par_id = self.add_node(site, href[i], i, par_id)
                except:
                    par_id = self.add_node(site, href[i], i, par_id)


    def insert_data(self, site, data,deep, par_id):
        site = comm.site2db(site)
        print site, data, deep, par_id
        str_sql = '''INSERT INTO '%s' (name, deep, par_id) values ('%s', %d, %d);''' % (site, data, deep, par_id)
        self.dbTree.__cmd__(str_sql)
    def create_tree(self, site):
        site = comm.site2db(site)
        str_sql = '''CREATE TABLE '%s' (name TEXT, deep INTEGER, par_id INTEGER);''' % (site)
        self.dbTree.__cmd__(str_sql)

def test_db():
    db = SpiderData('test.db')
    data = {'href':'http://www.baidu.com/1','url':'http://www.baidu.com/1/2/3','status':200, 'content':'<p>123</p>', 'msg':'OK', 'deep':3, 'key':'ALL', 'src_url': 'http://www.baidu.com', 'site':'www.baidu.com'}
    ctbox = CTBox('test_tr.db')
    db.add_data(ctbox,**data)
    db.add_data(ctbox,**data)
    db.add_data(ctbox,**data)
    import time
    time.sleep(1)
    import pdb
    pdb.set_trace()
    db.end_data()

def test_tree(dbfile):
    '''将数据库中href，site，id'''
    ctbox = CTBox(dbfile)
    data = {'href':'http://www.baidu.com/0/1/2/3'}
    ctbox.add_data(**data)

if __name__=='__main__':
    test_tree('test_tr.db')
