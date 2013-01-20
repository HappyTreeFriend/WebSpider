#!/usr/bin/env python
#coding=utf-8
import Queue,sys,time
from Common import *
class UrlQ(object):
	def __init__(self):
		self.urlQ = Queue.Queue(0)
		self.visit = list()
	def del_re(self, data):
		'''检查重复的url'''
		return comm.get_hash(data) in self.visit
	def putQ(self, data):
		if not self.del_re(data):
			self.urlQ.put(data)
			self.visit.append(comm.get_hash(data))
	def getQ(self):
		return self.urlQ.get()
	def wait_empty(self):
		self.urlQ.join()
	def is_empty(self):
		return self.urlQ.empty()
	def qsize(self):
		return self.urlQ.qsize()
		
import threading
#替我们工作的线程池中的线程
class MyThread(threading.Thread):
	def __init__(self, workQueue, resultQueue,timeout=3, **kwargs):
		threading.Thread.__init__(self, kwargs=kwargs)
		#线程在结束前等待任务队列多长时间
		self.timeout = timeout
		self.setDaemon(True)
		self.workQueue = workQueue
		self.resultQueue = resultQueue
		self.start()

	def run(self):
		while True:
			try:
				#从工作队列中获取一个任务
				callable, args, kwargs = self.workQueue.get(timeout=self.timeout)
				#我们要执行的任务
				try:
					res = callable(args, kwargs)
					if res:
						#把任务返回的结果放在结果队列中
						self.resultQueue.put(res+" | "+self.getName())    
				except:
					pass
			except Queue.Empty: #任务队列空的时候结束此线程
				break
				
class ThreadPool(object):
	def __init__(self, num_of_threads=3):
		self.workeQueue = Queue.Queue()
		self.resultQueue = Queue.Queue()
		self.threads = []
		self.__createThreadPool(num_of_threads)

	def __createThreadPool(self, num_of_threads):
		for i in range(num_of_threads):
			thread = MyThread(self.workeQueue, self.resultQueue)
			self.threads.append(thread)

	def wait_for_complete(self):
		#等待所有线程完成
		while len(self.threads):
			thread = self.threads.pop()
			#等待线程结束
			if thread.isAlive():
				#判断线程存活 是否调用join
				thread.join()
	def add_job(self, callable, *args, **kwargs):
		self.workeQueue.put((callable, args, kwargs))
		

if __name__=='__main__':
	testQ = UrlQ()
	testQ.putQ('1')
	print testQ.getQ()
	testQ.putQ('1')
	testQ.putQ('0')
	import pdb
	pdb.set_trace()
	print testQ.qsize()
