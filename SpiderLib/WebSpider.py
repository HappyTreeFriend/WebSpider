#!/usr/bin/env python
#coding=utf-8

import re,Common
import httplib,urllib,urllib2,cookielib
from BeautifulSoup import *
USER_AGENT = "WebSpider.py"
class WebSpider(object):
	'''网络爬虫功能模块
	'''
	def __init__(self, url, deep):
		self.cj = cookielib.CookieJar()
		urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj)))

		self.deep = deep
		#检查用户输入的url，并加入访问队列
		self.website = self.get_subsite(self.get_sitePath(url)[0])
		self.url = self.check_url(url)
		self.push_url(self.url)
		self.get_page()
		
	def check_url(self,url):
		'''检查url格式:
		去除路径中多余的/;
		'''
		try:
			tmp_proto, url = urllib.splittype(url)
			url = ''.join(urllib.splithost(url))
			return tmp_proto + '://' + re.compile(r'/+').sub('/',url)
		except:
			#一些url地址"#",/duty/
			return ''

	def get_subsite(self, url):
		'''返回站点域名'''
		return ''.join(re.findall(r'\.\w+', url)[-2:])
	def check_site(self,url):
		'''检查url是否同一站点，是则返回True'''
		try:
			if self.get_subsite(self.get_sitePath(url)[0]) == self.website:
				return True
			else:
				return False
		except:
			return False
	def get_sitePath(self,url):
		return urllib.splithost(urllib.splittype(url)[1])
	def get_proto(self, url):
		return urllib.splittype(url)[0]
	
	def push_url(self, url):
		if url:
			print '''将url加入队列'''
		else:
			print '未加入url队列'
	def pop_url(self):
		print '''从队列中取出url'''
		return 'http://www.baidu.com'
		
	def get_fetchStatus(self):
		'''获得合并返回状态'''
		self.http = httplib.HTTP(self.host)
		#HTTP请求头部
		self.http.putrequest("GET", self.path)
		self.http.putheader("User-Agent", USER_AGENT)
		self.http.putheader("Host", self.path)
		self.http.putheader("Accept", "*/*")
		self.http.endheaders()
		#获得响应
		errcode, errmsg, headers = self.http.getreply()
		self.http_status = (errcode, errmsg, headers)
	def get_status(self):
		'''只获得状态码'''
		self.get_fetchStatus()
		return self.http_status[0]
	def check_status(self, status):
		print '''处理返回状态码'''
		return True
		
	def get_pageInfo(self, **dict_page):
		'''页面深度，页面状态消息'''
		dict_page['deep'] = None
		dict_page['info'] = None
		return dict_page
	def save_page(self, content):
		print '''将页面的内容存入本地数据库'''
	def re_url(self, **tag_attr):
		attr = tag_attr['attr']
		#re_u = lambda x: self.push_url(self.check_site(self.check_url(x[attr])))
		#map(re_u, tag_attr['tag'])
		for u in tag_attr['tag']:
			print u[attr]
			#import pdb
			#pdb.set_trace()
			self.push_url(self.check_site(self.check_url(u[attr])))
	def save_url(self, content):
		'''将页面上的url加入内存数据库'''
		soup = BeautifulStoneSoup(content)
		#获取页面的所有连接,检查url格式，是否同一域名
		#re_url = lambda tag_attr: self.push_url(self.check_site(self.check_url(tag_attr["tag"][tag_attr["attr"]])))
		self.re_url(tag=soup.findAll(attrs={'src':True}), attr='src')
		self.re_url(tag=soup.findAll(attrs={'href':True}),attr='href')
		#list_url.append(soup.findAll(attrs={'action':True}))
	
	def down_page(self, now_url, status):
		'''下载页面'''
		content=urllib2.urlopen(now_url).read()
		#将页面的内容存入本地数据库
		self.save_page(self.get_pageInfo(href=now_url,status=status, content=content))
		self.save_url(content)
	def get_page(self):
		now_url = self.pop_url()
		self.host, self.path = self.get_sitePath(now_url)
		status = self.check_status(self.get_status())
		if status:
			#202状态
			self.down_page(now_url, status)
				
	def find_key(self):
		print '''分析页面关键字'''
