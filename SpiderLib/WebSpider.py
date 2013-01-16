#!/usr/bin/env python
#coding=utf-8

import re,Common,time
import httplib,urllib,urllib2,cookielib
from BeautifulSoup import *
from WorkerQ import *
from SpiderData import *
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
		self.url = self.check_url(url, url)
		self.urlq = UrlQ()
		self.push_url(self.url)
		#self.get_page()
		self.myJob()

	def myJob(self):
		while True:
			qsize = self.urlq.qsize()
			tp = ThreadPool(5)
			for i in range(qsize):
				time.sleep(0.5)
				tp.add_job(self.get_page)
			tp.wait_for_complete()
			#判断url队列的大小是否为0，等待30秒
			time.sleep(3)
			if self.urlq.is_empty():
				break
		
	def check_url(self, now_url, url):
		'''检查url格式:
		去除路径中多余的/;
		'''
		try:
			tmp_pro, tmp_url = urllib.splittype(now_url)
			if (url!='#' and url!='/') and (not re.match(r'https?://\w+(?:\.\w+)+', url)):
				#判断字符串格式
				url = tmp_pro + '://' + urllib.splithost(tmp_url)[0] + '/' + url
			tmp_proto, url = urllib.splittype(url)
			url = ''.join(urllib.splithost(url))
			return tmp_proto + '://' + re.compile(r'/+').sub('/',url)
		except:
			#一些url地址"#"
			return ''

	def get_subsite(self, url):
		'''返回站点域名'''
		#返回顶级域名
		#return ''.join(re.findall(r'\.\w+', url)[-2:])
		#返回子域名
		return url
	def check_site(self,url):
		'''检查url是否同一站点，是则返回True'''
		try:
			if self.get_subsite(self.get_sitePath(url)[0]) == self.website:
				return url
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
			self.urlq.putQ(url)
			print '''将url加入队列''',url
	def pop_url(self):
		#print '''从队列中取出url'''
		tmp = self.urlq.getQ()
		#import pdb
		#pdb.set_trace()
		print '''从队列中取出url''',tmp
		return tmp

	def get_fetchStatus(self, url):
		'''获得合并返回状态'''
		site_path = self.get_sitePath(url)
		self.http = httplib.HTTP(site_path[0])
		#HTTP请求头部
		self.http.putrequest("GET", site_path[1])
		self.http.putheader("User-Agent", USER_AGENT)
		self.http.putheader("Host", site_path[1])
		self.http.putheader("Accept", "*/*")
		self.http.endheaders()
		#获得响应
		errcode, errmsg, headers = self.http.getreply()
		self.http_status = (errcode, errmsg, headers)
	def get_status(self, url):
		'''只获得状态码'''
		self.get_fetchStatus(url)
		return self.http_status

	def get_urlDeep(self, url):
		'''返回url深度'''
		return self.get_sitePath(url)[1].count('/')
	def save_page(self, dict_page):
		print '''将页面的内容存入本地数据库'''
	def re_url(self, now_url, **tag_attr):
		attr = tag_attr['attr']
		#re_u = lambda x: self.push_url(self.check_site(self.check_url(x[attr])))
		#map(re_u, tag_attr['tag'])
		for u in tag_attr['tag']:
			#print u[attr]
			self.push_url(self.check_site(self.check_url(now_url, u[attr])))
	def save_url(self, content, now_url):
		'''将页面上的url加入内存数据库'''
		soup = BeautifulStoneSoup(content)
		#获取页面的所有连接,检查url格式，是否同一域名
		#re_url = lambda tag_attr: self.push_url(self.check_site(self.check_url(tag_attr["tag"][tag_attr["attr"]])))
		self.re_url(now_url, tag=soup.findAll(attrs={'src':True}), attr='src')
		self.re_url(now_url, tag=soup.findAll(attrs={'href':True}),attr='href')
		#list_url.append(soup.findAll(attrs={'action':True}))
	def wait_page(self):
		'''阻塞等待'''
		pass
	def redL_page(self):
		'''永久重定向url'''
		pass
	def redS_page(self):
		'''临时重定向url'''
		pass
	def down_page(self, now_url, status):
		'''下载页面'''
		content=urllib2.urlopen(now_url).read()
		key = self.find_key(content)
		if key:
			#将页面的内容存入本地数据库
			self.save_page({'href':now_url,'status':status[0], 'content':content, 'info':status[1], 'deep':self.get_urlDeep(now_url), 'key':key})
			self.save_url(content, now_url)
	def get_page(self, *args, **kwargs):
		now_url = self.pop_url()
		self.host, self.path = self.get_sitePath(now_url)
		status = self.get_status(now_url)
		print status
		self.after_status(status=status, url=now_url)
	def after_status(self, **obj):
		'''根据状态码，调用不同的处理方式'''
		statusFunc={
				200:self.down_page(obj['url'], obj['status']),
				202:self.wait_page(),#阻塞等待
				300:None,#丢弃
				301:self.redL_page(),#永久重定向
				302:self.redS_page(),#临时重定向
				}
		print obj['status']
		statusFunc[obj['status'][0]]
	def find_key(self, content):
		print '''分析页面关键字'''
		return 'GOOD'



if __name__=='__main__':
	WebSpider('http://www.baidu.com', 1)
