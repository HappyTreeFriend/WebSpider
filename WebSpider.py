#!/usr/bin/env python
#coding=utf-8

import re,urllib,urllib2,cookielib
from BeautifulSoup import *
class WebSpider(object):
	'''网络爬虫功能模块
	'''
	def __init__(self, url, deep):
		self.cj=cookielib.CookieJar()
		self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(self.opener)
		self.url=url
		self.deep=deep
		self.proto, self.rest=urllib.splittype(self.url)
		self.website, self.webpath=urllib.splithost(self.rest)
	def down_page(self):
		now_url=self.url
		content=urllib2.urlopen(now_url).read()
		soup=BeautifulStoneSoup(content)
	def run(self):
		pass
				
class WebAnaly(object):
	def find_link(self):
		'''获取连接'''
		find_a=soup.findAll('a')	#[a,a,...]
		self.obj_href=list()
		for cnt in range(len(find_a)):
			self.obj_href.append(find_a[cnt]['href'])
	def find_key(self):
		'''分析页面关键字'''
		pass
	def do_url(self):
		'''处理获取到的url'''
		for cnt in range(len(self.obj_href)):
			tmp_href={'href':find_a[cnt]['href'],'status':0,'deep':0}
			tmp_href.deep=self.deep(tmp_href.href)
			if tmp_href.deep > self.deep:
				continue
			tmp_href.status=self.status(tmp_href.href)
			self.obj_href.append(tmp_href)

class UrlQ(object):
	def check(self):
		'''检查url的格式
		将路径中多个‘/’转换成一个
		'''
		re_href=re.compile(r'/+').sub('/',str1)
	def del_re(self):
		'''删掉重复的url'''
		return list(set(self.obj_href))
	def del_nosite(self):
		'''删掉无关的url'''
		pass
	def status(self):
		'''
		检查连接状态
		0：连接正常
		1：连接不成功
		'''
		pass
	def deep(self):
		'''检查连接深度，根目录深度为0，以后递增'''
		pass
