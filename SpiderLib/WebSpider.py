#!/usr/bin/env python
#coding=utf-8

import re,Common,time
import httplib,urllib,urllib2,cookielib
from BeautifulSoup import *
from WorkerQ import *
from SpiderData import *
from urlparse import urljoin, urlparse, urlunparse, ParseResult
USER_AGENT = "WebSpider.py"
class WebSpider(object):
	'''网络爬虫功能模块
	'''
	def __init__(self, url, deep):
		self.cj = cookielib.CookieJar()
		urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj)))

		self.deep = deep
		#检查用户输入的url，并加入访问队列
		self.website = self.get_subsite(self.get_scheme_netloc_path_(url).netloc)
		self.url = self.check_url(url, url)
		self.urlq = UrlQ()
		self.push_url(self.url)
		#self.get_page()
		self.myJob()

	def myJob(self):
		while True:
			qsize = self.urlq.qsize()
			tp = ThreadPool(5)
			print '创建5个线程池'
			for i in range(qsize):
				time.sleep(0.5)
				print '线程池',i
				tp.add_job(self.get_page)
			tp.wait_for_complete()
			print '线程池回收'
			#判断url队列的大小是否为0，等待30秒
			time.sleep(3)
			print '队列是否为空',self.urlq.is_empty(),self.urlq.qsize()
			if self.urlq.is_empty():
				break
		
	def check_url(self, now_url, url):
		'''检查url格式
		去除路径中多余的/;
		'''
		try:
			if not re.match(r'https?://\w+(?:\.\w+)+', url):
				#判断字符串格式
				url = urljoin(now_url, url)
			url_pack = self.get_scheme_netloc_path_(url)
			path = re.compile(r'/+').sub('/', url_pack.path)
			if path.__len__():
				if path[-1] == '/':
					path = path[:-1]
			url = urlunparse(ParseResult(scheme=url_pack.scheme, netloc=url_pack.netloc, path=path, params=url_pack.params, query=url_pack.query, fragment=url_pack.fragment))
		except ValueError:
			#一些url地址"#"
			print ValueError
			return False

	def get_subsite(self, url):
		'''返回站点域名'''
		#返回顶级域名
		#return ''.join(re.findall(r'\.\w+', url)[-2:])
		#返回子域名
		return url
	def check_site(self,url):
		'''检查url是否同一站点，是则返回True'''
		try:
			if self.get_subsite(self.get_scheme_netloc_path_(url).netloc) == self.website:
				return url
			else:
				return False
		except:
			return False
	def get_scheme_netloc_path_(self, url):
		'''返回协议类型，站点，路径'''
		return urlparse(url)


	def push_url(self, url):
		if url:
			self.urlq.putQ(url)
	def pop_url(self):
		#print '''从队列中取出url'''
		tmp = self.urlq.getQ()
		#import pdb
		#pdb.set_trace()
		print '''从队列中取出url''',tmp,self.get_urlDeep(tmp)
		return tmp

	def get_urlDeep(self, url):
		'''返回url深度'''
		return self.get_scheme_netloc_path_(url).path.count('/')
	def save_page(self, dict_page):
		print '''将页面的内容存入本地数据库'''
	def re_url(self, now_url, **tag_attr):
		attr = tag_attr['attr']
		for u in tag_attr['tag']:
			#print u[attr]
			self.push_url(self.check_site(self.check_url(now_url, u[attr])))
	def save_url(self, content, now_url):
		'''将页面上的url加入内存数据库'''
		soup = BeautifulStoneSoup(content)
		#获取页面的所有连接,检查url格式，是否同一域名
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
	def get_page(self, *args, **kwargs):
		'''下载页面'''
		now_url = self.pop_url()
		try:
			req = urllib2.urlopen(now_url)
			content = req.read()
			deep = self.get_urlDeep(now_url)
			visit_url = req.geturl()
			status = req.getcode()
			msg = req.msg
		except URLError, e:
			visit_url = now_url
			status = e.code
			msg = e.reason
			self.after_status(status=status)
		key = self.find_key(content)
		if key:
			#将页面的内容存入本地数据库
			self.save_url(content, now_url)
			if deep <= self.deep:
				self.save_page({'href':now_url,'url':visit_url,'status':status, 'content':content, 'msg':msg, 'deep':deep, 'key':key, 'src_url': self.url, 'site':self.get_scheme_netloc_path_(now_url).netloc})
	def after_status(self, **obj):
		'''根据状态码，调用不同的处理方式'''
		statusFunc={
				202:self.wait_page(),#阻塞等待
				300:None,#丢弃
				301:self.redL_page(),#永久重定向
				302:self.redS_page(),#临时重定向
				}
		statusFunc[obj['status']]
	def find_key(self, content):
		print '''分析页面关键字'''
		return 'GOOD'

if __name__=='__main__':
	WebSpider('http://www.baidu.com', 1)
